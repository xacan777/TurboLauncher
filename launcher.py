import os
import json
import base64
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib

from api import API
from updater import Updater

USER_DATA_FILE = "user_data.json"
CONFIG_FILE = "config_launcher.json"
CLIENT_VERSION_FILE = "client_check_update.json"
# ---------- Мультиязычность ----------

LANG_TEXTS = {
    "Russian": {
        # --- Авторизация и интерфейс ---
        "auth_title": "FNL Launcher — Авторизация",
        "username": "Аккаунт:",
        "password": "Пароль:",
        "login": "Войти",
        "register": "Зарегистрироваться",
        "play": "Играть",
        "settings": "Настройки",
        "logout": "Выйти из аккаунта",
        "check_updates": "Проверить обновление",
        "server_status": "Сервер: неизвестно",
        "online": "В сети:",
        "news": "Новости",
        "leaders": "Таблица лидеров",
        "droplist": "Дроп-лист",
        "language": "Язык интерфейса:",
        "status_check": "Проверить обновление",
        "online_status": "🟢 Онлайн",
        "offline_status": "🔴 Офлайн",


        # --- Таблица лидеров ---
        "leader_name": "Имя",
        "leader_level": "Уровень",
        "leader_power": "Сила",
        "leader_class": "Класс",
        "leader_tab_levels": "По уровням",
        "leader_tab_power": "По силе",

        # --- Дроп-лист ---
        "drop_item": "Предмет",
        "drop_monster": "Монстр",
        "drop_place": "Локация",
        "drop_count": "Кол-во",
        "drop_status": "Статус",
        "drop_find": "Найти",

        # --- Усиление ---
        "enhancement": "Усиление предметов",
        "enh_item": "Предмет",
        "enh_rsuccess": "Шанс успеха",
        "enh_find": "Найти",
        "enh_scroll": "Свиток усиления",
        "enh_type": "Тип",

        # --- Ежедневные задания ---
        "daily_tasks": "Ежедневные задания",
        "task_name": "Задание",
        "task_reward": "Награда",
        "task_status": "Статус",
        "task_claim": "Забрать",
        "task_done": "✅ Выполнено",
        "task_not_done": "⏳ Не выполнено"
    },

    "Korean": {
        # --- Авторизация и интерфейс ---
        "auth_title": "FNL 런처 — 로그인",
        "username": "계정:",
        "password": "비밀번호:",
        "login": "로그인",
        "register": "회원가입",
        "play": "게임 시작",
        "settings": "설정",
        "logout": "로그아웃",
        "check_updates": "업데이트 확인",
        "server_status": "서버 상태: 알 수 없음",
        "online": "온라인:",
        "news": "뉴스",
        "leaders": "순위표",
        "droplist": "드롭 목록",
        "language": "언어 선택:",
        "status_check": "업데이트 확인",
        "online_status": "🟢 온라인",
        "offline_status": "🔴 오프라인",


        # --- Таблица лидеров ---
        "leader_name": "이름",
        "leader_level": "레벨",
        "leader_power": "전투력",
        "leader_class": "직업",
        "leader_tab_levels": "레벨 순위",
        "leader_tab_power": "전투력 순위",

        # --- Дроп-лист ---
        "drop_item": "아이템",
        "drop_monster": "몬스터",
        "drop_place": "지역",
        "drop_count": "수량",
        "drop_status": "상태",
        "drop_find": "검색",

        # --- Усиление ---
        "enhancement": "아이템 강화",
        "enh_item": "목",
        "enh_rsuccess": "성공 가능성",
        "enh_find": "찾다",
        "enh_scroll": "강화 주문서",
        "enh_type": "종류",

        # --- Ежедневные задания ---
        "daily_tasks": "일일 퀘스트",
        "task_name": "운동",
        "task_reward": "보상",
        "task_status": "상태",
        "task_claim": "가져가다",
        "task_done": "✅ 완료",
        "task_not_done": "⏳ 완료되지 않음"
    },
    "Chinese": {
        # --- Авторизация и интерфейс ---
        "auth_title": "FNL 启动器 — 登录",
        "username": "账号：",
        "password": "密码：",
        "login": "登录",
        "register": "注册",
        "play": "开始游戏",
        "settings": "设置",
        "logout": "退出登录",
        "check_updates": "检查更新",
        "server_status": "服务器状态：未知",
        "online": "在线的：",
        "news": "新闻",
        "leaders": "排行榜",
        "droplist": "掉落列表",
        "language": "界面语言：",
        "status_check": "检查更新",
        "online_status": "🟢 在线",
        "offline_status": "🔴 离线",

        # --- Таблица лидеров ---
        "leader_name": "名字",
        "leader_level": "等级",
        "leader_power": "战斗力",
        "leader_class": "职业",
        "leader_tab_levels": "按等级",
        "leader_tab_power": "按战力",

        # --- Дроп-лист ---
        "drop_item": "物品",
        "drop_monster": "怪物",
        "drop_place": "地点",
        "drop_count": "数量",
        "drop_status": "状态",
        "drop_find": "查找",

        # --- Усиление ---
        "enhancement": "物品强化",
        "enh_item": "物品",
        "enh_rsuccess": "成功的机会",
        "enh_find": "寻找",
        "enh_scroll": "强化卷轴",
        "enh_type": "类型",

        # --- Ежедневные задания ---
        "daily_tasks": "未完成",
        "task_name": "锻炼",
        "task_reward": "报酬",
        "task_status": "地位",
        "task_claim": "拿",
        "task_done": "✅ 完毕",
        "task_not_done": "⏳ 未完成"
    }
}


# ---------- Утилиты ----------

def get_lang():
    return load_json(CONFIG_FILE, {"language": "Russian"}).get("language", "Russian")

def set_lang(new_lang):
    cfg = load_json(CONFIG_FILE, {"language": "Russian"})
    cfg["language"] = new_lang
    save_json(CONFIG_FILE, cfg)

def load_json(path, default):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, ensure_ascii=False, indent=2)
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_config():
    return load_json(CONFIG_FILE, {"language": "Russian", "api_url": "http://188.124.37.192:5000"})


def remember_success(username, password):
    data = load_json(USER_DATA_FILE, {"last_accounts": []})
    existing = next((x for x in data["last_accounts"] if x["username"] == username), None)
    if existing:
        existing["password"] = password
    else:
        data["last_accounts"].insert(0, {"username": username, "password": password})
        data["last_accounts"] = data["last_accounts"][:10]
    save_json(USER_DATA_FILE, data)

def play(username, password):
    encoded_username = base64.b64encode(username.encode()).decode()
    config = load_config()

    if config.get('language') == 'Korean':
        exe = "FinalKR.exe"
    elif config.get('language') == 'Chinese':
        exe = "FinalCN.exe"
    else:
        exe = "FinalRU.exe"

    command = f'{exe} "P=&H1=&H2=MTEwMDQ=&P0={encoded_username}&P1=Q19SMg==&P2=NDYxMg==&P3=&P4={password}&P5=&PC1=Tg==&PC2=Tg=="'

    try:
        subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить игру: {e}")

def open_settings():
    try:
        subprocess.Popen(["R2Option.exe"], creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось открыть настройки: {e}")


# ---------- Маскирование логина ----------
def mask_username_deterministic(name: str) -> str:
    n = len(name)
    if n <= 1:
        return name
    name_list = list(name)
    if n <= 3:
        for i in range(1, n):
            name_list[i] = '*'
    elif 4 <= n <= 5:
        mid = n // 2
        name_list[mid] = '*'
    elif 6 <= n <= 8:
        for i in [2, n - 3]:
            if 0 <= i < n:
                name_list[i] = '*'
    elif 9 <= n <= 12:
        for i in [2, 4, n - 3]:
            if 0 <= i < n:
                name_list[i] = '*'
    else:
        for i in [2, 5, 7, n - 4]:
            if 0 <= i < n:
                name_list[i] = '*'
    return ''.join(name_list)


# ============================================================
# =============  ГЛАВНОЕ ОКНО (Авторизация)  =================
# ============================================================

class LauncherGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.api = API(CONFIG_FILE)
        self.language = get_lang()
        self.txt = LANG_TEXTS[self.language]

        self.title(self.txt["auth_title"])
        self.geometry("900x620")

        self._build_tab_login()

    def _build_tab_login(self):
        for w in self.winfo_children():
            w.destroy()

        self.txt = LANG_TEXTS[self.language]
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text=self.txt["username"]).grid(row=0, column=0, sticky="w")
        self.ent_user = ttk.Entry(frame, width=30)
        self.ent_user.grid(row=0, column=1, padx=5)

        ttk.Label(frame, text=self.txt["password"]).grid(row=1, column=0, sticky="w")
        self.ent_pass = ttk.Entry(frame, show="*", width=30)
        self.ent_pass.grid(row=1, column=1, padx=5)

        btns = ttk.Frame(frame)
        btns.grid(row=2, column=0, columnspan=3, pady=10, sticky="w")

        ttk.Button(btns, text=self.txt["login"], command=self.do_login).pack(side="left", padx=5)
        ttk.Button(btns, text=self.txt["register"], command=self.do_register).pack(side="left", padx=5)

        # выбор языка
        ttk.Label(frame, text=self.txt["language"]).grid(row=4, column=0, sticky="w", pady=(15, 0))
        self.lang_var = tk.StringVar(value=self.language)
        combo = ttk.Combobox(frame, textvariable=self.lang_var, values=["Russian", "Korean", "Chinese"], width=10, state="readonly")
        combo.grid(row=4, column=1, sticky="w", pady=(15, 0))
        combo.bind("<<ComboboxSelected>>", lambda e: self.change_language())

        # сохранённые аккаунты
        self.account_frame = ttk.Frame(frame)
        self.account_frame.grid(row=5, column=0, columnspan=3, sticky="we", pady=(10, 0))
        canvas = tk.Canvas(self.account_frame, height=60)
        hscroll = ttk.Scrollbar(self.account_frame, orient="horizontal", command=canvas.xview)
        self.scroll_accounts = ttk.Frame(canvas)
        self.scroll_accounts.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scroll_accounts, anchor="nw")
        canvas.configure(xscrollcommand=hscroll.set)
        canvas.pack(fill="x", expand=True)
        hscroll.pack(fill="x")
        self.refresh_saved_accounts()

    def change_language(self):
        """Смена языка только для окна авторизации"""
        self.language = self.lang_var.get()
        set_lang(self.language)
        self.txt = LANG_TEXTS[self.language]
        self._build_tab_login()  # просто перерисовать форму логина

    def refresh_saved_accounts(self):
        for w in self.scroll_accounts.winfo_children():
            w.destroy()
        data = load_json(USER_DATA_FILE, {"last_accounts": []})
        for acc in data["last_accounts"]:
            masked = mask_username_deterministic(acc["username"])
            ttk.Button(self.scroll_accounts, text=masked, width=16,
                       command=lambda a=acc: self._select_account(a)).pack(side="left", padx=4, pady=6)

    def _select_account(self, acc):
        self.ent_user.delete(0, tk.END)
        self.ent_user.insert(0, acc["username"])
        self.ent_pass.delete(0, tk.END)
        self.ent_pass.insert(0, acc["password"])

    def do_login(self):
        u = self.ent_user.get().strip()
        p = self.ent_pass.get().strip()
        if not u or not p:
            messagebox.showwarning("Внимание", "Введите логин и пароль")
            return

        resp, code = self.api.login(u, p)
        if resp.get("success"):
            remember_success(u, p)
            # --- сохраняем позицию ---
            x, y = self.winfo_x(), self.winfo_y()
            self.destroy()
            win = MainLauncherWindow(None, u, p, x, y)
            win.mainloop()
        else:
            messagebox.showerror("Ошибка", resp.get("error", f"HTTP {code}"))

    def do_register(self):
        u = self.ent_user.get().strip()
        p = self.ent_pass.get().strip()
        if not u or not p:
            messagebox.showwarning("Внимание", "Введите логин и пароль")
            return
        resp, code = self.api.register(u, p)
        if resp.get("success"):
            remember_success(u, p)
            messagebox.showinfo("Успех", "Регистрация выполнена")
            self.refresh_saved_accounts()
        else:
            messagebox.showerror("Ошибка", resp.get("error", f"HTTP {code}"))


# ============================================================
# ========  ОКНО ПОСЛЕ УСПЕШНОЙ АВТОРИЗАЦИИ (Toplevel)  =====
# ============================================================

class MainLauncherWindow(tk.Tk):
    def __init__(self, parent, username, password, pos_x=None, pos_y=None):
        super().__init__(parent)
        self.geometry("900x620" + (f"+{pos_x}+{pos_y}" if pos_x is not None else ""))
        self.lift()
        self.focus_force()
        self.attributes("-topmost", True)
        self.after(200, lambda: self.attributes("-topmost", False))

        self.parent = parent
        self.username = username
        self.password = password
        self.api = API(CONFIG_FILE)
        self.updater = Updater(CLIENT_VERSION_FILE)
        self.language = get_lang()
        self.txt = LANG_TEXTS[self.language]

        self.title("ASH Launcher")
        self.geometry("900x620")

        # === Notebook ===
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=6, pady=6)

        # Карта вкладок
        self.tab_frames = {}
        for key in ["Главное", "Новости", "Таблица лидеров", "Дроп-лист", "Усиление предметов", "Ежедневные задания"]:
            frame = ttk.Frame(self.notebook)
            if key == "Усиление предметов":
                text_key = "enhancement"
            else:
                text_key = self._tab_name_to_key(key)
            self.notebook.add(frame, text=self.txt.get(text_key, key))
            self.tab_frames[key] = frame

        # Состояние
        self._tab_inited = {k: False for k in self.tab_frames}
        self.has_new_daily_task = False
        self.daily_alert_visible = False
        self._refresh_handles = {}

        # Инициализируем вкладку Главное
        self._build_tab_main_controls(self.tab_frames["Главное"])
        self._tab_inited["Главное"] = True
        self.update_server_status()  # статус сразу активен

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)
        print("[DEBUG] MainLauncherWindow готово")
    def _flash_daily_tab(self):
        """Мигающая подсветка вкладки Ежедневные задания."""
        import itertools
        self._flash_cycle = itertools.cycle(["#ff6666", "#ff0000"])

        def flash():
            if not self.has_new_daily_task:
                # сброс
                for i in range(self.notebook.index("end")):
                    if self.notebook.tab(i, "text") in ("Ежедневные задания", "일일 퀘스트", "未完成"):
                        self.notebook.tab(i, background="")
                        break
                return

            color = next(self._flash_cycle)
            for i in range(self.notebook.index("end")):
                if self.notebook.tab(i, "text") in ("Ежедневные задания", "일일 퀘스트", "未完成"):
                    self.notebook.tab(i, background=color)
                    break

            self.after(600, flash)

        flash()

    def _play_sound(self):
        """Проигрывает короткий звуковой сигнал."""
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        except Exception:
            pass

    def short_text(text: str, limit=50):
        """Однострочный вариант текста без переносов"""
        if not text:
            return ""
        clean = text.replace("\r", " ").replace("\n", " ")
        clean = " ".join(clean.split())
        return clean[:limit] + ("…" if len(clean) > limit else "")


    def claim_daily(self, win):
        try:
            resp = self.api.post("daily_reward", {"username": self.username})
            if resp.get("success"):
                messagebox.showinfo("Награда", "Награда успешно получена!")
                win.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    # ---------- Табличное имя вкладки ----------
    def _tab_name_to_key(self, key):
        mapping = {
            "Главное": "play",
            "Новости": "news",
            "Таблица лидеров": "leaders",
            "Дроп-лист": "droplist"
        }
        return mapping.get(key, key)

    # ---------- Смена языка ----------
    def change_language(self):
        """Меняет язык лаунчера и обновляет интерфейс полностью"""
        new_lang = self.lang_var.get()
        set_lang(new_lang)
        self.language = new_lang
        self.txt = LANG_TEXTS[new_lang]

        # Обновляем заголовки вкладок
        self.notebook.tab(0, text=self.txt["play"])
        self.notebook.tab(1, text=self.txt["news"])
        self.notebook.tab(2, text=self.txt["leaders"])
        self.notebook.tab(3, text=self.txt["droplist"])

        # Пересоздаём вкладки
        for name, frame in self.tab_frames.items():
            for child in frame.winfo_children():
                child.destroy()

        self._build_tab_main_controls(self.tab_frames["Главное"])
        self._build_tab_news(self.tab_frames["Новости"])
        self._build_tab_leaderboard(self.tab_frames["Таблица лидеров"])
        self._build_tab_droplist(self.tab_frames["Дроп-лист"])

    # ---------- Главное ----------
    def _build_tab_main_controls(self, tab):
        txt = self.txt

        # ---- Статус сервера ----
        status_frame = ttk.Frame(tab)
        status_frame.pack(pady=(10, 5), anchor="w")

        self.server_status_lbl = ttk.Label(status_frame, text=txt["server_status"], font=("Arial", 11, "bold"))
        self.server_status_lbl.pack(side="left", padx=6)
        self.online_lbl = ttk.Label(status_frame, text=txt["online"], font=("Arial", 11))
        self.online_lbl.pack(side="left", padx=20)

        # ---- Кнопки ----
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text=txt["play"], command=lambda: play(self.username, self.password)).pack(side="left", padx=8)
        ttk.Button(btn_frame, text=txt["settings"], command=open_settings).pack(side="left", padx=8)
        ttk.Button(btn_frame, text=txt["logout"], command=self.logout).pack(side="left", padx=8)

        # ---- Селектор языка ----
        lang_frame = ttk.Frame(tab)
        lang_frame.pack(pady=(10, 5))
        ttk.Label(lang_frame, text=txt["language"]).pack(side="left", padx=5)
        self.lang_var = tk.StringVar(value=self.language)
        combo = ttk.Combobox(lang_frame, textvariable=self.lang_var,
                             values=["Russian", "Korean", "Chinese"],
                             width=10, state="readonly")
        combo.pack(side="left")
        combo.bind("<<ComboboxSelected>>", lambda e: self.change_language())
        social_frame = ttk.Frame(tab)
        social_frame.pack(side="bottom", pady=10)

        ttk.Button(social_frame, text="Discord", command=lambda: os.startfile("https://discord.gg/bJmBcrz23j")).pack(
            side="left", padx=4)
        ttk.Button(social_frame, text="Telegram", command=lambda: os.startfile("t.me/ashschi")).pack(side="left",
                                                                                                          padx=4)
        ttk.Button(social_frame, text="Донат", command=lambda: os.startfile("not yet")).pack(side="left",
                                                                                                         padx=4)

        # ---- Индикатор обновления ----
        self.lbl_status = ttk.Label(tab, text="")
        self.lbl_status.pack(anchor="w", padx=12)
        self.pb = ttk.Progressbar(tab, orient="horizontal", mode="determinate", length=520)
        self.pb.pack(padx=12, pady=8)

        ttk.Button(tab, text=txt["check_updates"], command=self.check_updates).pack(pady=10)

        ttk.Button(tab, text="Проверить клиент", command=self.check_client_integrity).pack(pady=4)

    def check_client_integrity(self):
        version_info = self.api.get("version")
        broken = []

        for f in version_info.get("files", []):
            path = os.path.join(f["folder"], f["name"])
            if not os.path.exists(path):
                broken.append(f["name"])
                continue
            with open(path, "rb") as file:
                data = file.read()
            h = hashlib.md5(data).hexdigest()
            if "hash" in f and f["hash"] != h:
                broken.append(f["name"])

        if broken:
            msg = "Повреждены файлы:\n" + "\n".join(broken)
            if messagebox.askyesno("Повреждение", msg + "\nПерезагрузить файлы?"):
                todo = [f for f in version_info["files"] if f["name"] in broken]
                self.updater.update_files(todo, lambda *a: None, lambda *a: None)
        else:
            messagebox.showinfo("Проверка", "Все файлы целы ✅")

    # ---------- Переключение вкладок ----------
    def _on_tab_change(self, event):
        name = list(self.tab_frames.keys())[self.notebook.index(self.notebook.select())]
        if not self._tab_inited[name]:
            print(f"[DEBUG] Инициализация вкладки: {name}")
            if name == "Новости":
                self._build_tab_news(self.tab_frames[name])
                self._schedule_refresh(name, self.refresh_news, 5000)
            elif name == "Таблица лидеров":
                self._build_tab_leaderboard(self.tab_frames[name])
                self._schedule_refresh(name, self.load_leader_data, 5000)
            elif name == "Дроп-лист":
                self._build_tab_droplist(self.tab_frames[name])
            elif name == "Усиление предметов":
                self._build_tab_enhancement(self.tab_frames[name])
            elif name == "Ежедневные задания":
                self._build_tab_daily_tasks(self.tab_frames[name])
                self.has_new_daily_task = False

        self._tab_inited[name] = True

    def _build_tab_daily_tasks(self, tab):
        txt = self.txt

        ttk.Label(tab, text="Ежедневные задания", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(8, 2))

        frame = ttk.Frame(tab)
        frame.pack(fill="both", expand=True, padx=10, pady=8)

        style = ttk.Style(tab)
        style.configure("Tasks.Treeview", rowheight=24)

        y_scroll = ttk.Scrollbar(frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        self.task_tree = ttk.Treeview(
            frame,
            columns=("id", "name", "reward", "status"),
            show="headings",
            yscrollcommand=y_scroll.set,
            selectmode="browse",
            height=18,
            style="Tasks.Treeview"
        )
        y_scroll.config(command=self.task_tree.yview)

        self.task_tree.heading("name", text="Задание")
        self.task_tree.heading("reward", text="Награда")
        self.task_tree.heading("status", text="Статус")
        self.task_tree.heading("id", text="ID")

        self.task_tree.column("id", width=0, stretch=False)
        self.task_tree.column("name", width=320, anchor="w")
        self.task_tree.column("reward", width=250, anchor="center")
        self.task_tree.column("status", width=150, anchor="center")

        self.task_tree.pack(fill="both", expand=True)

        self.task_descs = {}



        def load_tasks():
            def worker():
                data = self.api.get(f"daily_tasks?username={self.username}") or {}
                rows = data.get("data", [])
                # до этого уже есть rows = data.get("data", [])
                new_done = any(r["status"] == "done" for r in rows)

                if any(r["status"] == "done" for r in rows):
                    self.after_idle(lambda: self._play_sound())

                def ui():
                    self.task_tree.delete(*self.task_tree.get_children())
                    self.task_descs.clear()

                    for r in rows:
                        status_text = "🎁 Получить" if r["status"] == "done" else "⏳ Не выполнено"
                        iid = self.task_tree.insert(
                            "",
                            "end",
                            values=(r["id"], r["name"], r["reward"], status_text)
                        )
                        self.task_descs[str(r["id"])] = r.get("desc", "Описание отсутствует")

                    # 🔔 Проверяем, появились ли задания для получения
                    if any(r["status"] == "done" for r in rows):
                        self._play_sound()

                    # Автообновление каждые 5 сек
                    self.after(5000, load_tasks)

                self.after_idle(ui)

            threading.Thread(target=worker, daemon=True).start()

        def show_popup(title, content):
            popup = tk.Toplevel(self)
            popup.title(title)
            popup.transient(self)
            popup.configure(padx=10, pady=10)

            frm = ttk.Frame(popup)
            frm.pack(fill="both", expand=True)

            ttk.Label(frm, text=title, font=("Arial", 11, "bold")).pack(anchor="center", pady=(0, 6))

            text_frame = ttk.Frame(frm)
            text_frame.pack(fill="both", expand=True)

            txt = tk.Text(text_frame, wrap="word", height=10)
            vsb = ttk.Scrollbar(text_frame, orient="vertical", command=txt.yview)
            txt.configure(yscrollcommand=vsb.set)
            txt.pack(side="left", fill="both", expand=True)
            vsb.pack(side="right", fill="y")

            txt.insert("1.0", content)
            txt.config(state="disabled")

            ttk.Button(frm, text="Закрыть", command=popup.destroy).pack(pady=6)

            popup.update_idletasks()
            w = min(700, max(360, popup.winfo_reqwidth()))
            h = min(500, max(200, popup.winfo_reqheight()))

            x = max(0, min(self.winfo_pointerx() - w // 2, self.winfo_screenwidth() - w))
            y = max(0, min(self.winfo_pointery() - 50, self.winfo_screenheight() - h))
            popup.geometry(f"{w}x{h}+{x}+{y}")

        def claim_reward(task_id):
            def worker():
                res = self.api.post("daily_claim", {"username": self.username, "task_id": task_id})
                if res and res.get("success"):
                    messagebox.showinfo("Награда", "🎉 Награда успешно получена!")
                    load_tasks()
                else:
                    messagebox.showwarning("Ошибка", res.get("error", "Не удалось получить награду."))

            threading.Thread(target=worker, daemon=True).start()

        def on_click(event):
            item = self.task_tree.identify_row(event.y)
            col = self.task_tree.identify_column(event.x)
            if not item:
                return

            col_index = int(col.replace("#", ""))
            values = self.task_tree.item(item, "values")
            if not values:
                return

            # values = (id, name, reward, status) — всё строки
            task_id_str, name, reward, status = values

            # описание берём по строковому ключу
            full_desc = self.task_descs.get(task_id_str, "Описание отсутствует")

            # клик по колонке "Награда" -> показать описание
            if col_index == 3:
                show_popup(name, full_desc)
                return

            # клик по "Статус" -> получить награду (если доступно)
            if col_index == 4 and "Получить" in status:
                claim_reward(int(task_id_str))  # можно и без int

        self.task_tree.bind("<Button-1>", on_click)

        load_tasks()

    def _schedule_refresh(self, name, fn, interval_ms):
        def tick():
            try:
                fn()
            finally:
                self._refresh_handles[name] = self.after(interval_ms, tick)
        self._refresh_handles[name] = self.after(interval_ms, tick)

    # ---------- Статус сервера ----------
    def update_server_status(self):
        def worker():
            data = self.api.get("server/status") or {}
            online = data.get("online", False)
            players = data.get("players", 0)

            def ui():
                if online:
                    self.server_status_lbl.config(
                        text=self.txt["online_status"], foreground="#00ff66"
                    )
                    self.online_lbl.config(text=f"{self.txt['online']} {players}")
                else:
                    self.server_status_lbl.config(
                        text=self.txt["offline_status"], foreground="red"
                    )
                    self.online_lbl.config(text=f"{self.txt['online']} 0")

            self.after_idle(ui)

        threading.Thread(target=worker, daemon=True).start()
        self.after(5000, self.update_server_status)

    def logout(self):
        self.destroy()
        os._exit(0)

    # ---------- Остальные вкладки (без изменений) ----------
    # сюда оставь твои _build_tab_news, _build_tab_leaderboard, _build_tab_droplist и check_updates как были
    def get_lang_column(base_name):
        """
        Возвращает имя столбца для текущего языка.
        Например:
          get_lang_column("ClassName") -> ClassNameKR или ClassNameCN
        """
        lang = get_lang()
        suffix = {"Russian": "", "Korean": "KR", "Chinese": "CN"}.get(lang, "")
        return f"{base_name}{suffix}" if suffix else base_name

    # ------------------- Новости (как было, но в переданный tab) -------------------
    def _build_tab_news(self, tab):
        self.news_text = tk.Text(tab, state="disabled", wrap="word")
        self.news_text.pack(fill="both", expand=True, padx=8, pady=8)
        self.refresh_news()  # первичная загрузка

    def refresh_news(self):
        if not hasattr(self, "news_text"):
            return
        def worker():
            try:
                news = self.api.get_news()
            except Exception:
                news = []
            def ui():
                self.news_text.configure(state="normal")
                self.news_text.delete("1.0", tk.END)
                for item in news:
                    self.news_text.insert(tk.END, f"{item.get('date','')}: {item.get('title','')}\n")
                    self.news_text.insert(tk.END, f"{item.get('body','')}\n\n")
                self.news_text.configure(state="disabled")
            self.after_idle(ui)

        threading.Thread(target=worker, daemon=True).start()

    # ------------------- Таблица лидеров (как было, в переданный tab) -------------------
    def _build_tab_leaderboard(self, tab):
        txt = self.txt

        style = ttk.Style(tab)
        style.configure("Leader.TNotebook.Tab", padding=(12, 6))
        style.map("Leader.TNotebook.Tab",
                  background=[("selected", "#e6f0ff"), ("!selected", "#f7f7f7")])

        inner = ttk.Notebook(tab, style="Leader.TNotebook")
        inner.pack(fill="both", expand=True, padx=8, pady=8)

        # === Вкладка "По уровням" ===
        frm_levels = ttk.Frame(inner)
        inner.add(frm_levels, text=txt["leader_level"])

        frame_levels = ttk.Frame(frm_levels)
        frame_levels.pack(fill="both", expand=True, padx=6, pady=6)

        y_scroll_lvl = ttk.Scrollbar(frame_levels, orient="vertical")
        y_scroll_lvl.pack(side="right", fill="y")
        x_scroll_lvl = ttk.Scrollbar(frame_levels, orient="horizontal")
        x_scroll_lvl.pack(side="bottom", fill="x")

        self.tree_levels = ttk.Treeview(
            frame_levels,
            columns=("name", "level", "class"),
            show="headings",
            yscrollcommand=y_scroll_lvl.set,
            xscrollcommand=x_scroll_lvl.set
        )
        self.tree_levels.pack(fill="both", expand=True)
        y_scroll_lvl.config(command=self.tree_levels.yview)
        x_scroll_lvl.config(command=self.tree_levels.xview)

        # Заголовки для таблицы уровней
        self.tree_levels.heading("name", text=txt["leader_name"])
        self.tree_levels.heading("level", text=txt["leader_level"])
        self.tree_levels.heading("class", text=txt["leader_class"])

        self.tree_levels.column("name", width=280)
        self.tree_levels.column("level", width=120, anchor="center")
        self.tree_levels.column("class", width=180)

        # === Вкладка "По силе" ===
        frm_power = ttk.Frame(inner)
        inner.add(frm_power, text=txt["leader_power"])

        frame_power = ttk.Frame(frm_power)
        frame_power.pack(fill="both", expand=True, padx=6, pady=6)

        y_scroll_pow = ttk.Scrollbar(frame_power, orient="vertical")
        y_scroll_pow.pack(side="right", fill="y")
        x_scroll_pow = ttk.Scrollbar(frame_power, orient="horizontal")
        x_scroll_pow.pack(side="bottom", fill="x")

        self.tree_power = ttk.Treeview(
            frame_power,
            columns=("name", "power", "class"),
            show="headings",
            yscrollcommand=y_scroll_pow.set,
            xscrollcommand=x_scroll_pow.set
        )
        self.tree_power.pack(fill="both", expand=True)
        y_scroll_pow.config(command=self.tree_power.yview)
        x_scroll_pow.config(command=self.tree_power.xview)

        # Заголовки для таблицы силы
        self.tree_power.heading("name", text=txt["leader_name"])
        self.tree_power.heading("power", text=txt["leader_power"])
        self.tree_power.heading("class", text=txt["leader_class"])

        self.tree_power.column("name", width=280)
        self.tree_power.column("power", width=120, anchor="center")
        self.tree_power.column("class", width=180)

        # --- первичная загрузка ---
        self.load_leader_data()

    def load_leader_data(self):
        if not hasattr(self, "tree_levels") or not hasattr(self, "tree_power"):
            return

        def worker_levels():
            lang = get_lang()
            data = self.api.get(f"leaderboard/levels?lang={lang}") or {}
            rows = data.get("data", [])
            def ui():
                if not hasattr(self, "tree_levels"):
                    return
                self.tree_levels.delete(*self.tree_levels.get_children())
                for r in rows:
                    self.tree_levels.insert("", "end", values=(r["name"], r["level"], r["class"]))
            self.after(0, ui)

        def worker_power():
            lang = get_lang()
            data = self.api.get(f"leaderboard/power?lang={lang}") or {}
            rows = data.get("data", [])
            def ui():
                if not hasattr(self, "tree_power"):
                    return
                self.tree_power.delete(*self.tree_power.get_children())
                for r in rows:
                    self.tree_power.insert("", "end", values=(r["name"], r["power"], r["class"]))
            self.after(0, ui)

        threading.Thread(target=worker_levels, daemon=True).start()
        threading.Thread(target=worker_power, daemon=True).start()

    # ------------------- Дроп-лист (как было, в переданный tab) -------------------
    def _build_tab_droplist(self, tab):
        txt = self.txt
        filter_frame = ttk.Frame(tab)
        filter_frame.pack(fill="x", padx=10, pady=6)

        ttk.Label(filter_frame, text=f"{txt['drop_item']}:").grid(row=0, column=0, sticky="w")
        iname_entry = ttk.Entry(filter_frame, width=24)
        iname_entry.grid(row=0, column=1, padx=6)

        ttk.Label(filter_frame, text=f"{txt['drop_monster']}:").grid(row=0, column=2, sticky="w")
        mname_entry = ttk.Entry(filter_frame, width=24)
        mname_entry.grid(row=0, column=3, padx=6)

        ttk.Label(filter_frame, text=f"{txt['drop_place']}:").grid(row=0, column=4, sticky="w")
        place_entry = ttk.Entry(filter_frame, width=24)
        place_entry.grid(row=0, column=5, padx=6)

        # Кнопка поиска
        btn_search = ttk.Button(filter_frame, text=f"🔍 {txt['drop_find']}")
        btn_search.grid(row=0, column=6, padx=10)

        def bind_hotkeys(ent):
            """
            Горячие клавиши (Ctrl+C/V/X/A) работают независимо от раскладки.
            """

            def on_ctrl_key(event):
                # keycode одинаковый при любой раскладке:
                # A=65, C=67, V=86, X=88
                code = event.keycode

                # Ctrl+A — выделить всё
                if code == 65:
                    ent.select_range(0, 'end')
                    return "break"

                # Ctrl+C — копировать
                elif code == 67:
                    try:
                        self.clipboard_clear()
                        self.clipboard_append(ent.selection_get())
                    except tk.TclError:
                        pass
                    return "break"

                # Ctrl+V — вставить
                elif code == 86:
                    try:
                        ent.insert('insert', self.clipboard_get())
                    except tk.TclError:
                        pass
                    return "break"

                # Ctrl+X — вырезать
                elif code == 88:
                    try:
                        self.clipboard_clear()
                        self.clipboard_append(ent.selection_get())
                        ent.delete("sel.first", "sel.last")
                    except tk.TclError:
                        pass
                    return "break"

            ent.bind("<Control-Key>", on_ctrl_key)
            ent.bind("<Return>", lambda e: refresh_table())

        for entry in (iname_entry, mname_entry, place_entry):
            bind_hotkeys(entry)

        # === ТАБЛИЦА РЕЗУЛЬТАТОВ ===
        frame_table = ttk.Frame(tab)
        frame_table.pack(fill="both", expand=True, padx=10, pady=(4, 10))

        y_scroll = ttk.Scrollbar(frame_table, orient="vertical")
        y_scroll.pack(side="right", fill="y")
        x_scroll = ttk.Scrollbar(frame_table, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        self.drop_tree = ttk.Treeview(
            frame_table,
            columns=("id", "iname", "count", "monster", "place", "status"),
            show="headings",
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set,
            selectmode="browse",
            height=20
        )
        y_scroll.config(command=self.drop_tree.yview)
        x_scroll.config(command=self.drop_tree.xview)

        txt = self.txt
        headers = [
            ("id", "ID", 80),
            ("iname", txt["drop_item"], 200),
            ("count", txt["drop_count"], 90),
            ("monster", txt["drop_monster"], 200),
            ("place", txt["drop_place"], 180),
            ("status", txt["drop_status"], 90)
        ]

        for key, title, width in headers:
            self.drop_tree.heading(key, text=title)
            self.drop_tree.column(key, width=width, anchor="center")

        self.drop_tree.pack(fill="both", expand=True)

        # Подсветка при наведении (если включена тема)
        if hasattr(self.master, "treeview_hover"):
            self.master.treeview_hover(self.drop_tree)

        # === ФУНКЦИЯ ОБНОВЛЕНИЯ ===
        def refresh_table():
            iname = iname_entry.get().strip()
            mname = mname_entry.get().strip()
            place = place_entry.get().strip()
            lang = get_lang()

            def worker():
                params = f"droplist?iname={iname}&mname={mname}&place={place}&lang={lang}"
                data = self.api.get(params) or {}
                rows = data.get("data", [])

                def ui():
                    if not hasattr(self, "drop_tree"):
                        return
                    self.drop_tree.delete(*self.drop_tree.get_children())
                    for r in rows:
                        self.drop_tree.insert("", "end", values=(
                            r.get("item_id", ""),
                            r.get("item_name", ""),
                            r.get("count", ""),
                            r.get("monster_name", ""),
                            r.get("place", ""),
                            r.get("status", "")
                        ))

                self.after_idle(ui)

            threading.Thread(target=worker, daemon=True).start()

        self._droplist_refresh_callback = refresh_table

        btn_search.configure(command=refresh_table)
        refresh_table()  # первичная загрузка

    def _build_tab_enhancement(self, tab):
        txt = self.txt
        filter_frame = ttk.Frame(tab)
        filter_frame.pack(fill="x", padx=10, pady=6)

        # === Поле поиска ===
        ttk.Label(filter_frame, text=f"{txt['enh_item']}:").grid(row=0, column=0, sticky="w")
        iname_entry = ttk.Entry(filter_frame, width=30)
        iname_entry.grid(row=0, column=1, padx=6)

        # === Фильтр по типу ===
        ttk.Label(filter_frame, text=txt["enh_type"]).grid(row=0, column=2, sticky="w", padx=(10, 0))

        # 🔹 Локализованные значения списка
        type_labels = {
            "Russian": ["Все", "Оружие", "Доспехи"],
            "Korean": ["전체", "무기", "방어구"],
            "Chinese": ["全部", "武器", "防具"],
        }.get(self.language, ["Все", "Оружие", "Доспехи"])

        type_var = tk.StringVar(value=type_labels[0])
        type_box = ttk.Combobox(
            filter_frame,
            textvariable=type_var,
            values=type_labels,
            state="readonly",
            width=10
        )
        type_box.grid(row=0, column=3, padx=5)

        # чтобы "значение по умолчанию" сразу было видно даже без наведения
        type_box.set(type_labels[0])

        # === Кнопка поиска ===
        btn_search = ttk.Button(filter_frame, text=f"🔍 {txt['enh_find']}")
        btn_search.grid(row=0, column=4, padx=10)

        # === Таблица ===
        frame_table = ttk.Frame(tab)
        frame_table.pack(fill="both", expand=True, padx=10, pady=(4, 10))

        y_scroll = ttk.Scrollbar(frame_table, orient="vertical")
        y_scroll.pack(side="right", fill="y")
        x_scroll = ttk.Scrollbar(frame_table, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        self.enh_tree = ttk.Treeview(
            frame_table,
            columns=("id", "iname", "scroll", "rsuccess"),
            show="headings",
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set,
            selectmode="browse",
            height=20
        )
        y_scroll.config(command=self.enh_tree.yview)
        x_scroll.config(command=self.enh_tree.xview)

        headers = [
            ("id", "ID", 80),
            ("iname", txt["enh_item"], 240),
            ("scroll", txt["enh_scroll"], 220),
            ("rsuccess", txt["enh_rsuccess"], 100),
        ]

        for key, title, width in headers:
            self.enh_tree.heading(key, text=title)
            self.enh_tree.column(key, width=width, anchor="center")

        self.enh_tree.pack(fill="both", expand=True)

        if hasattr(self.master, "treeview_hover"):
            self.master.treeview_hover(self.enh_tree)

        # === Обновление таблицы ===
        def refresh_table():
            iname = iname_entry.get().strip()
            type_filter = type_var.get()
            lang = get_lang()
            selected_type = type_var.get()
            type_map = {
                "Все": "all", "Оружие": "weapon", "Доспехи": "defense",
                "전체": "all", "무기": "weapon", "방어구": "defense",
                "全部": "all", "武器": "weapon", "防具": "defense"
            }
            type_filter = type_map.get(selected_type, "all")

            params = f"enhancement?iname={iname}&lang={lang}&type={type_filter}"

            def worker():
                data = self.api.get(params) or {}
                rows = data.get("data", [])

                def ui():
                    if not hasattr(self, "enh_tree"):
                        return
                    self.enh_tree.delete(*self.enh_tree.get_children())
                    for r in rows:
                        self.enh_tree.insert(
                            "",
                            "end",
                            values=(
                                r.get("item_id", ""),
                                r.get("iname", ""),
                                r.get("scroll_name", ""),
                                f"{float(r.get('rsuccess', 0)):.2f}",
                            ),
                        )

                self.after_idle(ui)

            threading.Thread(target=worker, daemon=True).start()

        # === Горячие клавиши + Enter ===
        def bind_hotkeys(ent):
            def on_ctrl_key(event):
                code = event.keycode
                if code == 65:  # Ctrl+A
                    ent.select_range(0, 'end')
                    return "break"
                elif code == 67:  # Ctrl+C
                    try:
                        self.clipboard_clear()
                        self.clipboard_append(ent.selection_get())
                    except tk.TclError:
                        pass
                    return "break"
                elif code == 86:  # Ctrl+V
                    try:
                        ent.insert('insert', self.clipboard_get())
                    except tk.TclError:
                        pass
                    return "break"
                elif code == 88:  # Ctrl+X
                    try:
                        self.clipboard_clear()
                        self.clipboard_append(ent.selection_get())
                        ent.delete("sel.first", "sel.last")
                    except tk.TclError:
                        pass
                    return "break"

            ent.bind("<Control-Key>", on_ctrl_key)
            ent.bind("<Return>", lambda e: refresh_table())

        bind_hotkeys(iname_entry)
        btn_search.configure(command=refresh_table)

        # 🔹 При изменении выпадающего списка — сразу обновлять таблицу
        type_box.bind("<<ComboboxSelected>>", lambda e: refresh_table())

        refresh_table()  # первичная загрузка

    # ------------------- Обновления клиента (как было) -------------------
    def check_updates(self):
        try:
            client_state = load_json(CLIENT_VERSION_FILE, {"version": "0", "files": []})
            res = self.api.check_files(client_state.get("files", []))
            todo = res.get("files_to_download", [])
            if not todo:
                messagebox.showinfo("Обновление", "Клиент актуален")
                return

            def progress_cb(done_bytes, total_bytes, speed):
                if total_bytes > 0:
                    pct = int(done_bytes / total_bytes * 100)
                    self.pb["value"] = pct
                    mb_done = done_bytes / (1024 * 1024)
                    mb_total = total_bytes / (1024 * 1024)
                    self.lbl_status.config(
                        text=f"Загружается {mb_done:.1f} МБ из {mb_total:.1f} МБ ({speed:.2f} МБ/с)"
                    )
                    self.update_idletasks()

            def done_cb(ok, msg):
                if ok:
                    self.pb["value"] = 100
                    self.lbl_status.config(foreground="green", text="Обновление завершено ✅")
                else:
                    self.lbl_status.config(foreground="red", text=f"Ошибка: {msg}")

            self.updater.update_files(todo, progress_cb, done_cb)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось проверить обновления: {e}")

# =====================  ЗАПУСК  ==============================
if __name__ == "__main__":
    app = LauncherGUI()
    app.mainloop()





