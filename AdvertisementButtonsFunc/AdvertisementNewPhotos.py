import os
import uuid

from telebot import types

from DataBase.Advertisement_database import set_new_photo_folder_with_photos_ad, get_all_info_about_advertisement, \
    change_status
from Markups.markups import cancel_action
from Markups.menu_markups import keyboard_menu, markup_ad_types
from Messages.StartCreatingAdMessages import photo_error_message
from Notifications.ModeratorNotifications import notification_new_description_ad, notification_new_photos_ad
from OtherTools.AdvertisementChangesLogging import save_new_changes
from OtherTools.CancelAction import cancel_change_photos_ad_action


def set_new_photos_ad_btn(bot, call, ad_id):
    photo_input_msg = (
        "<b>📸 Надішліть нові фото оголошення для оголошення</b>\n\n"
        "<b>📝 Примітка:</b> <i>можна надіслати до 5 фотографій (НАДСИЛАТИ ПО 1шт.)</i>"
    )
    bot.send_message(call.message.chat.id, photo_input_msg, parse_mode='HTML', reply_markup=cancel_action)
    bot.register_next_step_handler(call.message, lambda msg: handle_photo(bot, msg, ad_id))


user_photos = {}


def handle_photo(bot, message, ad_id):
    if message.text == '❌ Скасувати дію':
        cancel_change_photos_ad_action(message, bot)
        user_photos.clear()
        return

    elif message.text == '🔥 Це все, зберегти фото':
        save_photos_and_continue(bot, message, ad_id)
        return

    if not message.photo:
        bot.send_message(message.chat.id, photo_error_message, parse_mode='HTML')
        bot.register_next_step_handler(message, lambda msg: handle_photo(bot, msg, ad_id))
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

        bot.register_next_step_handler(message, lambda msg: handle_photo(bot, msg, ad_id))


def save_photos_and_continue(bot, message, ad_id):
    user_id = message.from_user.id
    ad_info = get_all_info_about_advertisement(ad_id)


    if user_id in user_photos and user_photos[user_id]:
        unique_folder_name = str(uuid.uuid4())
        folder_path = os.path.join("photos", unique_folder_name)

        os.makedirs(folder_path, exist_ok=True)

        for i, photo in enumerate(user_photos[user_id]):
            file_info = bot.get_file(photo.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_path = os.path.join(folder_path, f"photo_{i + 1}.jpg")

            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)

        ad_name = ad_info[4]
        telegram_id = ad_info[1]

        bot.send_message(message.chat.id, f"<b>✔️ Фотографії оголошення '{ad_name}' успішно оновлено</b>\n\n<i><b>📝 Примітка:</b> оголошення знаходиться на модерації. Наші модератори перевірять Ваше оголошення якнайшвидше і його зможуть побачити інші люди</i>", reply_markup=markup_ad_types)
        set_new_photo_folder_with_photos_ad(ad_id, unique_folder_name)
        user_photos.clear()

        text = 'photos_log'
        save_new_changes(ad_id, text, old=None, new=None)

        new_status = 'on moderation'
        change_status(ad_id, new_status)
        notification_new_photos_ad(bot, ad_name, telegram_id)
    else:
        bot.send_message(message.chat.id,
                         "<b>😥Ви не додали жодної фотографіi</b>\n\n<i>❗️ Будь ласка, додайте хоча б одну фотографію перед тим, як зберегти</i>")
        bot.register_next_step_handler(message, lambda msg: handle_photo(bot, msg, ad_id))
