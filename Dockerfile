# 1. Базовый образ (Python 3.9 с минимальным окружением)
FROM python:3.9-alpine

# 2. Установка зависимых системных пакетов (если нужны)
RUN apk add --no-cache \
    curl \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev

# 3. Рабочая директория в контейнере
WORKDIR /app

# 4. Копируем зависимости отдельно для кэширования
COPY requirements.txt .

# 5. Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 6. Копируем весь проект в контейнер
COPY . .

# 7. Команда для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]