# database.py — Слой работы с данными (Память)
# Используем SQLite — это легкая база данных в одном файле

import aiosqlite  # 🗄️ Библиотека для асинхронной работы с БД
from datetime import datetime  # 📅 Чтобы записывать дату регистрации

DB_NAME = 'bot_database.db'  # Имя файла базы данных


async def create_table():
    """
    Создает таблицы при первом запуске, если их нет.
    1. users — для хранения пользователей
    2. search_history — для истории запросов
    """
    async with aiosqlite.connect(DB_NAME) as db:
        # Таблица пользователей
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                telegram_id INTEGER,
                registration_date TEXT
            )
        ''')
        # Таблица истории поиска
        await db.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                query TEXT,
                date TEXT
            )
        ''')
        await db.commit()
        print("✅ База данных подключена (Пользователи + История)")


async def add_user(user_id, username, full_name):
    """Добавляет нового пользователя, если его еще нет"""
    async with aiosqlite.connect(DB_NAME) as db:
        # Проверяем, есть ли он уже
        async with db.execute('SELECT user_id FROM users WHERE telegram_id = ?', (user_id,)) as cursor:
            if not await cursor.fetchone():
                # Если нет — записываем
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                await db.execute(
                    'INSERT INTO users (telegram_id, username, full_name, registration_date) VALUES (?, ?, ?, ?)',
                    (user_id, username, full_name, now)
                )
                await db.commit()


async def add_search_query(user_id, query):
    """Сохраняет, что искал пользователь (для аналитики)"""
    async with aiosqlite.connect(DB_NAME) as db:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await db.execute(
            'INSERT INTO search_history (user_id, query, date) VALUES (?, ?, ?)',
            (user_id, query, now)
        )
        await db.commit()


async def get_stats():
    """Собирает статистику для Админа"""
    async with aiosqlite.connect(DB_NAME) as db:
        # Считаем людей
        async with db.execute('SELECT COUNT(*) FROM users') as cursor:
            users_count = await cursor.fetchone()

        # Считаем запросы
        async with db.execute('SELECT COUNT(*) FROM search_history') as cursor:
            queries_count = await cursor.fetchone()

        return (f"📊 <b>Статистика бота:</b>\n\n"
                f"👤 Пользователей: <b>{users_count[0]}</b>\n"
                f"🔎 Поисковых запросов: <b>{queries_count[0]}</b>")


async def get_all_users():
    """Выгружает всех пользователей для Excel-отчета"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT telegram_id, username, full_name, registration_date FROM users') as cursor:
            return await cursor.fetchall()


async def get_all_users_ids():
    """Получает список только ID (для рассылки)"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT telegram_id FROM users') as cursor:
            rows = await cursor.fetchall()
            # Превращаем [(123,), (456,)] в простой список [123, 456]
            return [row[0] for row in rows]