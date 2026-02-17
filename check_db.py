import sqlite3

connection = sqlite3.connect('bot_users.db')
cursor = connection.cursor()

try:
    # 1. СМОТРИМ ПОЛЬЗОВАТЕЛЕЙ
    print("\n👥 ПОЛЬЗОВАТЕЛИ:")
    print(f"{'ID':<5} {'Telegram ID':<15} {'Имя':<20} {'Регистрация'}")
    print("-" * 60)

    cursor.execute('SELECT * FROM users')
    for user in cursor.fetchall():
        reg_date = user[4] if len(user) > 4 else "Нет данных"
        print(f"{user[0]:<5} {user[1]:<15} {user[3]:<20} {reg_date}")

    # 2. СМОТРИМ ИСТОРИЮ ПОИСКА
    print("\n🔎 ИСТОРИЯ ПОИСКА:")
    print(f"{'ID':<5} {'Telegram ID':<15} {'Запрос':<30} {'Время'}")
    print("-" * 80)

    cursor.execute('SELECT * FROM search_history ORDER BY id DESC LIMIT 10')  # Покажет последние 10
    for row in cursor.fetchall():
        print(f"{row[0]:<5} {row[1]:<15} {row[2]:<30} {row[3]}")

except sqlite3.OperationalError as e:
    print(f"❌ Ошибка: {e}")

connection.close()