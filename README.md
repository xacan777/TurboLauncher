# TURBO Launcher

Обновленный лаунчер с новым брендингом, современным UI, Python backend и готовыми API для базы данных и форума.

## Содержимое репозитория

- **Frontend**: Vue 3 + Electron (директория `src/`).
- **Backend**: Flask (`app.py`) + эталонные SQL/данные (`Laucnher.py`).
- **Форум**: хранится в `forum.json` (автогенерация при старте сервера).
- **Конфигурации**: `.env.example` (backend), `vue.config.js` (брендинг сборки).

## Запуск backend (Python)

1. Скопируйте окружение:
   ```bash
   cp .env.example .env
   ```
   Отредактируйте строку подключения `DB_CONNECTION_STRING` под вашу БД или оставьте пустой, чтобы использовать демо-данные.

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустите Flask сервер:
   ```bash
   python app.py
   ```
   API по умолчанию доступно на `http://localhost:5000/api`.

### Доступные API
- `POST /api/auth/login` – вход (демо без БД: `demo/demo`).
- `POST /api/auth/register` – регистрация.
- `GET /api/server/status` – статус сервера/онлайн.
- `GET /api/news` – новости лаунчера.
- `GET /api/leaderboard/levels`, `GET /api/leaderboard/power` – таблицы лидеров.
- `GET /api/droplist` – дроп-лист (фильтры `iname`, `mname`, `place`).
- `GET /api/enhancement` – усиление предметов (фильтры `iname`, `type`).
- Форум:
  - `GET /api/forum/topics`
  - `POST /api/forum/topics` (создание темы)
  - `GET /api/forum/topics/<id>/messages`
  - `POST /api/forum/topics/<id>/messages`

## Запуск frontend (Vue/Electron)

1. Установите зависимости:
   ```bash
   yarn install
   ```
   Если `vue-cli-service` не находится, убедитесь, что установка завершилась без ошибок (команда должна создать `node_modules` и бинарь `./node_modules/.bin/vue-cli-service`).
   > ⚠️ Требуемая версия Node для зависимостей — 16.x (рекомендуется 16 LTS).  
   > На Windows можно быстро переключиться через nvm-windows:  
   > `nvm install 16 && nvm use 16`
2. Установите переменную API (опционально):
   ```bash
   export VUE_APP_API_BASE_URL="http://localhost:5000/api"
   ```
3. Старт dev-сборки:
   ```bash
   yarn serve
   ```
4. Сборка продакшн:
   ```bash
   yarn build
   ```
5. Electron dev:
   ```bash
   yarn electron:serve
   ```
   Если вы видите сообщение `'vue-cli-service' is not recognized`, проверьте:
   - выполнен ли `yarn install` под текущим пользователем;
   - нет ли конфликта версий Node/Yarn (рекомендуется Yarn 1.x и Node 16+);
   - что вы запускаете команду из корня проекта, а не из другой директории.

### Быстрый старт через npm
```bash
npm install
npm run dev
```
`npm run dev` равносилен `yarn electron:serve` и поднимает Electron‑окно с фронтендом.

### Типовая ошибка на Node 18/20/22/24+
Если при `yarn install` появляется сообщение вроде
`The engine "node" is incompatible ... Expected "8 || 10 || 12 || 14 || 16 || 17". Got "24.x.x"`,
переключите Node на 16.x перед установкой:
```bash
nvm install 16
nvm use 16
```
Скрипт `scripts/check-node.js` дополнительно остановит установку, если версия Node не 16.x, чтобы было понятно, что нужно сменить среду.

## Основные экраны
- **Главная** – новости, статус серверов, быстрый старт клиента.
- **База данных** – вкладки: таблица лидеров, дроп-лист, усиление предметов.
- **Форум** – список тем, чтение/ответы, создание темы, обновление `forum.json`.
- **Авторизация/регистрация** – отдельный экран, хранение сессии в сторе и storage.

## Конфигурация бренда
- Электрон сборка: `vue.config.js` (`productName`, `appId`, иконки).
- Нотификации/заголовки: `src/utility.js`, `src/background.js`.

## Полезно знать
- При отсутствии подключения к БД backend возвращает демо-данные, чтобы UI оставался рабочим.
- `forum.json` создаётся автоматически, если его нет, и синхронизируется после операций создания тем/сообщений.
