from Markups.menu_markups import keyboard_menu
from SearchAds.SearchAds import get_user_search
from SearchAds.SearchMessage import search_message


def handle_clear_search(bot, message, acc_id):
    user_search = get_user_search(acc_id)
    user_search.clear_all()
    user_search.clear_init()
    bot.send_message(message.chat.id, "<b>❗️ Ви завершили пошук</b>", parse_mode='HTML', reply_markup=keyboard_menu)


def handle_clear_all_filters_search(bot, message, user_search):
    # user_search = get_user_search(acc_id)
    user_search.clear_all()
    user_search.clear_init()
    bot.send_message(message.chat.id,
                     "<b>❗️ Ви скасували всі Ваші налаштування пошуку</b>\n\n<i>Налаштування порожні</i>",
                     parse_mode='HTML', reply_markup=keyboard_menu)
    search_message(bot, message, user_search)


def handle_clear_matches_text(bot, message, user_search):
    user_search.clear_matches_text()
    search_message(bot, message, user_search)
    # search_filters_message(bot, message, user_search)


def handle_clear_condition(bot, message, user_search):
    user_search.clear_condition()
    search_message(bot, message, user_search)
    # search_filters_message(bot, message, user_search)


def handle_clear_category_subcategory(bot, message, user_search):
    user_search.clear_category()
    user_search.clear_subcategory()
    search_message(bot, message, user_search)


def handle_clear_price_max_min(bot, message, user_search):
    user_search.clear_price_min()
    user_search.clear_price_max()
    search_message(bot, message, user_search)


def handle_clear_location_region_city(bot, message, user_search):
    user_search.clear_location_region()
    user_search.clear_location_city()
    search_message(bot, message, user_search)


def handle_clear_sort_by(bot, message, user_search):
    user_search.clear_sort_date()
    user_search.clear_sort_price()
    search_message(bot, message, user_search)
