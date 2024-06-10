from telebot import types

from DataBase.Advertisement_database import get_all_info_about_advertisement, set_new_location_ad, change_status
from Markups.creating_ad_category_region_markups import regions, cities
from Markups.menu_markups import keyboard_menu, markup_ad_types
from Messages.StartCreatingAdMessages import error_region_selection_message, \
    error_city_selection_message
from Notifications.ModeratorNotifications import notification_new_description_ad, notification_new_location_ad
from OtherTools.AdvertisementChangesLogging import save_new_changes
from OtherTools.CancelAction import cancel_change_location_ad_action


def process_new_location_ad_input(bot, call, ad_id):
    info_ad = get_all_info_about_advertisement(ad_id)

    category_ad = info_ad[2]
    name = info_ad[4]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for region in regions:
        markup.add(types.KeyboardButton(region))
    markup.add(types.KeyboardButton("❌ Скасувати дію"))

    bot.send_message(call.message.chat.id, f"<b>❗️ Оберіть зі списку нову область для оголошення '{name}'</b>",
                     parse_mode='HTML', reply_markup=markup)

    bot.register_next_step_handler(call.message, region_selection, bot, ad_id)


def region_selection(message, bot, ad_id):
    if message.text == '❌ Скасувати дію':
        cancel_change_location_ad_action(bot, message)
        return

    region = message.text
    cities_list = cities.get(region, [])
    markup_cities = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if cities_list:
        for city in cities_list:
            markup_cities.add(types.KeyboardButton(city))
        markup_cities.add(types.KeyboardButton("❌ Скасувати дію"))

        city_selection_message = (f"📍 <b>Оберіть Ваше місто в {region}</b>\n\n🌍 <b>Примітка:</b> <i>Оберіть місто з "
                                  f"переліку, щоб точно вказати місцезнаходження вашого товару\n\n<b>Якщо Ваш населений пнукт "
                                  f"відсутній у списку, то оберіть найближчий до Вас</b></i>")

        bot.send_message(message.chat.id, city_selection_message, parse_mode='HTML', reply_markup=markup_cities)
        bot.register_next_step_handler(message, city_selection, bot, ad_id, region)
    else:
        markup_region = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for region in regions:
            markup_region.add(types.KeyboardButton(region))
        markup_region.add(types.KeyboardButton("❌ Скасувати дію"))
        bot.send_message(message.chat.id, error_region_selection_message, parse_mode='HTML', reply_markup=markup_region)
        bot.register_next_step_handler(message, region_selection, ad_id, bot)


def city_selection(message, bot, ad_id, region):
    if message.text == '❌ Скасувати дію':
        cancel_change_location_ad_action(bot, message)
        return

    ad_info = get_all_info_about_advertisement(ad_id)
    ad_name = ad_info[4]
    owner_id = ad_info[1]
    ad_old_region = ad_info[10]
    ad_old_city = ad_info[11]

    city = message.text

    # Перевірка, чи обране місто є в списку міст для даного регіону
    cities_list = cities.get(region, [])
    if city not in cities_list:
        bot.send_message(message.chat.id, error_city_selection_message, parse_mode='HTML')
        bot.register_next_step_handler(message, city_selection, bot, ad_id, region)
        return

    else:
        set_new_location_ad(ad_id, region, city)
        success_message = f'<b>✔️ Ви успішно змінили місцезнаходження</b>\n\n<i><b>📝 Примітка:</b> оголошення знаходиться на модерації. Наші модератори перевірять Ваше оголошення якнайшвидше і його зможуть побачити інші люди</i>'
        bot.send_message(message.chat.id, success_message, parse_mode='HTML', reply_markup=markup_ad_types)

        msg_old_location = f"{ad_old_region}, {ad_old_city}"
        msg_new_location = f"{region}, {city}"

        text = 'location_log'
        save_new_changes(ad_id, text, msg_old_location, msg_new_location)

        new_status = 'on moderation'
        change_status(ad_id, new_status)
        notification_new_location_ad(bot, ad_name, owner_id)
