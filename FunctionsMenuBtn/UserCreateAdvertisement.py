import os
import uuid
from telebot.types import Message

from DataBase.Advertisement_database import create_advertisement, get_ads_id
from telebot import TeleBot, types
from Markups.creating_ad_category_region_markups import regions, cities, categories, subcategories
from Markups.markups import cancel_action
from Markups.menu_markups import keyboard_menu
from Messages.StartCreatingAdMessages import category_selection_message, category_error_selection_message, \
    generate_subcategory_message, subcategory_error_selection_message, confirmation_message_category_subcategory, \
    title_input_message, description_input_message, photo_input_message, photo_error_message, price_input_message, \
    price_error_message, region_selection_message, non_correct_price_error_message, select_city_message, \
    error_region_selection_message, error_city_selection_message, announcement_success_message, \
    condition_selection_message, incorrect_condition_message, name_length_error_message, \
    description_length_error_message
from OtherTools.CancelAction import cancel_advertisement_creation
from Notifications.ModeratorNotifications import notification_new_ad


def start_creating_advertisement(bot: TeleBot, message: Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for category in categories:
        markup.add(types.KeyboardButton(category))
    markup.add(types.KeyboardButton("❌ Скасувати дію"))

    bot.send_message(message.chat.id, category_selection_message, parse_mode='HTML', reply_markup=markup)

    bot.register_next_step_handler(message, get_category, bot)


def get_category(message: Message, bot: TeleBot):
    if message.text == '❌ Скасувати дію':
        cancel_advertisement_creation(message, bot)
        return

    category = message.text
    subcategory_list = subcategories.get(category, [])

    if category in categories:
        if subcategory_list:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True,)
            for subcategory in subcategory_list:
                markup.add(types.KeyboardButton(subcategory))
            markup.add(types.KeyboardButton("❌ Скасувати дію"))

            bot.send_message(message.chat.id, generate_subcategory_message(category), parse_mode='HTML', reply_markup=markup)
            bot.register_next_step_handler(message, get_subcategory, bot, category)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        for category in categories:
            markup.add(types.KeyboardButton(category))
        markup.add(types.KeyboardButton("❌ Скасувати дію"))

        bot.send_message(message.chat.id, category_error_selection_message, parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, get_category, bot)


def get_subcategory(message: Message, bot: TeleBot, category: str):
    if message.text == '❌ Скасувати дію':
        cancel_advertisement_creation(message, bot)
        return

    subcategory = message.text

    subcategory_list = subcategories.get(category, [])
    if subcategory not in subcategory_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, )
        for subcategory in subcategory_list:
            markup.add(types.KeyboardButton(subcategory))
        markup.add(types.KeyboardButton("❌ Скасувати дію"))

        bot.send_message(message.chat.id, subcategory_error_selection_message,
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, get_subcategory, bot, category)

    else:
        bot.send_message(message.chat.id, confirmation_message_category_subcategory(category, subcategory), parse_mode='HTML')
        bot.send_message(message.chat.id, title_input_message, parse_mode='HTML', reply_markup=cancel_action)
        bot.register_next_step_handler(message, get_advertisement_name, bot, category, subcategory)


def get_advertisement_name(message: Message, bot: TeleBot, category: str, subcategory: str):
    if message.text == '❌ Скасувати дію':
        cancel_advertisement_creation(message, bot)
        return

    name = message.text
    if len(name) > 40:
        bot.send_message(message.chat.id, name_length_error_message, parse_mode='HTML', reply_markup=cancel_action)
        bot.register_next_step_handler(message, get_advertisement_name, bot, category, subcategory)
        return
    else:
        bot.send_message(message.chat.id, description_input_message, parse_mode='HTML', reply_markup=cancel_action)
        bot.register_next_step_handler(message, get_advertisement_description, bot, category, subcategory, name)


def get_advertisement_description(message: Message, bot: TeleBot, category: str, subcategory: str, name: str):
    if message.text == '❌ Скасувати дію':
        cancel_advertisement_creation(message, bot)
        return

    description = message.text

    if len(description) > 650:
        bot.send_message(message.chat.id, description_length_error_message, parse_mode='HTML', reply_markup=cancel_action)
        bot.register_next_step_handler(message, get_advertisement_description, bot, category, subcategory, name)
        return

    else:
        bot.send_message(message.chat.id, photo_input_message, parse_mode='HTML', reply_markup=cancel_action)
        bot.register_next_step_handler(message, handle_photo, bot, category, subcategory, name, description)


user_photos = {}


def handle_photo(message, bot, category, subcategory, name, description):
    if message.text == '❌ Скасувати дію':
        cancel_advertisement_creation(message, bot)
        user_photos.clear()
        return
    elif message.text == '🔥 Це все, зберегти фото':
        save_photos_and_continue(message, bot, category, subcategory, name, description)
        return

    if not message.photo:
        bot.send_message(message.chat.id, photo_error_message, parse_mode='HTML')
        bot.register_next_step_handler(message, handle_photo, bot, category, subcategory, name, description)
        return

    else:
        user_id = message.from_user.id
        if user_id not in user_photos:
            user_photos[user_id] = []

        photo_count = len(user_photos[user_id]) + 1
        total_photos = 5

        if len(user_photos[user_id]) == 5:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            save_key = types.KeyboardButton("🔥 Це все, зберегти фото")
            cancel_key = types.KeyboardButton('❌ Скасувати дію')
            keyboard.add(save_key, cancel_key)

            bot.send_message(message.chat.id, "<b>❗️ Ви вже додали максимальну кількість фотографій (5)</b>",
                             reply_markup=keyboard)
        else:
            user_photos[user_id].append(message.photo[-1])
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            photo2key = types.KeyboardButton("🔥 Це все, зберегти фото")
            photo3key = types.KeyboardButton('❌ Скасувати дію')
            keyboard.add(photo2key, photo3key)

            bot.send_message(message.chat.id, f"<b>✔️ Фотографія успішно додана ({photo_count}/{total_photos})</b>",
                             parse_mode='HTML', reply_markup=keyboard)

        bot.register_next_step_handler(message, handle_photo, bot, category, subcategory, name, description)


def save_photos_and_continue(message, bot, category, subcategory, name, description):
    user_id = message.from_user.id
    if user_id in user_photos and user_photos[user_id]:
        unique_folder_name = str(uuid.uuid4())
        folder_path = os.path.join("photos", unique_folder_name)

        os.makedirs(folder_path, exist_ok=True)

        for i, photo in enumerate(user_photos[user_id]):
            file_info = bot.get_file(photo.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_path = os.path.join(folder_path, f"photo_{i+1}.jpg")

            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)

        #bot.send_message(message.chat.id, f"Фотографії успішно збережено у папці {unique_folder_name}.")
        bot.send_message(message.chat.id, price_input_message, parse_mode='HTML', reply_markup=cancel_action)
        user_photos.clear()
        bot.register_next_step_handler(message, get_advertisement_price, bot, category, subcategory, name, description, unique_folder_name)
    else:
        bot.send_message(message.chat.id, "<b>😥Ви не додали жодної фотографіi</b>\n\n<i>❗️ Будь ласка, додайте хоча б одну фотографію перед тим, як зберегти</i>")
        bot.register_next_step_handler(message, handle_photo, bot, category, subcategory, name, description)


def get_advertisement_price(message: Message, bot: TeleBot, category: str, subcategory: str, name: str, description: str, unique_folder_name: str):
    if message.text == '❌ Скасувати дію':
        cancel_advertisement_creation(message, bot)
        return

    try:
        price = float(message.text)

        if price < 0 or price > 100000000:
            bot.send_message(message.chat.id, price_error_message, parse_mode='HTML')
            bot.register_next_step_handler(message, get_advertisement_price, bot, category, subcategory, name,
                                           description, unique_folder_name)

        else:

            markup_condition = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup_condition.add(types.KeyboardButton('Нове'), types.KeyboardButton('Вживане'))
            markup_condition.add(types.KeyboardButton("❌ Скасувати дію"))

            bot.send_message(message.chat.id, condition_selection_message, parse_mode='HTML',
                             reply_markup=markup_condition)

            bot.register_next_step_handler(message, get_advertisement_condition, bot, category, subcategory, name, description, unique_folder_name, price)

    except ValueError:
        bot.send_message(message.chat.id, non_correct_price_error_message, parse_mode='HTML')
        bot.register_next_step_handler(message, get_advertisement_price, bot, category, subcategory, name, description, unique_folder_name)


def get_advertisement_condition(message: Message, bot: TeleBot, category: str, subcategory: str, name: str, description: str, unique_folder_name: str, price: float):
    if message.text == '❌ Скасувати дію':
        cancel_advertisement_creation(message, bot)
        return

    condition = message.text

    if condition not in ['Нове', 'Вживане']:
        markup_condition = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup_condition.add(types.KeyboardButton('Нове'), types.KeyboardButton('Вживане'))
        markup_condition.add(types.KeyboardButton("❌ Скасувати дію"))

        bot.send_message(message.chat.id, incorrect_condition_message, parse_mode='HTML', reply_markup=markup_condition)
        bot.register_next_step_handler(message, get_advertisement_condition, bot, category, subcategory, name, description, unique_folder_name, price)
        return

    else:
        markup_region = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for region in regions:
            markup_region.add(types.KeyboardButton(region))
        markup_region.add(types.KeyboardButton("❌ Скасувати дію"))

        bot.send_message(message.chat.id, region_selection_message, parse_mode='HTML', reply_markup=markup_region)
        bot.register_next_step_handler(message, region_selection, bot, category, subcategory, name, description, unique_folder_name, price, condition)


def region_selection(message: Message, bot: TeleBot, category: str, subcategory: str, name: str, description: str, unique_folder_name: str, price: float, condition: str):
    if message.text == '❌ Скасувати дію':
        cancel_advertisement_creation(message, bot)
        return

    region = message.text
    cities_list = cities.get(region, [])
    markup_cities = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if cities_list:
        for city in cities_list:
            markup_cities.add(types.KeyboardButton(city))
        markup_cities.add(types.KeyboardButton("❌ Скасувати дію"))

        bot.send_message(message.chat.id, select_city_message(region), parse_mode='HTML', reply_markup=markup_cities)
        bot.register_next_step_handler(message, city_selection, bot, category, subcategory, name, description, unique_folder_name, price, condition, region)
    else:
        markup_region = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for region in regions:
            markup_region.add(types.KeyboardButton(region))
        markup_region.add(types.KeyboardButton("❌ Скасувати дію"))
        bot.send_message(message.chat.id, error_region_selection_message, parse_mode='HTML', reply_markup=markup_region)
        bot.register_next_step_handler(message, region_selection, bot, category, subcategory, name, description,
                                       unique_folder_name, price, condition)


def city_selection(message: Message, bot: TeleBot, category: str, subcategory: str, name: str, description: str, unique_folder_name: str, price: float, condition: str, region: str):
    if message.text == '❌ Скасувати дію':
        cancel_advertisement_creation(message, bot)
        return

    adv_id = generate_unique_advertisement_id()
    user_id = message.from_user.id

    city = message.text

    cities_list = cities.get(region, [])
    if city not in cities_list:
        bot.send_message(message.chat.id, error_city_selection_message, parse_mode='HTML')
        bot.register_next_step_handler(message, city_selection, bot, category, subcategory, name, description, unique_folder_name, price, condition, region)
        return

    bot.send_message(message.chat.id, announcement_success_message, parse_mode='HTML', reply_markup=keyboard_menu)
    create_advertisement(adv_id, user_id, category, subcategory, name, description, unique_folder_name, price, condition, region, city)

    notification_new_ad(bot, name, user_id)


def generate_unique_advertisement_id():
    while True:
        unique_id = "ad_" + str(uuid.uuid4())
        existing_ad = get_ads_id(unique_id)

        if existing_ad is None:
            return unique_id