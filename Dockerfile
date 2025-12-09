# Этап 1: сборка зависимостей (builder)
FROM python:3.13-slim AS builder

WORKDIR /app

RUN pip install poetry

RUN apt-get update && apt-get install -y \
    gcc \
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

# Создаем директории и устанавливаем права
RUN mkdir -p /app/media /app/staticfiles \
    && chown -R appuser:appuser /app

# Копируем зависимости
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

# Добавляем команду для сбора статических файлов
RUN chown -R appuser:appuser /app/staticfiles \
    && chmod -R 755 /app/staticfiles

# Переключаемся на пользователя appuser
USER appuser

EXPOSE 8000

# Добавляем команду для автоматического сбора статических файлов
CMD bash -c "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 project.wsgi:application"
