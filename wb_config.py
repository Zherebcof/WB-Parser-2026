# Настройки селекторов Wildberries
# Если WB поменяет дизайн, меняем классы только тут!

SELECTORS = {
    "card_wrapper": ".product-card__wrapper",       # Сама карточка товара
    "link_tag": "a.product-card__link",             # Ссылка на товар
    "price_new": "ins.price__lower-price",          # Новая цена
    "price_old": "del",             # ИСПРАВЛЕНИЕ:
    # Раньше тут была ошибка (копия price_new).
    # У старой цены на WB нет класса, она лежит просто в теге <del>.
    # Поэтому пишем название тега без точки.
    "image": "img.j-thumbnail"                      # Картинка
}