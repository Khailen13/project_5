# Этап 1: сборка зависимостей (builder)
FROM python:3.13-slim AS builder

WORKDIR /app

RUN pip install poetry

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Добавляем установку psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Этап 2: финальный образ (runner)
FROM python:3.13-slim AS runner

WORKDIR /app

# Создаем пользователя и группу
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Создаем директорию и устанавливаем права
RUN mkdir -p /app/media \
    && chown -R appuser:appuser /app

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

# Переключаемся на пользователя appuser
USER appuser

# Обновленные переменные окружения
ENV CELERY_BROKER_URL="redis://redis:6379/0"
ENV CELERY_BACKEND="redis://redis:6379/0"
ENV SECRET_KEY="django-insecure-1*-d_v+1b+0t)7#!+w+etl9vzg+y6nvqzny3ro9vw)=$lo&x#8"

# Добавляем переменные для подключения к БД
ENV DB_HOST=db
ENV DB_PORT=5432
ENV DB_NAME=your_database_name
ENV DB_USER=your_user
ENV DB_PASSWORD=your_password

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
