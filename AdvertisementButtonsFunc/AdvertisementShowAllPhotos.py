import os
from telebot import types
from DataBase.Advertisement_database import get_all_info_about_advertisement


def show_all_photos_by_advertisement_id(bot, call, ad_id):
    ad_info = get_all_info_about_advertisement(ad_id)
    ad_name = ad_info[4]
    name = f"<b>📷 Фото оголошення</b> \n<i>'{ad_name}'</i>"
    folder_name = ad_info[6]
    photo_folder_path = os.path.join("photos", folder_name)

    photo_file_paths = [os.path.join(photo_folder_path, photo_name) for photo_name in os.listdir(photo_folder_path)]

    if len(photo_file_paths) == 1:
        bot.send_message(call.message.chat.id, "😥 <b>У цього оголошення лише одна фотографія</b>", reply_to_message_id=call.message.message_id, parse_mode='HTML')
    else:
        media = [types.InputMediaPhoto(open(photo_path, 'rb'), caption=name if i == 0 else None, parse_mode='HTML') for
                 i, photo_path in enumerate(photo_file_paths)]
        bot.send_media_group(call.message.chat.id, media, reply_to_message_id=call.message.message_id)