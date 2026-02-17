# 1. Используем Python 3.11
FROM python:3.11-slim

# 2. Указываем рабочую папку
WORKDIR /app

   # 3. Устанавливаем системные зависимости для браузера (исправленный список)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*
    \
    # 4. Копируем и устанавливаем библиотеки из requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Устанавливаем сам браузер Chromium
RUN playwright install chromium

# 6. Копируем весь код
COPY . .

# 7. Запуск
CMD ["python", "main.py"]