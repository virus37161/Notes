Данное приложение позволяет создавать в телеграмме заметки с напоминаниями
1. git clone https://github.com/virus37161/Notes.git
2. необходимо создать в директории app .env и внести туда следующие переменные
POSTGRES_USER=django 
POSTGRES_PASSWORD=password
POSTGRES_DB=notes
POSTGRES_PORT=5432
POSTGRES_HOST=localhost
TOKEN = Ваш токен телеграмм бота
3. Деплой приложения на сервер
   docker compose up --watch
4. Ожидаем запуска и вводим команду /start в телеграмм боте.
