# Приложение для создания заметок с напоминаниями в Telegram

1. Клонируйте репозиторий:
git clone https://github.com/virus37161/Notes.git

2. Создайте файл `.env` в директории `app` и внесите туда следующие переменные:
POSTGRES_USER=django
POSTGRES_PASSWORD=password
POSTGRES_DB=notes
POSTGRES_PORT=5432
POSTGRES_HOST=localhost
TOKEN=Ваш токен телеграмм бота

3. Деплой приложения на сервер:
docker compose up --watch

4. Ожидайте запуска и введите команду `/start` в телеграмм боте.
