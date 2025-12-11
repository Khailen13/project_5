# Используем официальный образ Python с минималистичным образом
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Обновляем систему и устанавливаем системные зависимости
RUN apt-get update && \
    apt-get install -y \
        gcc \
        libpq-dev \
        && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Создаем системного пользователя
RUN groupadd -r appuser && \
    useradd -r -g appuser appuser

# Создаем директорию для кэша
RUN mkdir -p /home/appuser/.cache && \
    chmod -R 755 /home/appuser/.cache

# Копируем и устанавливаем Python зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Создаем необходимые директории с правильными правами
RUN mkdir -p \
    /app/staticfiles \
    /app/media \
    /app/logs \
    && chown -R appuser:appuser /app \
    && chmod -R 755 /app \
    && chmod -R 775 /app/staticfiles \
    && chmod -R 775 /app/media

# Копируем код приложения
COPY --chown=appuser:appuser . .

# Добавляем проверку содержимого после копирования
RUN ls -la /app  # Проверяем, что все файлы скопировались

# Устанавливаем пользователя по умолчанию
USER appuser

# Открываем порт
EXPOSE 8000

# Добавляем проверку версий установленных пакетов
RUN pip list

# Команда для запуска приложения
CMD ["gunicorn", "config.wsgi:application", "-b", "0.0.0.0:8000"]
