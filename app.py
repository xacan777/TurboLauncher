import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pyodbc
from Laucnher import (
    SAMPLE_DROPLIST,
    SAMPLE_ENHANCEMENT,
    SAMPLE_FORUM,
    SAMPLE_LEADERBOARD,
    SAMPLE_NEWS,
    SQL_CHECK_EXISTS,
    SQL_CHECK_USER,
    SQL_CREATE_USER,
    SQL_DROPLIST_BASE,
    SQL_ENHANCEMENT_BASE,
    SQL_FORUM_CREATE_MESSAGE,
    SQL_FORUM_CREATE_TOPIC,
    SQL_FORUM_MESSAGES,
    SQL_FORUM_TOPICS,
    SQL_LEADERBOARD_LEVELS,
    SQL_LEADERBOARD_POWER,
    SQL_UPDATE_IP,
)
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING", "")
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "5000"))
FORUM_JSON_PATH = Path(os.getenv("FORUM_JSON_PATH", "forum.json"))
NEWS_PATH = Path(os.getenv("NEWS_PATH", "news.json"))


# --- helpers ----------------------------------------------------------------
def get_db_connection() -> Optional[pyodbc.Connection]:
    if not DB_CONNECTION_STRING:
        return None
    try:
        return pyodbc.connect(DB_CONNECTION_STRING, timeout=5)
    except pyodbc.Error as exc:  # pragma: no cover - env specific
        print("DB connection failed:", exc)
        return None


def hash_token(username: str) -> str:
    return hashlib.sha256(f"{username}:{datetime.utcnow().isoformat()}".encode()).hexdigest()


def ensure_json_file(path: Path, payload: Dict[str, Any]) -> None:
    if not path.exists():
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def persist_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def validate_username(username: str) -> Tuple[bool, str]:
    if not username or len(username.strip()) < 3:
        return False, "Имя пользователя должно содержать минимум 3 символа"
    return True, ""


def validate_password(password: str) -> Tuple[bool, str]:
    if not password or len(password) < 6:
        return False, "Пароль должен содержать минимум 6 символов"
    return True, ""


def ensure_forum_snapshot() -> Dict[str, Any]:
    ensure_json_file(FORUM_JSON_PATH, SAMPLE_FORUM)
    return read_json(FORUM_JSON_PATH)


def sync_forum_from_db(conn: Optional[pyodbc.Connection]) -> Dict[str, Any]:
    if not conn:
        return ensure_forum_snapshot()

    topics: List[Dict[str, Any]] = []
    messages: List[Dict[str, Any]] = []
    try:
        cur = conn.cursor()
        cur.execute(SQL_FORUM_TOPICS)
        for row in cur.fetchall():
            topics.append(
                {
                    "id": int(row[0]),
                    "title": row[1],
                    "author": row[2],
                    "created_at": row[3].isoformat() if row[3] else None,
                    "updated_at": row[4].isoformat() if row[4] else None,
                    "message_count": int(row[5]) if row[5] is not None else 0,
                    "last_message_at": row[6].isoformat() if row[6] else None,
                }
            )

        cur.execute(SQL_FORUM_MESSAGES)
        for row in cur.fetchall():
            messages.append(
                {
                    "id": int(row[0]),
                    "topic_id": int(row[1]),
                    "author": row[2],
                    "text": row[3],
                    "created_at": row[4].isoformat() if row[4] else None,
                }
            )
    except pyodbc.Error as exc:  # pragma: no cover - env specific
        print("Forum sync failed:", exc)
        return ensure_forum_snapshot()

    payload = {"topics": topics, "messages": messages}
    persist_json(FORUM_JSON_PATH, payload)
    return payload


def rebuild_forum_snapshot() -> Dict[str, Any]:
    conn = get_db_connection()
    forum_data = sync_forum_from_db(conn)
    if conn:
        conn.close()
    return forum_data


def get_local_forum() -> Dict[str, Any]:
    ensure_json_file(FORUM_JSON_PATH, SAMPLE_FORUM)
    return read_json(FORUM_JSON_PATH)


def news_feed() -> List[Dict[str, Any]]:
    ensure_json_file(NEWS_PATH, {"items": SAMPLE_NEWS})
    payload = read_json(NEWS_PATH)
    return payload.get("items", SAMPLE_NEWS)


# --- routes: health & news --------------------------------------------------
@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "brand": "TURBO"})


@app.get("/api/news")
def api_news():
    return jsonify({"items": news_feed()})


@app.get("/api/server/status")
def server_status():
    conn = get_db_connection()
    if not conn:
        return jsonify({"online": True, "players": 0})
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM FNLAccount.dbo.TblUser WHERE mWorldNo = 777")
        players = cur.fetchone()[0] or 0
        return jsonify({"online": players > 0, "players": players})
    except pyodbc.Error as exc:  # pragma: no cover - env specific
        print("server_status error:", exc)
        return jsonify({"online": False, "players": 0})
    finally:
        conn.close()


# --- auth -------------------------------------------------------------------
@app.post("/api/auth/login")
def login():
    data = request.get_json(force=True, silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    ok, err = validate_username(username)
    if not ok:
        return jsonify({"success": False, "error": err}), 400
    ok, err = validate_password(password)
    if not ok:
        return jsonify({"success": False, "error": err}), 400

    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(SQL_CHECK_USER, (username, password))
            row = cur.fetchone()
            if not row:
                return jsonify({"success": False, "error": "Неверный логин или пароль"}), 401
            cur.execute(SQL_UPDATE_IP, (request.remote_addr, username))
            conn.commit()
        except pyodbc.Error as exc:  # pragma: no cover - env specific
            print("Login error:", exc)
            conn.rollback()
            return jsonify({"success": False, "error": "Ошибка базы данных"}), 500
        finally:
            conn.close()
    elif username != "demo" or password != "demo":
        return jsonify({"success": False, "error": "Недоступно без БД. Используйте demo/demo."}), 503

    token = hash_token(username)
    user = {"username": username}
    return jsonify({"success": True, "token": token, "user": user})


@app.post("/api/auth/register")
def register():
    data = request.get_json(force=True, silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    ok, err = validate_username(username)
    if not ok:
        return jsonify({"success": False, "error": err}), 400
    ok, err = validate_password(password)
    if not ok:
        return jsonify({"success": False, "error": err}), 400

    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(SQL_CHECK_EXISTS, (username,))
            exists = cur.fetchone()[0] > 0
            if exists:
                return jsonify({"success": False, "error": "Пользователь уже существует"}), 409
            cur.execute(SQL_CREATE_USER, (username, password, "turbo"))
            conn.commit()
        except pyodbc.Error as exc:  # pragma: no cover - env specific
            print("Register error:", exc)
            conn.rollback()
            return jsonify({"success": False, "error": "Ошибка базы данных"}), 500
        finally:
            conn.close()
    return jsonify({"success": True})


# --- leaderboard ------------------------------------------------------------
def get_class_column(lang: str) -> str:
    return {
        "Korean": "classnamekr",
        "Chinese": "classnamecn",
        "Russian": "classnameru",
    }.get(lang, "classnameru")


@app.get("/api/leaderboard/levels")
def leaderboard_levels():
    lang = request.args.get("lang", "Russian")
    conn = get_db_connection()
    data = []
    if conn:
        try:
            cur = conn.cursor()
            query = SQL_LEADERBOARD_LEVELS.format(class_col=get_class_column(lang))
            cur.execute(query)
            rows = cur.fetchall()
            data = [
                {
                    "name": row[0],
                    "level": int(row[1]) if row[1] is not None else 0,
                    "class": row[2],
                }
                for row in rows
            ]
        except pyodbc.Error as exc:  # pragma: no cover - env specific
            print("leaderboard_levels error:", exc)
        finally:
            conn.close()
    if not data:
        data = [{"name": item["name"], "level": item["level"], "class": item["class"]} for item in SAMPLE_LEADERBOARD]
    return jsonify({"success": True, "data": data})


@app.get("/api/leaderboard/power")
def leaderboard_power():
    lang = request.args.get("lang", "Russian")
    conn = get_db_connection()
    data = []
    if conn:
        try:
            cur = conn.cursor()
            query = SQL_LEADERBOARD_POWER.format(class_col=get_class_column(lang))
            cur.execute(query)
            rows = cur.fetchall()
            data = [
                {
                    "name": row[0],
                    "power": int(row[1]) if row[1] is not None else 0,
                    "class": row[2],
                }
                for row in rows
            ]
        except pyodbc.Error as exc:  # pragma: no cover - env specific
            print("leaderboard_power error:", exc)
        finally:
            conn.close()
    if not data:
        data = [{"name": item["name"], "power": item["power"], "class": item["class"]} for item in SAMPLE_LEADERBOARD]
    return jsonify({"success": True, "data": data})


# --- droplist ---------------------------------------------------------------
def localized_columns(lang: str) -> Tuple[str, str, str]:
    suffix = {"Korean": "KR", "Chinese": "CN"}.get(lang, "")
    item_col = f"i.iname{suffix}" if suffix else "i.iname"
    monster_col = f"m.mname{suffix}" if suffix else "m.mname"
    place_col = f"m.MonsterPlace{suffix}" if suffix else "m.MonsterPlace"
    return item_col, monster_col, place_col


@app.get("/api/droplist")
def droplist():
    lang = request.args.get("lang", "Russian")
    name = (request.args.get("iname", "") or "").strip()
    monster = (request.args.get("mname", "") or "").strip()
    place = (request.args.get("place", "") or "").strip()

    conn = get_db_connection()
    data = []
    if conn:
        try:
            cur = conn.cursor()
            item_col, monster_col, place_col = localized_columns(lang)
            base_sql = SQL_DROPLIST_BASE.format(
                item_col=item_col, monster_col=monster_col, place_col=place_col
            )
            filters = []
            params: List[Any] = []
            if name:
                filters.append(f"{item_col} LIKE ?")
                params.append(f"%{name}%")
            if monster:
                filters.append(f"{monster_col} LIKE ?")
                params.append(f"%{monster}%")
            if place:
                filters.append(f"{place_col} LIKE ?")
                params.append(f"%{place}%")
            query = base_sql + (" AND " + " AND ".join(filters) if filters else "")
            cur.execute(query, params)
            rows = cur.fetchall()
            data = [
                {
                    "item_id": row[0],
                    "item_name": row[1],
                    "count": row[2],
                    "monster_name": row[3],
                    "place": row[4],
                    "status": row[5],
                }
                for row in rows
            ]
        except pyodbc.Error as exc:  # pragma: no cover - env specific
            print("droplist error:", exc)
        finally:
            conn.close()
    if not data:
        data = SAMPLE_DROPLIST
    return jsonify({"success": True, "data": data})


# --- enhancement ------------------------------------------------------------
@app.get("/api/enhancement")
def enhancement():
    lang = request.args.get("lang", "Russian")
    iname = (request.args.get("iname") or "").strip()
    type_filter = (request.args.get("type") or "all").lower()

    conn = get_db_connection()
    data = []
    if conn:
        try:
            cur = conn.cursor()
            query = SQL_ENHANCEMENT_BASE
            if type_filter == "weapon":
                query += " AND i.TypeWeapon > 0"
            elif type_filter == "defense":
                query += " AND i.TypeDef > 0"
            query += " ORDER BY i.IID"
            cur.execute(query, f"%{iname}%")
            rows = cur.fetchall()
            data = [
                {
                    "item_id": row[0],
                    "iname": row[1],
                    "scroll_name": row[2],
                    "rsuccess": round(float(row[3]), 2) if row[3] else 0.0,
                }
                for row in rows
            ]
        except pyodbc.Error as exc:  # pragma: no cover - env specific
            print("enhancement error:", exc)
        finally:
            conn.close()
    if not data:
        data = SAMPLE_ENHANCEMENT
    return jsonify({"success": True, "data": data})


# --- forum ------------------------------------------------------------------
def update_forum_file(payload: Dict[str, Any]) -> None:
    persist_json(FORUM_JSON_PATH, payload)


def next_id(items: List[Dict[str, Any]]) -> int:
    return (max([item["id"] for item in items], default=0) + 1) if items else 1


@app.get("/api/forum/topics")
def forum_topics():
    payload = get_local_forum()
    return jsonify({"topics": payload.get("topics", [])})


@app.post("/api/forum/topics")
def forum_create_topic():
    body = request.get_json(force=True, silent=True) or {}
    title = (body.get("title") or "").strip()
    author = (body.get("author") or "anonymous").strip() or "anonymous"
    message = (body.get("message") or "").strip()

    if len(title) < 3 or len(title) > 120:
        return jsonify({"error": "Заголовок должен быть от 3 до 120 символов"}), 400
    if len(message) < 1 or len(message) > 2000:
        return jsonify({"error": "Сообщение должно быть от 1 до 2000 символов"}), 400

    forum_data = get_local_forum()
    topics = forum_data.get("topics", [])
    messages = forum_data.get("messages", [])

    topic_id = next_id(topics)
    now = datetime.utcnow().isoformat()
    topic = {
        "id": topic_id,
        "title": title,
        "author": author,
        "created_at": now,
        "updated_at": now,
        "message_count": 1,
        "last_message_at": now,
    }
    topics.append(topic)

    msg_id = next_id(messages)
    messages.append(
        {
            "id": msg_id,
            "topic_id": topic_id,
            "author": author,
            "text": message,
            "created_at": now,
        }
    )

    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(SQL_FORUM_CREATE_TOPIC, (title, author))
            db_topic_id = int(cur.fetchone()[0])
            cur.execute(SQL_FORUM_CREATE_MESSAGE, (db_topic_id, author, message))
            conn.commit()
            rebuild_forum_snapshot()
            conn.close()
            payload = read_json(FORUM_JSON_PATH)
            return jsonify({"topic": payload["topics"][-1]})
        except pyodbc.Error as exc:  # pragma: no cover - env specific
            print("forum create topic error:", exc)
            conn.rollback()
            conn.close()

    update_forum_file({"topics": topics, "messages": messages})
    return jsonify({"topic": topic})


@app.get("/api/forum/topics/<int:topic_id>/messages")
def forum_messages(topic_id: int):
    payload = get_local_forum()
    messages = [m for m in payload.get("messages", []) if m.get("topic_id") == topic_id]
    return jsonify({"messages": messages})


@app.post("/api/forum/topics/<int:topic_id>/messages")
def forum_add_message(topic_id: int):
    body = request.get_json(force=True, silent=True) or {}
    author = (body.get("author") or "anonymous").strip() or "anonymous"
    text = (body.get("text") or "").strip()

    if len(text) < 1 or len(text) > 2000:
        return jsonify({"error": "Сообщение должно быть от 1 до 2000 символов"}), 400

    forum_data = get_local_forum()
    topics = forum_data.get("topics", [])
    messages = forum_data.get("messages", [])

    topic = next((t for t in topics if t.get("id") == topic_id), None)
    if not topic:
        return jsonify({"error": "Тема не найдена"}), 404

    msg_id = next_id(messages)
    now = datetime.utcnow().isoformat()
    message = {
        "id": msg_id,
        "topic_id": topic_id,
        "author": author,
        "text": text,
        "created_at": now,
    }
    messages.append(message)
    topic["message_count"] = topic.get("message_count", 0) + 1
    topic["last_message_at"] = now
    topic["updated_at"] = now

    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(SQL_FORUM_CREATE_MESSAGE, (topic_id, author, text))
            conn.commit()
            rebuild_forum_snapshot()
            conn.close()
            payload = read_json(FORUM_JSON_PATH)
            updated_topic = next((t for t in payload["topics"] if t["id"] == topic_id), topic)
            return jsonify({"message": payload["messages"][-1], "topic": updated_topic})
        except pyodbc.Error as exc:  # pragma: no cover - env specific
            print("forum message error:", exc)
            conn.rollback()
            conn.close()

    update_forum_file({"topics": topics, "messages": messages})
    return jsonify({"message": message, "topic": topic})


# --- startup ---------------------------------------------------------------
if __name__ == "__main__":
    ensure_json_file(NEWS_PATH, {"items": SAMPLE_NEWS})
    rebuild_forum_snapshot()
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=False)
