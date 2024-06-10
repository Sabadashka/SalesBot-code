from telebot import types

#
profile_settings_btn = types.InlineKeyboardButton('⚙️ Налаштування облікового запису', callback_data='profile_settings')
# delete_profile_btn = types.InlineKeyboardButton("🚫 Видалити аккаунт", callback_data='delete_profile')
profile_settings_markups = types.InlineKeyboardMarkup(row_width=1)
profile_settings_markups.add(profile_settings_btn)

#
# edit_login_btn = types.InlineKeyboardButton("🔐 Змінити логін", callback_data='new_login')
edit_name_btn = types.InlineKeyboardButton("👤 Змінити ім'я", callback_data='new_name')
edit_mail_btn = types.InlineKeyboardButton("✉️ Змінити пошту ", callback_data='new_mail')
delete_profile_btn = types.InlineKeyboardButton("🚫 Видалити аккаунт", callback_data='delete_profile')
# edit_phone_number_btn = types.InlineKeyboardButton("📞 Змінити номер телефону", callback_data='new_phone_number')
go_from_edit_btn = types.InlineKeyboardButton("◀️ Повернутися назад", callback_data='go_from_edit')

profile_editing_markups = types.InlineKeyboardMarkup(row_width=1)
profile_editing_markups.add(edit_name_btn, edit_mail_btn, delete_profile_btn, go_from_edit_btn)

cancel_name_edit_btn = types.KeyboardButton("❌ Скасувати зміну імені")
cancel_name_edit_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel_name_edit_markup.add(cancel_name_edit_btn)

cancel_login_edit_btn = types.KeyboardButton("❌ Скасувати зміну логіну")
cancel_login_edit_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel_login_edit_markup.add(cancel_login_edit_btn)

#
cancel_phone_number_edit_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel_phone_number_edit_btn = types.KeyboardButton("❌ Скасувати зміну номеру телефону")
cancel_phone_number_edit_markup.add(cancel_phone_number_edit_btn)

cancel_mail_edit_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel_mail_edit_btn = types.KeyboardButton("❌ Скасувати зміну скиньки")
cancel_mail_edit_markup.add(cancel_mail_edit_btn)
