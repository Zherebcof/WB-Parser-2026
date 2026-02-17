import asyncio
import os
from dotenv import load_dotenv

# ==============================================================================
# 1. УРОВЕНЬ "ЛЕГКАЯ ПЕХОТА" (Библиотека Requests)
# ==============================================================================
# КОГДА ИСПОЛЬЗОВАТЬ:
# - Простые старые сайты (Википедия, форумы).
# - Если сайт быстро открывается и данные сразу есть в коде (Ctrl+U).
# - Нет жесткой защиты (Cloudflare).
# ==============================================================================

import requests


def get_simple_page(url):
    """
    Простой запрос. Самый быстрый способ, но легко палится.
    """

    # ЗАГОЛОВКИ (HEADERS)
    # Мы притворяемся браузером, чтобы сервер не подумал, что мы "голый" скрипт.
    headers = {
        # Паспорт: Говорим, что мы Chrome на Windows
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        # Говорим, какие форматы мы понимаем (текст, картинки)
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        # Язык: Русский, затем Английский
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    try:
        # timeout=10: Если сайт тупит больше 10 секунд, мы бросаем трубку, чтобы бот не завис.
        response = requests.get(url, headers=headers, timeout=10)

        # ПРОВЕРКА НА ОШИБКИ
        # Если статус 404 (нет страницы) или 500 (ошибка сервера), скрипт остановится и покажет ошибку.
        response.raise_for_status()

        # Возвращаем чистый текст HTML страницы
        return response.text

    except Exception as e:
        print(f"❌ Ошибка requests: {e}")
        return None


# ==============================================================================
# 2. УРОВЕНЬ "НИНДЗЯ" (Библиотека curl_cffi)
# ==============================================================================
# КОГДА ИСПОЛЬЗОВАТЬ:
# - Сайт выдает ошибку 403 (Access Denied) при обычном requests.
# - Данные прилетают в JSON (API), но стоит защита Cloudflare.
# - JavaScript выполнять НЕ нужно (просто забрать данные).
# ==============================================================================

from curl_cffi import requests as cffi_requests


def get_protected_api(url):
    """
    Хитрый запрос. Подделывает TLS-отпечаток (походку) браузера.
    """
    try:
        # impersonate="chrome120":
        # Это ГЛАВНАЯ магия. Мы копируем поведение реального браузера байт-в-байт.
        # Защита думает, что это настоящий Хром.
        response = cffi_requests.get(
            url,
            impersonate="chrome120",
            timeout=15
        )

        # .json(): Обычно такие запросы делают к API, поэтому сразу превращаем ответ в словарь Python
        return response.json()

    except Exception as e:
        print(f"❌ Ошибка curl_cffi: {e}")
        return None


# ==============================================================================
# 3. УРОВЕНЬ "ТЯЖЕЛЫЙ ТАНК" (Playwright Stealth)
# ==============================================================================
# КОГДА ИСПОЛЬЗОВАТЬ:
# - Wildberries, Ozon, YouTube и другие SPA-сайты.
# - Когда нужно, чтобы на странице отработали скрипты (JavaScript).
# - Когда ничего другое не помогает.
# ==============================================================================

from playwright.sync_api import sync_playwright


def get_heavy_site_stealth(url):
    """
    Запуск полноценного браузера с максимальной маскировкой.
    """
    with sync_playwright() as p:
        # 1. ЗАПУСК БРАУЗЕРА (LAUNCH)
        browser = p.chromium.launch(
            headless=True,  # True = Без окна (скрытно), False = Видим браузер
            args=[
                # Самый важный флаг: отключает режим "Автоматизации" в Хроме
                '--disable-blink-features=AutomationControlled',
                # Безопасность для запуска на сервере (Linux)
                '--no-sandbox',
                # Убирает лишние визуальные полоски
                '--disable-infobars',
                # Отключает расширения, чтобы не палиться и экономить память
                '--disable-extensions'
            ]
        )

        # 2. НАСТРОЙКА ПРОФИЛЯ (CONTEXT)
        # Создаем "виртуальную личность"
        context = browser.new_context(
            # Подставляем User-Agent от обычного ПК (иначе будет HeadlessChrome)
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            # Размер экрана FullHD (роботы часто сидят на 800x600)
            viewport={'width': 1920, 'height': 1080},
            # Язык и время (важно для защиты, чтобы совпадало с IP)
            locale='ru-RU',
            timezone_id='Europe/Moscow'
        )

        # 3. ХИРУРГИЧЕСКОЕ ВМЕШАТЕЛЬСТВО (SCRIPT)
        page = context.new_page()
        # Удаляем переменную navigator.webdriver, которую ищут защитные системы
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        try:
            # wait_until='domcontentloaded': Ждем, пока загрузится HTML, а не все картинки (быстрее)
            page.goto(url, wait_until='domcontentloaded', timeout=30000)

            # ВАЖНО: Тут можно добавить ожидание конкретного элемента
            # page.wait_for_selector('.price-block')

            # Забираем итоговый код страницы
            content = page.content()
            return content

        except Exception as e:
            print(f"❌ Ошибка Playwright: {e}")
            return None
        finally:
            # Всегда закрываем браузер, даже если была ошибка, чтобы не забить память
            browser.close()


# ==============================================================================
# 4. ШАБЛОН ТЕЛЕГРАМ-БОТА (Aiogram 3.x)
# ==============================================================================
# Базовый скелет для любого нового бота.
# ==============================================================================

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

# Загружаем переменные из файла .env (чтобы не светить токен)
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Создаем объекты бота и диспетчера
bot = Bot(token=TOKEN)
# MemoryStorage нужен для FSM (машины состояний), чтобы бот помнил диалог
dp = Dispatcher(storage=MemoryStorage())


# ХЭНДЛЕР (Обработчик) команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я шаблон бота. Я готов к работе.")


# ФУНКЦИЯ ЗАПУСКА
async def main():
    print("🚀 Бот запущен!")
    # Удаляем старые обновления (чтобы бот не отвечал на старые сообщения при включении)
    await bot.delete_webhook(drop_pending_updates=True)
    # Запускаем бесконечный цикл прослушивания
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Запуск асинхронной функции
    asyncio.run(main())