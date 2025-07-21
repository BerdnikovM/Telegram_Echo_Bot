FROM python:3.12-slim

# 1. Переменные окружения, чтобы потом не писать --no-cache-dir
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# 2. Кэшируем зависимости
COPY requirements.txt .
RUN pip install -r requirements.txt

# 3. Копируем исходники
COPY . .

# 4. Позволяем задавать токен во время запуска
#    Если переменной нет — используем то, что прописан в config.py
ENV BOT_TOKEN=""

CMD ["python", "bot.py"]
