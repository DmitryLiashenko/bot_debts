# 1. Базовый образ с Python 
FROM python:3.11-slim

# 2. Установка зависимостей, необходимых для gspread и google-auth 
RUN apt-get update && apt-get install -y gcc libffi-dev && rm -rf /var/lib/apt/lists/*

# 3. Рабочая директория внутри контейнера
WORKDIR /app

# 4. Копируем файл зависимостей в контейнер
COPY requirements.txt .

# 5. Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 6. Копируем весь код проекта (без файлов из .dockerignore)
COPY . .

# 7. Команда запуска бота
CMD ["python", "bot.py"]
