# middlewares.py — Прослойки (Фильтры)
# Этот файл работает как фейс-контроль на входе в клуб (Бот)

import time  # 🕒 Библиотека для работы со временем (чтобы засекать секунды)
from aiogram import BaseMiddleware  # 🛡️ Базовый класс (шаблон) для создания фильтров
from aiogram.types import Message  # 📩 Тип данных "Сообщение" (текст, фото и т.д.)
from typing import Callable, Dict, Any, Awaitable  # 🧰 Типизация (подсказки для редактора кода)


class AntiFloodMiddleware(BaseMiddleware):
    """
    🛡️ Класс защиты от спама (Анти-Флуд).

    Как это работает:
    1. Мы запоминаем, когда конкретный человек писал в последний раз.
    2. Если он пишет снова, а прошло меньше N секунд — мы его игнорируем.
    """

    def __init__(self, time_limit: int = 2):
        # Этот метод срабатывает один раз при запуске бота
        self.limit = time_limit  # ⏱ Лимит времени (2 секунды по умолчанию)
        self.last_message_times = {}  # 📒 Блокнот охранника. Формат: {ID_юзера: Время}

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        """
        Этот метод срабатывает ПРИ КАЖДОМ сообщении.
        handler — это "дверь" дальше (к логике бота).
        event — это само сообщение от пользователя.
        """

        # 1. ПРОВЕРКА ТИПА СОБЫТИЯ
        # Нас интересуют только сообщения (Message).
        # (Бывают еще "редактирования", "колбэки" от кнопок — их пока пропускаем без проверки)
        if isinstance(event, Message):

            # Достаем ID того, кто стучится
            user_id = event.from_user.id
            # Смотрим на часы (текущее время в секундах)
            current_time = time.time()

            # 2. ПРОВЕРКА В БЛОКНОТЕ
            # Если этот ID уже есть в списке (значит, он писал нам ранее)
            if user_id in self.last_message_times:

                # Считаем, сколько времени прошло с прошлого раза
                time_passed = current_time - self.last_message_times[user_id]

                # 3. ВЕРДИКТ ОХРАННИКА
                # Если прошло МЕНЬШЕ лимита (например, прошло 0.5 сек, а лимит 2.0)
                if time_passed < self.limit:
                    # ⛔ СТОП!
                    # Мы делаем return БЕЗ вызова handler().
                    # Это значит, что сообщение умирает здесь. Бот (handlers.py) его не увидит.
                    return

                    # 4. ЗАПИСЬ В БЛОКНОТ
            # Если спама нет — обновляем время последнего визита для этого юзера
            self.last_message_times[user_id] = current_time

        # 5. ЗЕЛЕНЫЙ СВЕТ 🟢
        # Вызываем handler() — открываем дверь и передаем сообщение дальше в handlers.py
        return await handler(event, data)