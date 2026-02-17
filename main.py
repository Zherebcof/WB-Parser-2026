# main.py — Точка входа в программу (Запускатор)

import asyncio  # 🏃 Библиотека для асинхронного запуска (чтобы делать много дел одновременно)
import logging  # 📝 Библиотека для ведения журнала событий (логов)
import os       # 💻 Библиотека для работы с операционной системой (получить переменные окружения)

from dotenv import load_dotenv  # 🔐 Загрузчик секретов из файла .env
from aiogram import Bot, Dispatcher  # 🤖 Главные классы бота
from aiogram.fsm.storage.memory import MemoryStorage  # 🧠 Оперативная память бота (для хранения состояний)

# 👇 Подключаем наши модули (файлы, которые мы написали)
import database  # 🗄️ База данных
from handlers import router  # 🎮 Обработчики команд (мозги бота)
from middlewares import AntiFloodMiddleware  # 🛡️ Защита от спама

# 1. ЗАГРУЗКА НАСТРОЕК
# Ищем файл .env и загружаем из него токен
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Функция запуска (Главная функция)
async def main():
    # Настраиваем логирование (уровень INFO — пишем всё важное)
    logging.basicConfig(level=logging.INFO)
    print("🚀 Бот запускается...")

    # 2. ПОДГОТОВКА БАЗЫ ДАННЫХ
    # Создаем таблицу, если её нет (при первом запуске)
    await database.create_table()

    # 3. ИНИЦИАЛИЗАЦИЯ
    # Создаем самого бота
    bot = Bot(token=BOT_TOKEN)
    # Создаем диспетчера (он распределяет сообщения)
    dp = Dispatcher(storage=MemoryStorage())

    # 4. ПОДКЛЮЧЕНИЕ ЗАЩИТЫ (MIDDLEWARE)
    # Ставим "Охранника" на входе. 2.0 секунды — задержка между сообщениями.
    dp.message.middleware(AntiFloodMiddleware(time_limit=2.0))

    # 5. ПОДКЛЮЧЕНИЕ МОЗГОВ (ROUTER)
    # Подключаем все наши функции из handlers.py
    dp.include_router(router)

    # 6. СТАРТ
    # Удаляем старые сообщения, которые скопились, пока бот спал
    await bot.delete_webhook(drop_pending_updates=True)
    # Запускаем бесконечный цикл прослушивания Телеграма
    await dp.start_polling(bot)

# Точка входа: если файл запустили напрямую, а не импортировали
if __name__ == "__main__":
    try:
        # Запускаем асинхронную функцию main()
        asyncio.run(main())
    except KeyboardInterrupt:
        # Если нажали Ctrl+C, пишем красиво, а не ошибку
        print("🛑 Бот остановлен администратором")