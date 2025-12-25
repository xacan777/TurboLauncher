"""
Reference implementation for the TURBO launcher backend.

This module keeps the legacy SQL snippets and example payloads that the
launcher relies on.  The Flask app (app.py) imports from here to avoid
duplicating strings and to ensure the documented behaviour stays in sync
with the running server.
"""

from datetime import datetime

# --- SQL templates ---------------------------------------------------------

# Authentication
SQL_CHECK_USER = "SELECT mUserId, mUserSuperPswd FROM TblUser WHERE mUserId=? AND mUserSuperPswd=?"
SQL_CHECK_EXISTS = "SELECT COUNT(*) FROM TblUser WHERE mUserId=?"
SQL_CREATE_USER = "INSERT INTO TblUser (mUserId, mUserSuperPswd, mUserPswd) VALUES (?, ?, ?)"
SQL_UPDATE_IP = "UPDATE TblUser SET mip=? WHERE mUserId=?"

# Leaderboards
SQL_LEADERBOARD_LEVELS = """
SELECT TOP 100
    c.charactersname,
    c.mlevel,
    c.{class_col}
FROM FNLGame.dbo.[fnlaccount.user를 통한 문자 레벨] AS c
WHERE c.charactersname IS NOT NULL
ORDER BY c.mlevel DESC
"""

SQL_LEADERBOARD_POWER = """
SELECT TOP 100
    mNm,
    SUM(CAST(Сила_предмета AS INT)) AS TotalPower,
    {class_col}
FROM fnlgame.dbo.power_pc
GROUP BY mNm, {class_col}
ORDER BY TotalPower DESC;
"""

# Enhancement
SQL_ENHANCEMENT_BASE = """
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

# Droplist
SQL_DROPLIST_BASE = """
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

# Forum
SQL_FORUM_TOPICS = """
SELECT id, title, author, created_at, updated_at, message_count, last_message_at
FROM ForumTopics
ORDER BY last_message_at DESC
"""

SQL_FORUM_MESSAGES = """
SELECT id, topic_id, author, text, created_at
FROM ForumMessages
ORDER BY created_at ASC
"""

SQL_FORUM_CREATE_TOPIC = """
INSERT INTO ForumTopics (title, author, created_at, updated_at, message_count, last_message_at)
VALUES (?, ?, GETDATE(), GETDATE(), 0, GETDATE());
SELECT SCOPE_IDENTITY();
"""

SQL_FORUM_CREATE_MESSAGE = """
INSERT INTO ForumMessages (topic_id, author, text, created_at)
VALUES (?, ?, ?, GETDATE())
"""

# --- Reference payloads ----------------------------------------------------

SAMPLE_NEWS = [
    {
        "title": "Добро пожаловать в TURBO",
        "body": "Обновленный лаунчер и новый форум уже здесь.",
        "image_url": "",
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
    },
    {
        "title": "Внимание к базе данных",
        "body": "Лидеры, дроп-лист и усиление доступны через новое API.",
        "image_url": "",
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
    },
]

SAMPLE_LEADERBOARD = [
    {"name": "Aster", "level": 95, "power": 125000, "class": "Guardian"},
    {"name": "Nex", "level": 92, "power": 119500, "class": "Mage"},
]

SAMPLE_DROPLIST = [
    {
        "item_id": 101,
        "item_name": "Священный меч",
        "count": 1,
        "monster_name": "Хранитель врат",
        "place": "Северный бастион",
        "status": 0,
    },
    {
        "item_id": 202,
        "item_name": "Зелье энергии",
        "count": 3,
        "monster_name": "Часовой",
        "place": "Долина драконов",
        "status": 0,
    },
]

SAMPLE_ENHANCEMENT = [
    {"item_id": 501, "iname": "Клинок бури", "scroll_name": "Свиток силы", "rsuccess": 0.35},
    {"item_id": 502, "iname": "Плащ ветра", "scroll_name": "Свиток защиты", "rsuccess": 0.42},
]

SAMPLE_FORUM = {
    "topics": [
        {
            "id": 1,
            "title": "Добро пожаловать",
            "author": "system",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "message_count": 1,
            "last_message_at": datetime.utcnow().isoformat(),
        }
    ],
    "messages": [
        {
            "id": 1,
            "topic_id": 1,
            "author": "system",
            "text": "Форум TURBO открыт. Делитесь идеями и багрепортами.",
            "created_at": datetime.utcnow().isoformat(),
        }
    ],
}
