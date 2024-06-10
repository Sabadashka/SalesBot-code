from telebot import types

from DataBase.Advertisement_database import set_new_category_ad, set_new_subcategory_ad, get_all_info_about_advertisement
from Markups.creating_ad_category_region_markups import categories, subcategories
from Markups.menu_markups import moderator_moderation_exit


def moderator_process_new_category_ad_input(bot, call, ad_id):
    info_ad = get_all_info_about_advertisement(ad_id)

    category_ad = info_ad[2]
    name = info_ad[4]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for category in categories:
        markup.add(types.KeyboardButton(category))
    markup.add(types.KeyboardButton("❌ Скасувати дію"))

    bot.send_message(call.message.chat.id, f"❗️ *[MODERATOR]* Введіть нову категорію для оголошення *'{name}'*",
                     parse_mode='Markdown', reply_markup=markup)

    bot.register_next_step_handler(call.message, get_category, bot, ad_id)


def get_category(message, bot, ad_id):
    category = message.text
    subcategory_list = subcategories.get(category, [])

    if category in categories:
        if subcategory_list:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, )
            for subcategory in subcategory_list:
                markup.add(types.KeyboardButton(subcategory))
            markup.add(types.KeyboardButton("❌ Скасувати дію"))

            set_new_category_ad(ad_id, category)

            bot.send_message(message.chat.id, f"❗️ *[MODERATOR]* Виберіть підкатегорію для {category}:",
                             parse_mode='Markdown', reply_markup=markup)
            bot.register_next_step_handler(message, get_subcategory, bot, category, ad_id)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        for category in categories:
            markup.add(types.KeyboardButton(category))
        markup.add(types.KeyboardButton("❌ Скасувати дію"))
        bot.send_message(message.chat.id, "❗️ *[MODERATOR]* Потрібно обрати категорію зі списку", parse_mode='Markdown',
                         reply_markup=markup)
        bot.register_next_step_handler(message, get_category, bot, ad_id)


def get_subcategory(message, bot, current_category, ad_id):
    subcategory = message.text

    subcategory_list = subcategories.get(current_category, [])
    if subcategory not in subcategory_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, )
        for subcategory in subcategory_list:
            markup.add(types.KeyboardButton(subcategory))
        markup.add(types.KeyboardButton("❌ Скасувати дію"))

        bot.send_message(message.chat.id, "❗️ *[MODERATOR]* Потрібно обрати підкатегорію зі списку",
                         parse_mode='Markdown', reply_markup=markup)
        bot.register_next_step_handler(message, get_subcategory, bot, current_category, ad_id)

    else:

        set_new_subcategory_ad(ad_id, subcategory)
        bot.send_message(message.chat.id,
                         f"❗️ *[MODERATOR]* Категорію змінено на *'{current_category}'*, підкатегорію змінено на *'{subcategory}'*",
                         parse_mode='Markdown', reply_markup=moderator_moderation_exit)