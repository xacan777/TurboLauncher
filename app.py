from flask import Flask, request, jsonify, send_from_directory
from util import get_db_connection, validate_username, validate_password, get_app_version
import pyodbc
import json
import os

app = Flask(__name__)

# --- Версионирование клиента и файлов ---
server_version = get_app_version()

files_to_update = [
    {'folder': 'etc', 'name': 'etc.rfs', 'version': '1.7',
     'url': 'https://www.dropbox.com/scl/fi/zrdveap3ph7l44lu69cny/etc.rfs?rlkey=ih83bqucgexh2lc1hz051wn3g&st=xz3yj4ll&dl=1'},
    {'folder': 'gui', 'name': 'gui.rfs', 'version': '1.7',
     'url': 'https://www.dropbox.com/scl/fi/ehey3x7aokoukkxkmuz0u/gui.rfs?rlkey=0wulndvwksf2801sd5f92ozen&st=e63c6anh&dl=1'},
    {'folder': '.', 'name': 'r2.cfg', 'version': '5',
     'url': 'https://www.dropbox.com/scl/fi/nt9zdl4nbihn5v1oim16z/R2.cfg?rlkey=2pz4n58xglwe74qzx1teoqd91&st=e5b19djb&dl=1'}
]

@app.get("/get_server_version")
def get_server_version():
    return jsonify({'version': server_version})

@app.get("/version")
def get_version():
    return jsonify({'version': server_version, 'files': files_to_update})

@app.post("/check_files")
def check_files():
    client_files = request.json.get('files', [])
    files_to_download = []
    for srv in files_to_update:
        cli = next((f for f in client_files if f['name'] == srv['name']), None)
        if not cli or cli.get('version') != srv['version']:
            files_to_download.append(srv)
    return jsonify({'files_to_download': files_to_download})

# --- Аутентификация ---
@app.post("/login")
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'error': 'Missing username or password'}), 400
    ok, err = validate_username(username)
    if not ok: return jsonify({'success': False, 'error': err}), 400
    ok, err = validate_password(password)
    if not ok: return jsonify({'success': False, 'error': err}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database connection error'}), 500

    try:
        cur = conn.cursor()
        cur.execute('SELECT mUserId, mUserSuperPswd FROM TblUser WHERE mUserId=? AND mUserSuperPswd=?',
                    (username, password))
        row = cur.fetchone()
        if row:
            user_ip = request.remote_addr
            try:
                cur.execute('UPDATE TblUser SET mip=? WHERE mUserId=?', (user_ip, username))
                conn.commit()
            except pyodbc.Error as e:
                print("DB update IP error:", e)
                conn.rollback()
                return jsonify({'success': False, 'error': 'Database error'}), 500
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Invalid login or password'}), 401
    finally:
        conn.close()

def get_lang_column(base_name: str, lang: str) -> str:
    """
    Возвращает имя столбца с учетом языка.
    Учитывает, что некоторые таблицы используют нестандартные имена:
      iname -> inameKR/CN
      MonsterName -> MonsterNameKR/CN
      MonsterPlace -> MonsterPlaceKR/CN
    """
    suffix = {
        "Korean": "KR",
        "Chinese": "CN",
        "Russian": ""
    }.get(lang, "")

    # специальные случаи
    mapping = {
        "mname": "MonsterName",
        "iname": "iname",
        "MonsterPlace": "MonsterPlace"
    }

    base_col = mapping.get(base_name, base_name)
    return f"{base_col}{suffix}" if suffix else base_col


@app.post("/register")
def register():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'error': 'Missing username or password'}), 400
    ok, err = validate_username(username)
    if not ok: return jsonify({'success': False, 'error': err}), 400
    ok, err = validate_password(password)
    if not ok: return jsonify({'success': False, 'error': err}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database connection error'}), 500

    try:
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM TblUser WHERE mUserId=?', (username,))
        exists = cur.fetchone()[0] > 0
        if exists:
            return jsonify({'success': False, 'error': 'Username already exists'}), 409

        cur.execute('INSERT INTO TblUser (mUserId, mUserSuperPswd, mUserPswd) VALUES (?, ?, ?)',
                    (username, password, 'nhngames'))
        conn.commit()
        return jsonify({'success': True})
    except pyodbc.Error as e:
        print("DB insert error:", e)
        return jsonify({'success': False, 'error': 'Database error'}), 500
    finally:
        conn.close()

@app.post("/update_ip")
def update_ip():
    data = request.json or {}
    username = data.get('username')
    if not username:
        return jsonify({'success': False, 'error': 'Missing username'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database connection error'}), 500

    try:
        cur = conn.cursor()
        cur.execute('UPDATE TblUser SET mip=? WHERE mUserId=?', (request.remote_addr, username))
        conn.commit()
        return jsonify({'success': True})
    except pyodbc.Error as e:
        print("DB update IP error:", e)
        conn.rollback()
        return jsonify({'success': False, 'error': 'Database error'}), 500
    finally:
        conn.close()

# --- Новости (ручное заполнение) ---
NEWS_FILE = "news.json"
if not os.path.exists(NEWS_FILE):
    with open(NEWS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

@app.get("/news")
def get_news():
    with open(NEWS_FILE, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))

@app.post("/news")  # простой ручной эндпоинт (можно защитить токеном)
def add_news():
    # ожидается: { "title": "...", "body": "...", "image_url": "http://...", "date": "2025-10-10" }
    item = request.json or {}
    with open(NEWS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    data.insert(0, item)
    with open(NEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return jsonify({"success": True})

# --- Персонажи: уровни/класс ---
@app.get("/characters/<username>")
def characters(username):
    """
    ЗАПРОС ПРИМЕРНЫЙ: возможно, у вас другая схема/таблицы.
    Скорректируйте FROM/JOIN под реальные названия.
    """
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database connection error'}), 500
    try:
        cur = conn.cursor()
        # Пример: получение персонажей аккаунта
        # Ниже — вариант, если таблица персонажей в другой БД (FNLGame) и ссылается на аккаунт по mUserId
        # Измените имена таблиц/полей под точные (вы упомянули: charactersname, mlevel, characterclass)
        query = """
        SELECT c.charactersname, c.mlevel, c.characterclass
        FROM FNLGame.dbo.[fnlaccount.user를 통한 문자 레벨] c
        INNER JOIN FNLAccount.dbo.TblUser u ON c.identifier = u.mUserId
        WHERE u.mUserId = ?
        ORDER BY c.mlevel DESC
        """
        cur.execute(query, (username,))
        rows = cur.fetchall()
        out = [
            {
                "name": r[0],
                "level": int(r[1]) if r[1] is not None else None,
                "class": r[2]
            } for r in rows
        ]
        return jsonify({"success": True, "characters": out})
    except pyodbc.Error as e:
        print("DB characters error:", e)
        return jsonify({'success': False, 'error': 'Database error'}), 500
    finally:
        conn.close()

@app.get("/leaderboard/levels")
def leaderboard_levels():
    """
    Таблица лидеров по уровню персонажей.
    """
    lang = request.args.get("lang", "Russian")
    class_col = {
        "Korean": "classnamekr",
        "Chinese": "classnamecn",
        "Russian": "classnameru"
    }.get(lang, "classnameru")

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database connection error'}), 500

    try:
        cur = conn.cursor()
        query = f"""
        SELECT TOP 100
            c.charactersname,
            c.mlevel,
            c.{class_col}
        FROM FNLGame.dbo.[fnlaccount.user를 통한 문자 레벨] AS c
        WHERE c.charactersname IS NOT NULL
        ORDER BY c.mlevel DESC
        """
        cur.execute(query)
        rows = cur.fetchall()
        out = [
            {
                "name": r[0],
                "level": int(r[1]) if r[1] is not None else 0,
                "class": r[2]
            } for r in rows
        ]
        return jsonify({"success": True, "data": out})
    except Exception as e:
        print("DB leaderboard_levels error:", e)
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()




@app.get("/leaderboard/power")
def leaderboard_power():
    """
    Таблица лидеров по суммарной силе предметов.
    """
    lang = request.args.get("lang", "Russian")
    class_col = {
        "Korean": "classnamekr",
        "Chinese": "classnamecn",
        "Russian": "classnameru"
    }.get(lang, "classnameru")

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database connection error'}), 500

    try:
        cur = conn.cursor()
        query = f"""
        SELECT TOP 100
            mNm,
            SUM(CAST(Сила_предмета AS INT)) AS TotalPower,
            {class_col}
        FROM fnlgame.dbo.power_pc
        GROUP BY mNm, {class_col}
        ORDER BY TotalPower DESC;
        """
        cur.execute(query)
        rows = cur.fetchall()

        out = [
            {
                "name": r[0],
                "power": int(r[1]) if r[1] is not None else 0,
                "class": r[2]
            } for r in rows
        ]
        return jsonify({"success": True, "data": out})

    except Exception as e:
        print("DB leaderboard_power error:", e)
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()

@app.get("/server/status")
def server_status():
    """
    Возвращает статус сервера и количество игроков на worldNo=777.
    Если игроков нет — сервер считается OFFLINE.
    """
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"online": False, "players": 0})

        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM FNLAccount.dbo.TblUser WHERE mWorldNo = 777")
        players = cur.fetchone()[0] or 0

        # если 0 игроков — считаем сервер оффлайн
        if players == 0:
            return jsonify({"online": False, "players": 0})
        else:
            return jsonify({"online": True, "players": players})

    except Exception as e:
        print("server_status error:", e)
        return jsonify({"online": False, "players": 0})
    finally:
        try:
            conn.close()
        except:
            pass

@app.get("/enhancement")
def enhancement():
    """
    Возвращает таблицу усилений с шансами и свитками.
    Фильтры: имя предмета, тип (оружие / защита / все)
    """
    lang = request.args.get("lang", "Russian")
    iname = (request.args.get("iname") or "").strip()
    type_filter = (request.args.get("type") or "all").lower()

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database connection error'}), 500

    try:
        cur = conn.cursor()
        query = """
        SELECT TOP 5000
            r.ritemid0 AS item_id,
            i.iname AS item_name,
            s.iname AS scroll_name,
            ROUND(r.rsuccess, 2) AS rsuccess,
            i.TypeWeapon,
            i.TypeDef
        FROM fnlparm.dbo.DT_Refine AS r
        JOIN fnlparm.dbo.DT_Item AS i ON r.ritemid0 = i.IID
        LEFT JOIN fnlparm.dbo.DT_Item AS s ON r.id_scroll = s.IID
        WHERE (i.TypeWeapon > 0 AND i.TypeWeapon < 5 OR i.TypeDef > 0 AND i.TypeDef < 5)
          AND i.iname LIKE ?
        """

        # --- фильтр по типу ---
        if type_filter == "weapon":
            query += " AND i.TypeWeapon > 0"
        elif type_filter == "defense":
            query += " AND i.TypeDef > 0"

        query += " ORDER BY i.IID"

        cur.execute(query, f"%{iname}%")
        rows = cur.fetchall()

        out = [
            {
                "item_id": r[0],
                "iname": r[1],
                "scroll_name": r[2],
                "rsuccess": round(float(r[3]), 2) if r[3] else 0.0,
            }
            for r in rows
        ]
        return jsonify({"success": True, "data": out})

    except Exception as e:
        print("DB enhancement error:", e)
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()


@app.get("/daily_reward")
def daily_reward():
    username = request.args.get("username")
    if not username:
        return jsonify({'success': False, 'error': 'No username provided'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'DB connection failed'}), 500

    try:
        cur = conn.cursor()

        # 1) Состояние игрока
        cur.execute("""
            SELECT mWorldNo, mBalance
            FROM FNLAccount.dbo.TblUser
            WHERE mUserId=?
        """, (username,))
        row = cur.fetchone()
        if not row:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        mWorldNo, mBalance = row
        print(f"[DEBUG] User: mWorldNo={mWorldNo}, mBalance={mBalance}")

        # 2) Стратегия чтения Balance:
        #    а) Попробуем получить "последнюю" запись по пользователю (если таких несколько).
        #    б) Сразу подготовим булево: есть ли у пользователя запись с no=378.
        cur.execute("""
            SELECT TOP 1 [no]
            FROM FNLAccount.dbo.Balance
            WHERE mUserId=?
            ORDER BY [no] DESC
        """, (username,))
        row = cur.fetchone()
        last_no = None
        if row is not None:
            # аккуратно нормализуем тип (убираем пробелы/CRLF и приводим к int)
            try:
                last_no = int(str(row[0]).strip())
            except Exception:
                last_no = None

        cur.execute("""
            SELECT COUNT(*)
            FROM FNLAccount.dbo.Balance
            WHERE mUserId=? AND [no]=?
        """, (username, 378))
        has_no_378 = (cur.fetchone()[0] > 0)

        print(f"[DEBUG] Balance: last_no={last_no}, has_no_378={has_no_378}")

        # 3) Все задания на сегодня
        cur.execute("""
            SELECT id, task_name, is_done
            FROM FNLAccount.dbo.DailyTasks
            WHERE username=? AND CAST(task_date AS DATE)=CAST(GETDATE() AS DATE)
        """, (username,))
        tasks = cur.fetchall()
        if not tasks:
            return jsonify({'success': True, 'message': 'No tasks for today'})

        updated = 0
        for t_id, task_name, is_done in tasks:
            if is_done != 0:
                continue  # уже обработанные не трогаем

            task_lower = (task_name or "").lower()

            # 1) "войдите" → mWorldNo == 777
            if ("войдите" in task_lower) and (mWorldNo == 777):
                cur.execute("""
                    UPDATE FNLAccount.dbo.DailyTasks
                    SET is_done = 1
                    WHERE id=? AND username=? AND is_done=0
                """, (t_id, username))
                updated += 1

        conn.commit()

        # 4) Итоги
        cur.execute("""
            SELECT COUNT(*)
            FROM FNLAccount.dbo.DailyTasks
            WHERE username=? AND CAST(task_date AS DATE)=CAST(GETDATE() AS DATE)
        """, (username,))
        count_today = cur.fetchone()[0]

        cur.execute("""
            SELECT COUNT(*)
            FROM FNLAccount.dbo.DailyTasks
            WHERE username=? AND is_done=1 AND CAST(task_date AS DATE)=CAST(GETDATE() AS DATE)
        """, (username,))
        can_claim = cur.fetchone()[0] > 0

        return jsonify({
            'success': True,
            'updated': updated,
            'has_tasks_today': count_today > 0,
            'can_claim': can_claim
        })

    except Exception as e:
        print("daily_reward error:", e)
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()


@app.post("/daily_reward")
def claim_daily_reward():
    """
    Выдаёт награду за выполненные задания:
      - Проверяет статус (is_done=1)
      - Получает mUserNo
      - Добавляет запись в FNLBilling.dbo.TblSysOrderList
      - Обновляет статус (is_done=2)
    """
    data = request.json or {}
    username = data.get("username")
    task_id = data.get("task_id")

    if not username or not task_id:
        return jsonify({'success': False, 'error': 'Missing parameters'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'DB connection failed'}), 500

    try:
        cur = conn.cursor()

        # --- Проверяем задание ---
        cur.execute("""
            SELECT task_name, reward_name, is_done
            FROM FNLAccount.dbo.DailyTasks
            WHERE id=? AND username=? AND CAST(task_date AS DATE)=CAST(GETDATE() AS DATE)
        """, (task_id, username))
        row = cur.fetchone()
        if not row:
            return jsonify({'success': False, 'error': 'Task not found'}), 404

        task_name, reward_name, is_done = row
        if is_done == 0:
            return jsonify({'success': False, 'error': 'Task not completed'}), 400
        if is_done == 2:
            return jsonify({'success': False, 'error': 'Reward already claimed'}), 400

        # --- Получаем mUserNo по логину ---
        cur.execute("SELECT mUserNo FROM FNLAccount.dbo.TblUser WHERE mUserId=?", (username,))
        row = cur.fetchone()
        if not row:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        mUserNo = row[0]

        # --- Определяем награду по названию задания ---
        item_id = 409   # золото
        count = 10000000
        item_name = reward_name or "Награда"

        # Можно кастомизировать под разные задания
        if "войдите" in task_name.lower():
            item_id = 409
            count = 10000000
            item_name = "10 000 000 серебра"
        elif "баланс" in task_name.lower():
            item_id = 410
            count = 1000
            item_name = "1 000 баланса"
        elif "проверка" in task_name.lower():
            item_id = 153
            count = 1
            item_name = "проверка"

        # --- Добавляем награду в TblSysOrderList ---
        cur.execute("""
            INSERT INTO FNLBilling.dbo.TblSysOrderList (
                mRegDate, mSysID, mUserNo, mSvrNo, mItemID, mCnt,
                mAvailablePeriod, mPracticalPeriod, mStatus, mLimitedDate, ItemName
            )
            VALUES (
                GETDATE(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, (
            777,         # mSysID
            mUserNo,     # mUserNo
            777,         # mSvrNo
            item_id,     # mItemID
            count,       # mCnt
            0, 0, 0,
            '2070-01-01',
            item_name
        ))

        # --- Помечаем задание как полученное ---
        cur.execute("""
            UPDATE FNLAccount.dbo.DailyTasks
            SET is_done = 2
            WHERE id=? AND username=? AND CAST(task_date AS DATE)=CAST(GETDATE() AS DATE)
        """, (task_id, username))

        conn.commit()
        return jsonify({'success': True, 'reward': item_name})

    except Exception as e:
        conn.rollback()
        print("claim_daily_reward error:", e)
        return jsonify({'success': False, 'error': str(e)}), 500

    finally:
        conn.close()

@app.get("/daily_tasks")
def daily_tasks():
    username = request.args.get("username")
    if not username:
        return jsonify({'success': False, 'error': 'No username provided'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'DB failed'}), 500

    try:
        cur = conn.cursor()

        # --- Проверяем статус игрока в TblUser ---
        cur.execute("SELECT mWorldNo FROM FNLAccount.dbo.TblUser WHERE mUserId=?", (username,))
        row = cur.fetchone()
        if row:
            world_no = row[0]
            # Если игрок находится в игре — выставляем is_done = 1 для задания входа
            if world_no == 777:
                cur.execute("""
                    UPDATE FNLAccount.dbo.DailyTasks
                    SET is_done = 1
                    WHERE username=? 
                      AND task_name=N'Войдите в игру и получите подарок!' 
                      AND CAST(task_date AS DATE)=CAST(GETDATE() AS DATE)
                      AND is_done = 0
                """, (username,))
                conn.commit()

        # --- Загружаем задания на сегодня ---
        cur.execute("""
            SELECT
                id,
                task_name,
                LTRIM(RTRIM(REPLACE(REPLACE(reward_name, CHAR(13), ' '), CHAR(10), ' '))) AS reward_name,
                is_done,
                LTRIM(RTRIM(REPLACE(REPLACE(ISNULL(task_desc, N''), CHAR(13), CHAR(10)), CHAR(10), ' '))) AS task_desc
            FROM FNLAccount.dbo.DailyTasks
            WHERE username=? AND CAST(task_date AS DATE)=CAST(GETDATE() AS DATE)
            ORDER BY id
        """, (username,))
        rows = cur.fetchall()

        out = []
        for r in rows:
            status = "done" if r[3] == 1 else "not_done"
            out.append({
                "id": r[0],
                "name": r[1],
                "reward": r[2],
                "status": status,
                "desc": r[4]
            })

        return jsonify({"success": True, "data": out})

    except Exception as e:
        print("daily_tasks error:", e)
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()

@app.post("/daily_claim")
def daily_claim():
    data = request.json or {}
    username = data.get("username")
    task_id = data.get("task_id")

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'DB failed'}), 500

    try:
        cur = conn.cursor()

        # Проверяем можно ли получить награду
        cur.execute("""
            SELECT is_done, reward_name 
            FROM FNLAccount.dbo.DailyTasks
            WHERE id=? AND username=? 
              AND CAST(task_date AS DATE)=CAST(GETDATE() AS DATE)
        """, (task_id, username))
        row = cur.fetchone()

        if not row:
            return jsonify({'success': False, 'error': 'Задание не найдено'}), 404
        if row[0] == 0:
            return jsonify({'success': False, 'error': 'Задание не выполнено'}), 400

        reward_name = row[1] or "Награда"

        # Получаем mUserNo
        cur.execute("SELECT mUserNo FROM FNLAccount.dbo.TblUser WHERE mUserId=?", (username,))
        user_row = cur.fetchone()
        if not user_row:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        mUserNo = user_row[0]

        # Добавляем награду в TblSysOrderList
        cur.execute("""
            INSERT INTO FNLBilling.dbo.TblSysOrderList (
                mRegDate, mSysID, mUserNo, mSvrNo, mItemID, mCnt,
                mAvailablePeriod, mPracticalPeriod, mStatus, mLimitedDate, ItemName
            )
            VALUES (
                GETDATE(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, (
            777,          # mSysID
            mUserNo,      # mUserNo
            777,          # mSvrNo
            409,          # mItemID (фиксирован)
            10000000,     # mCnt
            0, 0, 0,
            '2070-01-01',
            reward_name   # ItemName
        ))

        # Помечаем задание как полученное
        cur.execute("""
            UPDATE FNLAccount.dbo.DailyTasks
            SET is_done=2
            WHERE id=? AND username=? 
              AND CAST(task_date AS DATE)=CAST(GETDATE() AS DATE)
        """, (task_id, username))

        conn.commit()
        return jsonify({"success": True, "reward": reward_name})

    except Exception as e:
        conn.rollback()
        print("daily_claim error:", e)
        return jsonify({'success': False, 'error': str(e)}), 500

    finally:
        conn.close()

HAS_FTS = None

def check_fulltext_support(conn):
    global HAS_FTS
    if HAS_FTS is not None:
        return HAS_FTS
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*) 
            FROM sys.fulltext_indexes 
            WHERE object_id IN (
                OBJECT_ID('dbo.DT_Item'),
                OBJECT_ID('dbo.DT_Monster')
            )
        """)
        HAS_FTS = (cur.fetchone() or [0])[0] > 0
    except Exception:
        HAS_FTS = False
    return HAS_FTS


@app.get("/droplist")
def droplist():
    lang = request.args.get("lang", "Russian").capitalize()
    name = (request.args.get("iname", "") or "").strip()
    monster = (request.args.get("mname", "") or "").strip()
    place = (request.args.get("place", "") or "").strip()

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'DB connection failed'}), 500

    try:
        cur = conn.cursor()

        # --- Формируем имена локализованных столбцов ---
        # если язык Korean → добавляем KR, если Chinese → CN, иначе — без суффикса
        suffix = {"Korean": "KR", "Chinese": "CN"}.get(lang, "")
        item_col = f"i.iname{suffix}" if suffix else "i.iname"
        monster_col = f"m.mname{suffix}" if suffix else "m.mname"
        place_col = f"m.MonsterPlace{suffix}" if suffix else "m.MonsterPlace"

        # --- Основной SQL ---
        base_sql = f"""
            SELECT TOP 300
                di.DItem,
                {item_col} AS item_name,
                di.DNumber,
                {monster_col} AS monster_name,
                {place_col} AS place,
                di.dstatus
            FROM fnlparm.dbo.DT_DropGroup AS dg
            INNER JOIN fnlparm.dbo.DT_DropItem AS di ON dg.DDrop = di.DDrop
            INNER JOIN fnlparm.dbo.DT_Item AS i ON di.DItem = i.IID
            INNER JOIN fnlparm.dbo.DT_MonsterDrop AS md ON dg.DGroup = md.DGroup
            INNER JOIN fnlparm.dbo.DT_Monster AS m ON md.MID = m.MID
            WHERE di.dIsEvent = 0
        """

        # --- Фильтры поиска ---
        where = []
        params = []
        if name:
            where.append(f"{item_col} LIKE ?")
            params.append(f"%{name}%")
        if monster:
            where.append(f"{monster_col} LIKE ?")
            params.append(f"%{monster}%")
        if place:
            where.append(f"{place_col} LIKE ?")
            params.append(f"%{place}%")

        if where:
            sql = base_sql + " AND " + " AND ".join(where)
        else:
            sql = base_sql

        # --- Выполнение ---
        cur.execute(sql, params)
        rows = cur.fetchall()

        # --- Вывод ---
        out = [{
            "item_id": r[0],
            "item_name": r[1],
            "count": r[2],
            "monster_name": r[3],
            "place": r[4],
            "status": r[5],
        } for r in rows]

        return jsonify({"success": True, "data": out})

    except Exception as e:
        print("DB droplist error:", e)
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()


if __name__ == "__main__":
    # запустить: FLASK_APP=app.py flask run --host=0.0.0.0 --port=5000
    app.run(host="0.0.0.0", port=5000, debug=False)



