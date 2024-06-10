import math


def get_matches_text_button(user_search):
    if user_search.matches_text:
        matches_text_btn_text = f"❌ Скасувати вказаний збіг тексту"
        callback = 'cancel_matches_text_btn'
    else:
        matches_text_btn_text = "📝 Вказати текст для пошуку"
        callback = 'matches_text_btn'
    return matches_text_btn_text, callback


def get_condition_button(user_search):
    if user_search.condition:
        condition_btn_text = f"❌ Скасувати вказаний стан товару"
        callback = 'cancel_condition_btn'
    else:
        condition_btn_text = "🔖 Вказати стан товару"
        callback = 'condition_btn'
    return condition_btn_text, callback


def get_category_and_subcategory_button(user_search):
    if user_search.category and user_search.subcategory:
        category_and_subcategory_btn_text = f"❌ Скасувати вказані категорії та підкатегорії"
        callback = 'cancel_category_and_subcategory_btn'
    else:
        category_and_subcategory_btn_text = "🏷️ Вказати Категорію/Підкатегорію"
        callback = 'category_and_subcategory_btn'
    return category_and_subcategory_btn_text, callback


def get_price_min_max_callback(user_search):
    if user_search.price_min is not None and user_search.price_max is not None:
        if not (user_search.price_min == 0 and math.isinf(user_search.price_max)):
            price_min_max_btn_text = f"❌ Скасувати вказану максмальну/мінімальну ціну"
            callback = 'cancel_price_min_max_btn'
            return price_min_max_btn_text, callback

    price_min_max_btn_text = "💰 Вказати ціну [Мінімальна/Максимальна]"
    callback = 'price_min_max_btn'
    return price_min_max_btn_text, callback


def get_location_button(user_search):
    if user_search.location_region and user_search.location_city:
        location_btn_text = f"❌ Скасувати вказане місцезнаходження"
        callback = 'cancel_location_btn'
    else:
        location_btn_text = "🌍 Вказати місцезнаходження [Область/Місто]"
        callback = 'location_btn'
    return location_btn_text, callback


def get_sort_by_button(user_search):
    if user_search.sort_date or user_search.sort_price:
        sort_by_btn_text = f"❌ Скасувати вказане сортування"
        callback = 'cancel_sort_by_btn'
    else:
        sort_by_btn_text = "🔄 Сортувати пошук за... [Дата/Ціна]"
        callback = 'sort_by_btn'
    return sort_by_btn_text, callback
