FROM python:3.13-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Создание системного пользователя
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Создание директории для кэша
RUN mkdir -p /home/appuser/.cache && \
    chmod -R 755 /home/appuser/.cache

# Установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Очистка кэша pip
RUN pip cache purge

# Создание директорий с правильными правами
RUN mkdir -p \
    /app/staticfiles \
    /app/media \
    /app/logs \
    && chown -R appuser:appuser /app \
    && chmod -R 755 /app \
    && chmod -R 775 /app/staticfiles \
    && chmod -R 775 /app/media

# Копирование кода с правильным владельцем
COPY --chown=appuser:appuser . .

# Дополнительные права для staticfiles
RUN chmod -R 777 /app/staticfiles

USER appuser
EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "-b", "0.0.0.0:8000"]