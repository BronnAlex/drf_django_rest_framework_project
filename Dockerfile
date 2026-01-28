# Используем официальный slim-образ Python 3.12
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Обновляем список доступных пакетов и Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей в контейнер
COPY requirements.txt ./

# Устанавливаем зависимости Python
# Флаг --no-cache-dir указывает pip не сохранять кэш чтобы уменьшить размер образа
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения в контейнер
COPY . .

# Определяем переменные окружения
ENV SECRET_KEY=os.getenv("SECRET_KEY")
ENV CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL")
ENV CELERY_BACKEND=os.getenv("CELERY_RESULT_BACKEND")
ENV CELERY_BEAT_SCHEDULER = os.getenv("CELERY_BEAT_SCHEDULER")

# Создаем директорию app/media для медиафайлов внутри контейнера
RUN mkdir -p /app/media

# Пробрасываем порт, который будет использовать Django
EXPOSE 8000

# Команда для запуска приложения при запуске контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
