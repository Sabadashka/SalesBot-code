from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telebot import types

###
start_bot_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_bot = types.KeyboardButton("🚀 Почати роботу з ботом")
start_bot_keyboard.add(start_bot)

###
markup_reg = types.ReplyKeyboardMarkup(resize_keyboard=True)
registration_button = types.KeyboardButton("📝 Реєстрація")
markup_reg.add(registration_button)

###
cancel_action = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel_button = InlineKeyboardButton("❌ Скасувати дію", callback_data='cancel_advertisement_creation')
cancel_action.add(cancel_button)

cancel_reg_btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel_reg_button = InlineKeyboardButton("❌ Скасувати реєстрацію", callback_data='cancel_reg_btn')
cancel_reg_btn.add(cancel_reg_button)


finish_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
finish_keyboard_button = InlineKeyboardButton("Завершити надсилання фото", callback_data='save_photo')
finish_keyboard.add(finish_keyboard_button)