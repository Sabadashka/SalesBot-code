import os
import random

import telebot
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
from telebot import types
import settings
from AdminAndModeratorButtonsFunc.ModeratorAdvertisementNewDescription import moderator_set_new_description_ad
from AdminAndModeratorButtonsFunc.ModeratorAdvertisementNewName import moderator_set_new_name_ad
from AdminAndModeratorButtonsFunc.ModeratorConfirmAdPublication import publish_ad, delete_ad
from AdminAndModeratorButtonsFunc.ModeratorAdvertisementNewCategory import moderator_process_new_category_ad_input
from AdvertisementButtonsFunc.ActivateMyAd import activate_my_ad
from AdvertisementButtonsFunc.AddToFavorites import add_to_favorites
from AdminAndModeratorButtonsFunc.AdminResponseToViolation import yes_violation, no_violation
from AdvertisementButtonsFunc.AdvertisementExtend import extend_my_ad
from AdvertisementButtonsFunc.AdvertisementNewDescription import set_new_description_ad_btn
from AdvertisementButtonsFunc.AdvertisementNewLocation import process_new_location_ad_input
from AdvertisementButtonsFunc.AdvertisementNewName import set_new_name_ad_btn
from AdvertisementButtonsFunc.AdvertisementNewPhotos import set_new_photos_ad_btn
from AdvertisementButtonsFunc.AdvertisementNewPrice import set_new_price_ad_btn
from AdvertisementButtonsFunc.AdvertisementShowAllPhotos import show_all_photos_by_advertisement_id
from AdvertisementButtonsFunc.Complaint import complaint
from AdvertisementButtonsFunc.DeactivateMyAd import deactivate_my_ad
from AdvertisementButtonsFunc.DeleteFromFavorites import delete_favorite
from AdvertisementButtonsFunc.DeleteMyAd import delete_my_ad
from AdvertisementButtonsFunc.OwnerInfo import show_owner_info
from DataBase.Advertisement_database import check_and_deactivate_ads, print_ads_for_deactivation
from DataBase.BlockedUsers_database import get_all_data_blocked_user, \
    check_and_unblock_users
from DataBase.Notified_database import check_notified, create_new_notified
from DataBase.Users_database import get_user_data
from FunctionsMenuBtn.FunctionsAdminMenuBtn.AdminCheckQuestions import start_creating_answer, reject_answer
from FunctionsMenuBtn.UserCreateAdvertisement import start_creating_advertisement, cancel_advertisement_creation
from FunctionsMenuBtn.MainMenu import main_menu
from FunctionsMenuBtn.UserShowNotifications import display_notifications, show_notification
from FunctionsMenuBtn.UserCreateQuestion import start_creating_question
from Messages.HelpMessage import message_help
from OtherTools.CancelAction import cancel_registration_button
from FunctionsMenuBtn.UserShowFavorites import show_user_favorites_with_status_published, print_favorite
from FunctionsMenuBtn.UserShowAdvertisements import request_ad_type, \
    show_user_advertisements_with_status_on_moderation, show_user_advertisements_with_status_published, \
    show_user_advertisements_with_status_deleted, show_user_advertisements_with_status_deactivated, send_advertisement
from FunctionsMenuBtn.UserCreateProfile import start_creating_user
from Markups.categories_markups import category_markup, children_world_markup, vehicle_markup, realty_markup, \
    spare_parts_markup, job_markup, animals_markup, house_garden_markup, electronics_markup, business_services_markup, \
    rent_hire_markup, fashion_style_markup, hobbies_markup
from Markups.menu_markups import keyboard_menu, admin_keyboard_menu, moderator_keyboard_menu
from FunctionsMenuBtn.UserShowProfile import show_user_profile_back
from OtherTools.CheckMessageInterval import check_message_interval, warning_phrases
from OtherTools.CheckRole import check_role_for_moderation, check_exists_moderation, check_role_for_complaints, \
    check_exists_complaints, check_role_for_show_users, check_role_for_show_moderators, check_role_for_show_admins, \
    check_role_for_show_blocked_users, check_role_for_block_user, check_role_for_unblock_user, \
    check_role_for_database_actions, role_check_to_return_to_menu, check_role_to_enter_moderator_panel, \
    check_role_to_enter_admin_panel, check_role_for_change_role_user, \
    check_role_to_return_to_apanel_menu, check_role_for_show_top_moderators, blocked_user_info, \
    check_role_for_make_notification, check_role_for_show_questions, check_role_exit_from_top_moderators, \
    check_role_for_show_top_moderators_by_moderation, check_role_for_show_top_moderators_by_answers, \
    check_role_for_choice_type_show_users, check_exist_answer
from OtherTools.GetUserNameTelegram import get_username_from_acc_id
from Messages.StartBotMessages import send_message_with_username
from OtherTools.LoggingSetup import setup_menu_logger
from SearchAds.ClearFilters import handle_clear_search, handle_clear_matches_text, handle_clear_all_filters_search, \
    handle_clear_condition, handle_clear_category_subcategory, handle_clear_price_max_min, \
    handle_clear_location_region_city, handle_clear_sort_by
from SearchAds.Inputs.InputCategorySubcategory import process_category_step
from SearchAds.Inputs.InputCondition import process_condition_step
from SearchAds.Inputs.InputLocation import process_location_region_step
from SearchAds.Inputs.InputMatchesText import process_matches_text_step
from SearchAds.Inputs.InputPriceMinMax import process_price_step
from SearchAds.Inputs.InputSortBy import process_sort_by
from SearchAds.SearchAds import handle_start_search_advertisements, handle_previous_advertisement, \
    handle_next_advertisement, get_user_search
# from SearchAds.SearchAds import send_next_advertisement
from SearchAds.SearchMessage import search_message, search_filters_message
from UserProfileButtonsFunctions.UserDeleteProfile import delete_account, no_delete_profile, yes_delete_profile
from Markups.user_profile_markups import profile_editing_markups, profile_settings_markups
from UserProfileButtonsFunctions.UserNewMail import process_change_mail
from UserProfileButtonsFunctions.UserNewName import new_name


bot = telebot.TeleBot(settings.botAPI)


@bot.message_handler(commands=["apanel"])
def connect_admin_panel(message):
    acc_id = message.chat.id
    user_data = get_user_data(acc_id)

    if user_data is not None:
        role = user_data.get('role', 2)
        if role == 2:
            bot.send_message(message.chat.id, "❗️ У Вас є доступ до панелі *Адміністратора*!", parse_mode='Markdown',
                             reply_markup=admin_keyboard_menu)
        elif role == 1:
            bot.send_message(message.chat.id, "❗️ У Вас є доступ до панелі *Модератора*!", parse_mode='Markdown',
                             reply_markup=moderator_keyboard_menu)
        else:
            bot.send_message(message.chat.id, "❗️ Ви не *Адміністратор*/*Модератор*. У Вас немає таких прав!",
                             parse_mode='Markdown',
                             reply_markup=keyboard_menu)


@bot.message_handler(commands=["start"])
def start(message):
    # запит на БД
    acc_id = message.chat.id
    user_data = get_user_data(acc_id)

    if user_data is None:
        username = get_username_from_acc_id(bot, acc_id)
        send_message_with_username(bot, message, username)

    else:
        role = user_data.get('role', 2)

        if role == 2:
            role_info = "👑 Ви авторизовані як *Адміністратор*"
            bot.send_message(message.chat.id, role_info, reply_markup=admin_keyboard_menu, parse_mode='Markdown')
            bot.send_message(message.chat.id, '❗️ Оберіть пункт в меню', reply_markup=keyboard_menu)

        elif role == 1:
            role_info = "🛡️ Ви авторизовані як *Модератор*"
            bot.send_message(message.chat.id, role_info, reply_markup=admin_keyboard_menu, parse_mode='Markdown')
            bot.send_message(message.chat.id, '❗️ Оберіть пункт в меню', reply_markup=keyboard_menu)

        elif role == 0:
            bot.send_message(message.chat.id, '❗️ У Вас вже існує обліковий запис')
            bot.send_message(message.chat.id, '❗️ Оберіть пункт в меню', reply_markup=keyboard_menu)

        elif role == -1:
            blocked_user_data = get_all_data_blocked_user(acc_id)
            if blocked_user_data:
                blocked_user_info(bot, message, acc_id)

            else:
                bot.send_message(message.chat.id, f'❗️ Щось пішло не так... Зверніться до адміністрації...')
            # bot.send_message(message.chat.id, 'Виберіть пункт в меню', reply_markup=keyboard_menu)

        else:
            bot.send_message(message.chat.id, '️❗️ У Вас немає ролі, якісь проблеми з аккаунтом.\n Зверніться в '
                                              'підтримку.')


menu_logger = setup_menu_logger()


# Окрема функція для обробки вибору пунктів меню
@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    if message.chat.type == 'private':
        # запит на БД
        acc_id = message.chat.id
        user_data = get_user_data(acc_id)
        # check_blocked_role(bot, message, role, acc_id)

        if user_data is not None:
            role = user_data.get('role', 2)

            if role == -1:
                blocked_user_info(bot, message, acc_id)
                return

            if not check_message_interval(acc_id, message.text, interval_seconds=3):
                warning_message = '<b>❗️ Не потрібно так часто натискати кнопки</b>\n\n'
                # warning_message += random.choice(warning_phrases)
                warning_message += random.sample(warning_phrases, 1)[0]
                bot.send_message(acc_id, warning_message, parse_mode='HTML')
                return

            menu_logger.info(f'ID: {acc_id} >>> {message.text}')

            if message.text == '📝 Створити оголошення':
                start_creating_advertisement(bot, message)

            elif message.text == '🔍 Пошук оголошень':
                user_search = get_user_search(acc_id)
                search_message(bot, message, user_search)

            elif message.text == '🚀 Виконати пошук':
                handle_start_search_advertisements(bot, message)

            elif message.text == '◀️ Вийти з пошуку':
                handle_clear_search(bot, message, acc_id)

            elif message.text == '◀️ Попереднє оголошення':
                handle_previous_advertisement(bot, message)

            elif message.text == 'Наступне оголошення ▶️':
                handle_next_advertisement(bot, message)

            elif message.text == '❌ Завершити пошук':
                handle_clear_search(bot, message, acc_id)

            elif message.text == '📂 Мої оголошення':
                # show_user_advertisements(bot, message)
                request_ad_type(bot, message)

            elif message.text == '📌 Активні оголошення':
                show_user_advertisements_with_status_published(bot, message)
                # request_ad_type(bot, message)

            elif message.text == '⏳ Очікують перевірку':
                show_user_advertisements_with_status_on_moderation(bot, message)

            elif message.text == '🚫 Деактивовані оголошення':
                show_user_advertisements_with_status_deactivated(bot, message)

            elif message.text == '🗑️ Видалені оголошення':
                show_user_advertisements_with_status_deleted(bot, message)

            elif message.text == '◀️ Головне меню':
                main_menu(bot, message)

            elif message.text == '👤 Мій обліковий запис':
                # show_user_profile(bot, message)
                profile_text = show_user_profile_back(message)

                # Відправлення інформації про профіль у чат
                bot.send_message(message.chat.id, profile_text, parse_mode="HTML",
                                 reply_markup=profile_settings_markups)

            elif message.text == '❓ Допомога':
                help_markup = types.InlineKeyboardMarkup(row_width=1)
                question_button = types.InlineKeyboardButton("❓ У мене є запитання", callback_data='make_question')
                help_markup.add(question_button)

                bot.send_message(message.chat.id, message_help, parse_mode='HTML', reply_markup=help_markup)

            elif message.text == '🔔️ Сповіщення':
                # display_notifications(bot, message, acc_id)
                display_notifications(bot, message)

            elif message.text == '❤️ Вибрані':
                show_user_favorites_with_status_published(bot, message)

            # admin_panel
            elif message.text == '👑️ Адмінська панель':
                check_role_to_enter_admin_panel(role, bot, message)

            elif message.text == '🛡️ Модераторська панель':
                check_role_to_enter_moderator_panel(role, bot, message)

            elif message.text == "◀️ Вийти в головне меню":
                role_check_to_return_to_menu(role, bot, message)

            # [MODERATOR] Перевірка оголошення для модератора

            elif message.text == "👁 Перевірити оголошення":
                check_role_for_moderation(role, bot, message)

            elif message.text == '➡️ Наступне оголошення':
                check_role_for_moderation(role, bot, message)

            elif message.text == '◀️ Завершити перегляд оголошень':
                check_exists_moderation(role, acc_id, bot, message)

            # ---------------------------------

            # [ADMIN]

            elif message.text == "⚠️ Переглянути скарги":
                check_role_for_complaints(role, bot, message)

            elif message.text == '➡️ Наступна скарга':
                check_role_for_complaints(role, bot, message)

            elif message.text == '◀️ Завершити перегляд скарг':
                check_exists_complaints(role, acc_id, bot, message)

            elif message.text == '🗃️ Дії з Базою Даних':
                check_role_for_database_actions(role, bot, message)

            elif message.text == '👥 Список користвувачів':
                check_role_for_choice_type_show_users(role, bot, message)

            elif message.text == '👥 Користувачів':
                check_role_for_show_users(role, bot, message)

            elif message.text == '🛡️ Модераторів':
                check_role_for_show_moderators(role, bot, message)

            elif message.text == '👑️ Адміністраторів':
                check_role_for_show_admins(role, bot, message)

            elif message.text == '🚫 Заблокованих':
                check_role_for_show_blocked_users(role, bot, message)

            elif message.text == '❌ Не показувати нічого':
                check_role_for_database_actions(role, bot, message)

            elif message.text == '🔒 Заблокувати користувача':
                check_role_for_block_user(role, acc_id, bot, message)

            elif message.text == '🔓 Розблокувати користувача':
                check_role_for_unblock_user(role, bot, message)

            elif message.text == '📢 Створити сповіщення':
                check_role_for_make_notification(role, bot, message)

            elif message.text == '🎭 Змінити роль':
                check_role_for_change_role_user(role, bot, message)

            elif message.text == '◀️ Повернутися назад':
                check_role_to_return_to_apanel_menu(role, bot, message)

            # ---------------------------------

            elif message.text == "🏆 Топ модераторів":
                check_role_for_show_top_moderators(role, bot, message)

            elif message.text == "🏆 [Перевірка оголошень]":
                check_role_for_show_top_moderators_by_moderation(role, bot, message)

            elif message.text == "🏆 [Відповіді на запитання]":
                check_role_for_show_top_moderators_by_answers(role, bot, message)

            elif message.text == "◀️ Назад":
                check_role_exit_from_top_moderators(role, bot, message)

            elif message.text == "📝 Переглянути запитання":
                check_role_for_show_questions(role, bot, message)

            elif message.text == "Наступне запитання ➡️":
                check_role_for_show_questions(role, bot, message)

            elif message.text == "◀️ Завершити перегляд запитань":
                check_exist_answer(role, acc_id, bot, message)

            else:
                bot.send_message(message.chat.id, '❗️ Невідома команда...', reply_markup=keyboard_menu)

        elif message.text == '📝 Реєстрація':
            start_creating_user(bot, message)

        elif message.text == '🚀 Почати роботу з ботом':
            # start(message)
            start_creating_user(bot, message)

        else:
            bot.send_message(message.chat.id, 'Напишіть команду /start для початку роботи з Ботом!')


@bot.callback_query_handler(func=lambda call: call.data.startswith('make_question'))
def user_make_question(call):
    acc_id = call.message.chat.id
    start_creating_question(bot, call, acc_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('answer_button'))
def user_make_question(call):
    question_id = call.data[len('answer_button'):]
    acc_id = call.message.chat.id
    start_creating_answer(bot, call, acc_id, question_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('reject_button'))
def user_make_question(call):
    question_id = call.data[len('reject_button'):]
    acc_id = call.message.chat.id
    reject_answer(bot, call, acc_id, question_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('show_notification'))
def show_full_notification(call):
    notification_id = call.data[len('show_notification'):]
    show_notification(bot, call, notification_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('go_back_notifications'))
def show_notifications(call):
    notification_id = call.data[len('go_back_notifications'):]
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    display_notifications(bot, call)


@bot.callback_query_handler(func=lambda call: call.data == 'profile_settings')
def profile_editor(call):
    updated_message_text = f"❗️ Оберіть, що саме хочете змінити в *профілі*:"

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=updated_message_text,
                          reply_markup=profile_editing_markups,
                          parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == 'go_from_edit')
def profile(call):
    profile_text = show_user_profile_back(call.message)

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=profile_text,
                          reply_markup=profile_settings_markups,
                          parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == 'new_name')
def set_new_name_profile(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)

    new_name(bot, call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'new_mail')
def set_new_mail_profile(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)

    process_change_mail(bot, call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'delete_profile')
def delete_profile(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    delete_account(bot, call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == 'yes_btn')
def yes_delete_profile_btn(call):
    acc_id = call.message.chat.id
    message_id = call.message.message_id

    yes_delete_profile(bot, call.message, acc_id, message_id)


@bot.callback_query_handler(func=lambda call: call.data == 'no_btn')
def no_delete_profile_btn(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    no_delete_profile(bot, call.message, chat_id, message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('show_advertisement'))
def show_advertisement(call):
    ad_id = call.data[len('show_advertisement'):]
    # print(ad_id)
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    send_advertisement(bot, call.message, ad_id)


@bot.callback_query_handler(func=lambda call:call.data.startswith('show_favorite'))
def show_favorite(call):
    ad_id = call.data[len('show_favorite'):]
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    print_favorite(bot, call.message, ad_id)



@bot.callback_query_handler(func=lambda call: call.data.startswith('deactivate_ad'))
def handle_deactivate_my_advertisement_callback(call):
    ad_id = call.data[len('deactivate_ad'):]

    deactivate_my_ad(bot, call, ad_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('show_all_photos_button'))
def handle_show_all_photos_ad_callback(call):
    ad_id = call.data[len('show_all_photos_button'):]

    show_all_photos_by_advertisement_id(bot, call, ad_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('activate_ad'))
def handle_activate_my_advertisement_callback(call):
    ad_id = call.data[len('activate_ad'):]

    activate_my_ad(bot, call, ad_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_ad'))
def handle_delete_my_advertisement_callback(call):
    ad_id = call.data[len('delete_ad'):]

    delete_my_ad(bot, call, ad_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('extend_ad'))
def handle_extend_my_advertisement_callback(call):
    ad_id = call.data[len('extend_ad'):]
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)

    extend_my_ad(bot, call.message, chat_id, ad_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_ad'))
def handle_edit_advertisement_callback(call):
    ad_id = call.data[len('edit_ad'):]

    new_photos_btn = types.InlineKeyboardButton("📸 Оновити фото", callback_data=f'new_photos{ad_id}')
    edit_ad_name_btn = types.InlineKeyboardButton("✏️ Змінити назву", callback_data=f'ad_new_name{ad_id}')
    edit_ad_description_btn = types.InlineKeyboardButton("📝 Змінити опис", callback_data=f'ad_new_description{ad_id}')
    edit_ad_price_btn = types.InlineKeyboardButton("💰 Змінити ціну ", callback_data=f'ad_new_price{ad_id}')
    edit_ad_location_btn = types.InlineKeyboardButton("📍 Змінити місцезнаходження",
                                                      callback_data=f'ad_new_location{ad_id}')
    go_from_edit_btn = types.InlineKeyboardButton("❌ Нічого не змінювати", callback_data='go_from_ad_edit')

    advertisement_editing_markups = types.InlineKeyboardMarkup(row_width=1)
    advertisement_editing_markups.add(new_photos_btn, edit_ad_name_btn, edit_ad_description_btn, edit_ad_price_btn,
                                      edit_ad_location_btn, go_from_edit_btn)

    updated_message_text = f"❗️ Оберіть, що саме хочете змінити в *оголошенні*:"

    bot.send_message(call.message.chat.id, updated_message_text, reply_to_message_id=call.message.message_id,
                     parse_mode='Markdown', reply_markup=advertisement_editing_markups)


# Нові фото для оголошення
@bot.callback_query_handler(func=lambda call: call.data.startswith('new_photos'))
def handle_edit_advertisement_new_photos_callback(call):
    ad_id = call.data[len('new_photos'):]
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)

    set_new_photos_ad_btn(bot, call, ad_id)


# Нове ім'я для оголошення
@bot.callback_query_handler(func=lambda call: call.data.startswith('ad_new_name'))
def handle_edit_advertisement_new_name_callback(call):
    ad_id = call.data[len('ad_new_name'):]
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)

    set_new_name_ad_btn(bot, call, ad_id, chat_id)


# Новий опис для оголошення
@bot.callback_query_handler(func=lambda call: call.data.startswith('ad_new_description'))
def handle_edit_advertisement_new_name_callback(call):
    ad_id = call.data[len('ad_new_description'):]
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)

    set_new_description_ad_btn(bot, call, ad_id, chat_id)


# Нова ціна для оголошення
@bot.callback_query_handler(func=lambda call: call.data.startswith('ad_new_price'))
def handle_edit_advertisement_new_name_callback(call):
    ad_id = call.data[len('ad_new_price'):]
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)

    # set_new_price_ad(bot, call, ad_id)
    set_new_price_ad_btn(bot, call, ad_id, chat_id)


# Нове місцезнаходження для оголошення
@bot.callback_query_handler(func=lambda call: call.data.startswith('ad_new_location'))
def handle_edit_advertisement_new_name_callback(call):
    ad_id = call.data[len('ad_new_location'):]
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)

    process_new_location_ad_input(bot, call, ad_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('go_from_ad_edit'))
def handle_edit_advertisement_new_name_callback(call):
    ad_id = call.data[len('go_from_ad_edit'):]
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    bot.send_message(call.message.chat.id, "❗️ Ви обрали нічого не змінювати")


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_from_favorites_btn'))
def handle_delete_advertisement_from_favorites_callback(call):
    ad_id = call.data[len('delete_from_favorites_btn'):]

    delete_favorite(bot, call, ad_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('add_to_favorites_btn'))
def handle_add_advertisement_to_favorites_callback(call):
    telegram_id = call.message.chat.id
    ad_id = call.data[len('add_to_favorites_btn'):]

    add_to_favorites(bot, call, telegram_id, ad_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('complain_btn'))
def handle_complaint_ad(call):
    telegram_id = call.message.chat.id
    ad_id = call.data[len('complain_btn'):]

    complaint(bot, call, ad_id, telegram_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('no_violation_btn'))
def handle_no_violation(call):
    complaint_id = call.data[len('no_violation_btn'):]

    no_violation(bot, call, complaint_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('yes_violation_btn'))
def handle_detected_violation(call):
    complaint_id = call.data[len('yes_violation_btn'):]

    yes_violation(bot, call, complaint_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('moderator_name_btn'))
def handle_moderator_name(call):
    ad_id = call.data[len('moderator_name_btn'):]
    # bot.send_message(call.message.chat.id, 'В розробці')

    moderator_set_new_name_ad(bot, call, ad_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('moderator_category_btn'))
def handle_moderator_description(call):
    ad_id = call.data[len('moderator_category_btn'):]

    moderator_process_new_category_ad_input(bot, call, ad_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('moderator_description_btn'))
def handle_detected_violation(call):
    ad_id = call.data[len('moderator_description_btn'):]

    moderator_set_new_description_ad(bot, call, ad_id)


# Опублікувати оголошення кнопка
@bot.callback_query_handler(func=lambda call: call.data.startswith('moderator_publish_ad_btn'))
def handle_delete_my_advertisement_callback(call):
    ad_id = call.data[len('moderator_publish_ad_btn'):]
    telegram_id = call.message.chat.id

    publish_ad(bot, call, ad_id, telegram_id)


# Видалити оголошення кнопка
@bot.callback_query_handler(func=lambda call: call.data.startswith('moderator_delete_ad_btn'))
def handle_delete_my_advertisement_callback(call):
    ad_id = call.data[len('moderator_delete_ad_btn'):]
    telegram_id = call.message.chat.id

    delete_ad(bot, call, ad_id, telegram_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('show_contacts_btn'))
def handle_detected_violation(call):
    ad_id = call.data[len('show_contacts_btn'):]

    show_owner_info(bot, call, ad_id)


# Обробник для кнопки скасування
@bot.callback_query_handler(func=lambda call: call.data == 'cancel_advertisement_creation')
def handle_cancel_advertisement_creation_callback(call):
    cancel_advertisement_creation(call.message, bot)


# Обробник для кнопки скасування
@bot.callback_query_handler(func=lambda call: call.data == 'cancel_registration_button')
def handle_cancel_advertisement_creation_callback(call):
    cancel_registration_button(call.message, bot)


@bot.callback_query_handler(func=lambda call: call.data == 'not_available_category_btn')
def not_available_category(call):
    bot.send_message(call.message.chat.id, '❗️ Щось пішло не так....\n😢 Дана категорія недоступна')


@bot.callback_query_handler(func=lambda call: call.data == 'сhildren_world_btn')
def children_world(call):
    category_name = '*"👶 Дитячий світ"*'
    updated_message_text = f"❗️ Ви обрали категорію {category_name}.\n 🤔️ Оберіть підкатегорію:"

    # Оновлення попереднього повідомлення
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=updated_message_text,
                          reply_markup=children_world_markup,
                          parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == 'realty_markup_btn')
def realty(call):
    category_name = '*"🏠 Нерухомість"*'
    updated_message_text = f"❗️ Ви обрали категорію {category_name}.\n 🤔️ Оберіть підкатегорію:"

    # Оновлення попереднього повідомлення
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=updated_message_text,
                          reply_markup=realty_markup,
                          parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == 'vehicle_markup_btn')
def vehicle(call):
    category_name = '*"🚗 Авто"*'
    updated_message_text = f"❗️ Ви обрали категорію {category_name}.\n 🤔️ Оберіть підкатегорію:"

    # Оновлення попереднього повідомлення
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=updated_message_text,
                          reply_markup=vehicle_markup,
                          parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == 'spare_parts_markup_btn')
def spare_parts_transport(call):
    category_name = '*"🛠️ Запчастини для транспорту"*'
    updated_message_text = f"❗️ Ви обрали категорію {category_name}.\n 🤔️ Оберіть підкатегорію:"

    # Оновлення попереднього повідомлення
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=updated_message_text,
                          reply_markup=spare_parts_markup,
                          parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == 'job_markup_btn')
def job(call):
    category_name = '*"💼 Робота"*'
    updated_message_text = f"❗️ Ви обрали категорію {category_name}.\n 🤔️ Оберіть підкатегорію:"

    # Оновлення попереднього повідомлення
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=updated_message_text,
                          reply_markup=job_markup,
                          parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == 'animals_markup_btn')
def animals(call):
    category_name = '*"🐾 Тварини"*'
    updated_message_text = f"❗️ Ви обрали категорію {category_name}.\n 🤔️ Оберіть підкатегорію:"

    # Оновлення попереднього повідомлення
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=updated_message_text,
                          reply_markup=animals_markup,
                          parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == 'house_garden_markup_btn')
def house_garden(call):
    category_name = '*"🏡 Дім і сад"*'
    updated_message_text = f"❗️ Ви обрали категорію {category_name}.\n 🤔️ Оберіть підкатегорію:"

    # Оновлення попереднього повідомлення
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=updated_message_text,
                          reply_markup=house_garden_markup,
                          parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == 'electronics_markup_btn')
def electronics(call):
    category_name = '*"📱 Електроніка"*'
    updated_message_text = f"❗️ Ви обрали категорію {category_name}.\n 🤔️ Оберіть підкатегорію:"

    # Оновлення попереднього повідомлення
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=updated_message_text,
                          reply_markup=electronics_markup,
                          parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == 'business_services_markup_btn')
def business_services(call):
    category_name = '*"🤝 Бізнес та сервіси"*'
    updated_message_text = f"❗️ Ви обрали категорію {category_name}.\n 🤔️ Оберіть підкатегорію:"

    # Оновлення попереднього повідомлення
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=updated_message_text,
                          reply_markup=business_services_markup,
                          parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == 'rent_hire_markup_btn')
def rent_hire(call):
    category_name = '*"🚀 Оренда та прокат"*'
    updated_message_text = f"❗️ Ви обрали категорію {category_name}.\n 🤔️ Оберіть підкатегорію:"

    # Оновлення попереднього повідомлення
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=updated_message_text,
                          reply_markup=rent_hire_markup,
                          parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == 'fashion_style_markup_btn')
def fashion_style(call):
    category_name = '*"👗 Мода та стиль"*'
    updated_message_text = f"❗️ Ви обрали категорію {category_name}.\n 🤔️ Оберіть підкатегорію:"

    # Оновлення попереднього повідомлення
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=updated_message_text,
                          reply_markup=fashion_style_markup,
                          parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == 'hobbies_markup_btn')
def hobbies_recreation_sports(call):
    category_name = '*"⚽ Хобі, відпочинок і спорт"*'
    updated_message_text = f"❗️ Ви обрали категорію {category_name}.\n 🤔️ Оберіть підкатегорію:"

    # Оновлення попереднього повідомлення
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=updated_message_text,
                          reply_markup=hobbies_markup,
                          parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.message.chat.id
    user_search = get_user_search(user_id)

    if call.data == 'filters_settings_btn':
        message_id = call.message.message_id
        bot.delete_message(chat_id=user_id, message_id=message_id)
        search_filters_message(bot, call.message, user_search)

    elif call.data == 'matches_text_btn':
        message_id = call.message.message_id
        bot.delete_message(chat_id=user_id, message_id=message_id)
        bot.send_message(user_id, "Введіть текст збігів:")
        bot.register_next_step_handler(call.message,
                                       lambda message: process_matches_text_step(bot, message, user_search))

    elif call.data == 'condition_btn':
        message_id = call.message.message_id
        bot.delete_message(chat_id=user_id, message_id=message_id)
        process_condition_step(bot, call.message, user_search)

    elif call.data == 'category_and_subcategory_btn':
        message_id = call.message.message_id
        bot.delete_message(chat_id=user_id, message_id=message_id)
        process_category_step(bot, call.message, user_search)

    elif call.data == 'price_min_max_btn':
        message_id = call.message.message_id
        bot.delete_message(chat_id=user_id, message_id=message_id)
        process_price_step(bot, call.message, user_search)

    elif call.data == 'location_btn':
        message_id = call.message.message_id
        bot.delete_message(chat_id=user_id, message_id=message_id)
        process_location_region_step(bot, call.message, user_search)

    elif call.data == 'sort_by_btn':
        message_id = call.message.message_id
        bot.delete_message(chat_id=user_id, message_id=message_id)
        process_sort_by(bot, call.message, user_search)

    elif call.data == 'back_to_message_filters_btn':
        message_id = call.message.message_id
        bot.delete_message(chat_id=user_id, message_id=message_id)
        search_message(bot, call.message, user_search)

    elif call.data == 'cancel_matches_text_btn':
        print('cancel_matches_text_btn - all is ok')
        message_id = call.message.message_id
        bot.delete_message(chat_id=user_id, message_id=message_id)
        handle_clear_matches_text(bot, call.message, user_search)

    elif call.data == 'cancel_condition_btn':
        print('cancel_condition_btn - all is ok')
        message_id = call.message.message_id
        bot.delete_message(chat_id=user_id, message_id=message_id)
        handle_clear_condition(bot, call.message, user_search)

    elif call.data == 'cancel_category_and_subcategory_btn':
        print('cancel_category_and_subcategory_btn - all is ok')
        message_id = call.message.message_id
        bot.delete_message(chat_id=user_id, message_id=message_id)
        handle_clear_category_subcategory(bot, call.message, user_search)

    elif call.data == 'cancel_price_min_max_btn':
        print('cancel_price_min_max_btn - all is ok')
        message_id = call.message.message_id
        bot.delete_message(chat_id=user_id, message_id=message_id)
        handle_clear_price_max_min(bot, call.message, user_search)

    elif call.data == 'cancel_location_btn':
        print('cancel_location_btn - all is ok')
        message_id = call.message.message_id
        bot.delete_message(chat_id=user_id, message_id=message_id)
        handle_clear_location_region_city(bot, call.message, user_search)

    elif call.data == 'cancel_sort_by_btn':
        print('cancel_sort_by_btn - all is ok')
        message_id = call.message.message_id
        bot.delete_message(chat_id=user_id, message_id=message_id)
        handle_clear_sort_by(bot, call.message, user_search)

    elif call.data == 'cancel_all_filters_btn':
        message_id = call.message.message_id
        bot.delete_message(chat_id=user_id, message_id=message_id)
        handle_clear_all_filters_search(bot, call.message, user_search)


@bot.callback_query_handler(func=lambda call: True)
def callback_query_subcategory(call):
    if call.message:
        subcategory_text = None

        if call.data == 'children_world_clothing':
            subcategory_text = "👕 Дитячий одяг"
        elif call.data == 'children_world_footwear':
            subcategory_text = "👟 Дитяче взуття"
        elif call.data == 'children_world_prams':
            subcategory_text = "🛍️ Дитячі коляски"
        elif call.data == 'children_world_car_seats':
            subcategory_text = "👶 Дитячі автокрісла"
        elif call.data == 'children_world_furniture':
            subcategory_text = "🪑 Дитячі меблі"
        elif call.data == 'children_world_toys':
            subcategory_text = "🎲 Іграшки"
        elif call.data == 'children_world_transport':
            subcategory_text = "🚗 Дитячий транспорт"
        elif call.data == 'children_world_feeding':
            subcategory_text = "🍼 Годування"
        elif call.data == 'children_world_school_supplies':
            subcategory_text = "🎒 Товари для школярів"
        elif call.data == 'children_world_others':
            subcategory_text = "🔗 Інші товари"

        ##
        elif call.data == 'realty_apartments':
            subcategory_text = "🏢 Квартири"
        elif call.data == 'realty_rooms':
            subcategory_text = "🛌 Кімнати"
        elif call.data == 'realty_houses':
            subcategory_text = "🏡 Будинки"
        elif call.data == 'realty_short_term_rental':
            subcategory_text = "🏠 Подобова оренда житла"
        elif call.data == 'realty_land':
            subcategory_text = "🌳 Земля"
        elif call.data == 'realty_commercial_property':
            subcategory_text = "🏢 Комерційна нерухомість"
        elif call.data == 'realty_garages_parking':
            subcategory_text = "🚗 Гаражі/Парковки"
        elif call.data == 'realty_foreign_property':
            subcategory_text = "🌍 Нерухомість за кордоном"

        ##
        elif call.data == 'vehicle_cars':
            subcategory_text = "🚗 Легкові автомобілі"
        elif call.data == 'vehicle_trucks':
            subcategory_text = "🚚 Вантажні автомобілі"
        elif call.data == 'vehicle_buses':
            subcategory_text = "🚌 Автобуси"
        elif call.data == 'vehicle_motorcycles':
            subcategory_text = "🏍️ Мотоцикли"
        elif call.data == 'vehicle_special_equipment':
            subcategory_text = "🚜 Спецтехніка"
        elif call.data == 'vehicle_agricultural_machinery':
            subcategory_text = "🚜 Сільгосптехніка"
        elif call.data == 'vehicle_water_transport':
            subcategory_text = "🛥️ Водний транспорт"
        elif call.data == 'vehicle_cars_from_poland':
            subcategory_text = "🚗 Автомобілі з Польщі"
        elif call.data == 'vehicle_trailers_motorhomes':
            subcategory_text = "🚐 Причепи/Будинки на колесах"
        elif call.data == 'vehicle_other_transport':
            subcategory_text = "🚀 Інший транспорт"

        ##
        elif call.data == 'spare_parts_auto_parts':
            subcategory_text = "🚗 Автозапчастини"
        elif call.data == 'spare_parts_auto_accessories':
            subcategory_text = "🛠️ Аксесуари для авто"
        elif call.data == 'spare_parts_car_audio_multimedia':
            subcategory_text = "🔊 Автозвук та мультимедіа"
        elif call.data == 'spare_parts_tires_wheels':
            subcategory_text = "🚗 Шини/Диски і Колеса"
        elif call.data == 'spare_parts_gps_dashcams':
            subcategory_text = "🌐 GPS-навігатори / Відеореєстратори"
        elif call.data == 'spare_parts_transport_for_parts':
            subcategory_text = "🚛 Транспорт на запчастини / Авторозбірка"
        elif call.data == 'spare_parts_motorcycle_parts':
            subcategory_text = "🏍️ Мотозапчастини"
        elif call.data == 'spare_parts_motorcycle_gear':
            subcategory_text = "👕 Мотоекіпірування"
        elif call.data == 'spare_parts_motorcycle_accessories':
            subcategory_text = "🛵 Мотоаксесуари"
        elif call.data == 'spare_parts_lubricants_auto_chemicals':
            subcategory_text = "🧴 Мастила та Автохімія"
        elif call.data == 'spare_parts_other_vehicle_parts':
            subcategory_text = "🔩 Запчастини для іншої техніки"

        ##
        elif call.data == 'job_retail_trade':
            subcategory_text = "🛒 Роздрібна торгівля / продажі / закупка"
        elif call.data == 'job_logistics_warehouse_delivery':
            subcategory_text = "🚚 Логістика / Склад / Доставка"
        elif call.data == 'job_construction_finish_works':
            subcategory_text = "🏗️ Будівництво / Облицювальні роботи"
        elif call.data == 'job_call_centers_telecommunications':
            subcategory_text = "📞 Колл-центри / Телекомунікації"
        elif call.data == 'job_administrative_staff':
            subcategory_text = "📋 Адміністративний персонал"
        elif call.data == 'job_security':
            subcategory_text = "🛡️ Охорона / Безпека"
        elif call.data == 'job_cleaning_domestic_staff':
            subcategory_text = "🧹 Клінінг / Домашній персонал"
        elif call.data == 'job_beauty_fitness_sports':
            subcategory_text = "💇 Краса / Фітнес / Спорт"
        elif call.data == 'job_education_translation':
            subcategory_text = "📚 Освіта / Переклад"
        elif call.data == 'job_culture_art_entertainment':
            subcategory_text = "🎭 Культура / Мистецтво / Розваги"
        elif call.data == 'job_medical_pharmaceutical':
            subcategory_text = "🏥 Медицина / Фармацевтика"
        elif call.data == 'job_it_computers':
            subcategory_text = "💻 IT / Комп'ютери"
        elif call.data == 'job_banking_finance_insurance_law':
            subcategory_text = "🏦 Банки / Фінанси / Страхування / Юриспруденція"
        elif call.data == 'job_real_estate':
            subcategory_text = "🏠 Нерухомість"
        elif call.data == 'job_advertising_design_pr':
            subcategory_text = "📢 Реклама / Дизайн / PR"
        elif call.data == 'job_manufacturing':
            subcategory_text = "🏭 Виробництво"
        elif call.data == 'job_agriculture_forestry':
            subcategory_text = "🚜 Сільське і лісове господарство"
        elif call.data == 'job_part_time':
            subcategory_text = "🕒 Часткова зайнятість"
        elif call.data == 'job_accounting':
            subcategory_text = "📊 Бухгалтерія"
        elif call.data == 'job_hotel_restaurant_business':
            subcategory_text = "🏨 Готельно-ресторанний бізнес"
        elif call.data == 'job_other_industries':
            subcategory_text = "🌐 Інші сфери занять"
        elif call.data == 'job_auto_service_car_washes':
            subcategory_text = "🔧 СТО / Автомийки"
        elif call.data == 'job_military_service':
            subcategory_text = "🎖️ Служба в Силах оборони"

        ###
        elif call.data == 'animals_dogs':
            subcategory_text = "🐶 Собаки"
        elif call.data == 'animals_cats':
            subcategory_text = "🐱 Коти"
        elif call.data == 'animals_aquarium':
            subcategory_text = "🐠 Акваріумістика"
        elif call.data == 'animals_birds':
            subcategory_text = "🐦 Пташки"
        elif call.data == 'animals_rodents':
            subcategory_text = "🐭 Гризуни"
        elif call.data == 'animals_reptiles':
            subcategory_text = "🦎 Рептилії"
        elif call.data == 'animals_farm_animals':
            subcategory_text = "🐄 Сільгосп тварини"
        elif call.data == 'animals_other_animals':
            subcategory_text = "🐾 Інші тварини"
        elif call.data == 'animals_pet_supplies':
            subcategory_text = "🏬 Зоотовари"
        elif call.data == 'animals_mating':
            subcategory_text = "💑 В'язка"
        elif call.data == 'animals_found_bureau':
            subcategory_text = "🔍 Бюро знахідок"

        ##
        elif call.data == 'house_garden_stationery_consumables':
            subcategory_text = "📝 Канцтовари / Витратні матеріали"
        elif call.data == 'house_garden_furniture':
            subcategory_text = "🛋️ Меблі"
        elif call.data == 'house_garden_food_drinks':
            subcategory_text = "🍲 Продукти харчування / Напої"
        elif call.data == 'house_garden_garden':
            subcategory_text = "🌳 Сад / Город"
        elif call.data == 'house_garden_interior_items':
            subcategory_text = "🖼️ Предмети інтер'єру"
        elif call.data == 'house_garden_construction_repair':
            subcategory_text = "🛠️ Будівництво / Ремонт"
        elif call.data == 'house_garden_tools':
            subcategory_text = "🔧 Інструменти"
        elif call.data == 'house_garden_indoor_plants':
            subcategory_text = "🪴 Кімнатні рослини"
        elif call.data == 'house_garden_tableware_kitchenware':
            subcategory_text = "🍽️ Посуд / Кухонне приладдя"
        elif call.data == 'house_garden_garden_inventory':
            subcategory_text = "🚜 Садовий інвентар"
        elif call.data == 'house_garden_household_inventory_chemicals':
            subcategory_text = "🧽 Господарський інвентар / Побутова хімія"
        elif call.data == 'house_garden_other_home_goods':
            subcategory_text = "🏠 Інші товари для дому"

        ##
        elif call.data == 'electronics_phones_accessories':
            subcategory_text = "📱 Телефони та аксесуари"
        elif call.data == 'electronics_computers_components':
            subcategory_text = "💻 Комп'ютери та комплектуючі"
        elif call.data == 'electronics_photo_video':
            subcategory_text = "📷 Фото / Відео"
        elif call.data == 'electronics_tv_video_equipment':
            subcategory_text = "📺 ТВ / Відеотехніка"
        elif call.data == 'electronics_audio_equipment':
            subcategory_text = "🔊 Аудіотехніка"
        elif call.data == 'electronics_games_consoles':
            subcategory_text = "🎮 Ігри та ігрові приставки"
        elif call.data == 'electronics_tablets_accessories':
            subcategory_text = "📟 Планшети та аксесуари"
        elif call.data == 'electronics_laptops_accessories':
            subcategory_text = "💻 Ноутбуки та аксесуари"
        elif call.data == 'electronics_home_appliances':
            subcategory_text = "🏠 Техніка для дому"
        elif call.data == 'electronics_kitchen_appliances':
            subcategory_text = "🍳 Техніка для кухні"
        elif call.data == 'electronics_climate_equipment':
            subcategory_text = "❄️ Кліматичне обладнання"
        elif call.data == 'electronics_personal_care':
            subcategory_text = "🧴 Індивідуальний догляд"
        elif call.data == 'electronics_accessories_components':
            subcategory_text = "🔌 Аксесуари й комплектуючі"
        elif call.data == 'electronics_other_electronics':
            subcategory_text = "🔧 Інша електротехніка"

        ##
        if call.data == 'business_services_auto_moto':
            subcategory_text = "🚗 Авто / Мото послуги"
        elif call.data == 'business_services_beauty_health':
            subcategory_text = "💇 Краса / Здоров'я"
        elif call.data == 'business_services_child_elderly_care':
            subcategory_text = "👶 Догляд за дітьми та літніми людьми"
        elif call.data == 'business_services_household':
            subcategory_text = "🏠 Побутові послуги"
        elif call.data == 'business_services_cleaning':
            subcategory_text = "🧹 Клінінг"
        elif call.data == 'business_services_education_sports':
            subcategory_text = "📚 Послуги освіти та спорту"
        elif call.data == 'business_services_transportation':
            subcategory_text = "🚚 Перевезення"
        elif call.data == 'business_services_specialized_services':
            subcategory_text = "🛠️ Послуги спецтехніки"
        elif call.data == 'business_services_photo_video':
            subcategory_text = "📸 Фото та відеозйомка"
        elif call.data == 'business_services_event_organization':
            subcategory_text = "🎉 Організація свят"
        elif call.data == 'business_services_appliance_repair':
            subcategory_text = "🛠️ Ремонт та обслуговування техніки"
        elif call.data == 'business_services_construction_repair':
            subcategory_text = "🔨 Будівництво та ремонт"
        elif call.data == 'business_services_raw_materials_materials':
            subcategory_text = "📦 Сированина / Матеріали"
        elif call.data == 'business_services_secondhand_reception':
            subcategory_text = "🔄 Прийом вторсировини"
        elif call.data == 'business_services_tourism_immigration':
            subcategory_text = "✈️ Туризм / Іміграція"
        elif call.data == 'business_services_business':
            subcategory_text = "👔 Ділові послуги"
        elif call.data == 'business_services_business_sale':
            subcategory_text = "💼 Продаж бізнесу"
        elif call.data == 'business_services_animal_services':
            subcategory_text = "🐾 Послуги для тварин"
        elif call.data == 'business_services_funeral_services':
            subcategory_text = "⚰️ Ритуальні послуги"
        elif call.data == 'business_services_other_services':
            subcategory_text = "🔧 Інші послуги"

        ##
        elif call.data == 'rent_hire_transport_equipment':
            subcategory_text = "🚗 Оренда транспорту та спецтехніки"
        elif call.data == 'rent_hire_bike_moto_rental':
            subcategory_text = "🚲 Прокат велосипедів і мото"
        elif call.data == 'rent_hire_equipment_rental':
            subcategory_text = "🛠️ Оренда обладнання"
        elif call.data == 'rent_hire_tool_rental':
            subcategory_text = "🔧 Прокат інструментів"
        elif call.data == 'rent_hire_medical_goods_rental':
            subcategory_text = "🏥 Прокат товарів медичного призначення"
        elif call.data == 'rent_hire_tech_electronics_rental':
            subcategory_text = "🔌 Прокат техніки та електроніки"
        elif call.data == 'rent_hire_event_goods_rental':
            subcategory_text = "🎉 Прокат товарів для заходів"
        elif call.data == 'rent_hire_sports_tourism_rental':
            subcategory_text = "⚽ Прокат спортивних та туристичних товарів"
        elif call.data == 'rent_hire_clothing_accessories_rental':
            subcategory_text = "👗 Прокат одягу та аксесуарів"
        elif call.data == 'rent_hire_childrens_clothing_rental':
            subcategory_text = "👶 Прокат дитячого одягу та товарів"
        elif call.data == 'rent_hire_other_goods_rental':
            subcategory_text = "🔄 Прокат інших товарів"

        ##
        elif call.data == 'fashion_style_womens_clothing':
            subcategory_text = "👗 Жіночий одяг"
        elif call.data == 'fashion_style_womens_shoes':
            subcategory_text = "🥿 Жіноче взуття"
        elif call.data == 'fashion_style_mens_clothing':
            subcategory_text = "👔 Чоловічий одяг"
        elif call.data == 'fashion_style_mens_shoes':
            subcategory_text = "👞 Чоловіче взуття"
        elif call.data == 'fashion_style_womens_underwear_swimwear':
            subcategory_text = "🩲 Жіноча білизна та купальники"
        elif call.data == 'fashion_style_mens_underwear_swimwear':
            subcategory_text = "🩲 Чоловіча білизна та плавки"
        elif call.data == 'fashion_style_headwear':
            subcategory_text = "👒 Головні убори"
        elif call.data == 'fashion_style_for_wedding':
            subcategory_text = "👰 Для весілля"
        elif call.data == 'fashion_style_wristwatches':
            subcategory_text = "⌚ Наручні годинники"
        elif call.data == 'fashion_style_accessories':
            subcategory_text = "🕶️ Аксесуари"
        elif call.data == 'fashion_style_maternity_clothing':
            subcategory_text = "🤰 Одяг для вагітних"
        elif call.data == 'fashion_style_beauty_health':
            subcategory_text = "💄 Краса / здоров'я"
        elif call.data == 'fashion_style_gifts':
            subcategory_text = "🎁 Подарунки"
        elif call.data == 'fashion_style_workwear_footwear_accessories':
            subcategory_text = "👷 Спецодяг, спецвзуття та аксесуари"
        elif call.data == 'fashion_style_miscellaneous':
            subcategory_text = "👚 Мода різне"

        ##
        elif call.data == 'hobbies_antiques_collectibles':
            subcategory_text = "🏺 Антикваріат / Колекції"
        elif call.data == 'hobbies_musical_instruments':
            subcategory_text = "🎶 Музичні інструменти"
        elif call.data == 'hobbies_sports_recreation':
            subcategory_text = "⚽ Спорт / Відпочинок"
        elif call.data == 'hobbies_cycling':
            subcategory_text = "🚴 Вело"
        elif call.data == 'hobbies_militaria':
            subcategory_text = "🪖 Мілітарія"
        elif call.data == 'hobbies_quadcopters_accessories':
            subcategory_text = "🚁 Квадрокоптери та аксесуари"
        elif call.data == 'hobbies_books_magazines':
            subcategory_text = "📚 Книги / Журнали"
        elif call.data == 'hobbies_cd_dvd_vinyl':
            subcategory_text = "💿 CD / DVD / Платівки"
        elif call.data == 'hobbies_tickets':
            subcategory_text = "🎫 Квитки"
        elif call.data == 'hobbies_travel_companions':
            subcategory_text = "🌍 Пошук попутників"
        elif call.data == 'hobbies_bands_musicians':
            subcategory_text = "🎤 Пошук гуртів / Музикантів"
        elif call.data == 'hobbies_miscellaneous':
            subcategory_text = "🛒 Інше"

        elif call.data == 'go_back_btn':
            updated_message_text = "🤔️ Обери категорію:"

            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=updated_message_text,
                                  reply_markup=category_markup,
                                  parse_mode="Markdown")

        if subcategory_text:
            pass
            #process_subcategory_callback(bot, call.message.chat.id, subcategory_text)


@bot.callback_query_handler(func=lambda call: call.data == 'go_back_btn')
def go_back(call):
    updated_message_text = "🤔️ Обери категорію:"

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=updated_message_text,
                          reply_markup=category_markup,
                          parse_mode="Markdown")


def user_bd_create():
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    # Таблиця користувачів
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        telegram_id INTEGER PRIMARY KEY NOT NULL,
        name VARCHAR(100) NOT NULL,
        mail TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        registration_time TEXT,
        role INTEGER DEFAULT 0
    )""")

    # Таблиця оголошень
    cursor.execute("""CREATE TABLE IF NOT EXISTS advertisements(
        advertisement_id TEXT PRIMARY KEY,
        telegram_id TEXT,
        advertisement_category TEXT,
        advertisement_subcategory TEXT,
        advertisement_name VARCHAR(50),
        advertisement_description VARCHAR(300) NOT NULL,
        advertisement_photo_folder TEXT,
        advertisement_price INTEGER,
        advertisement_date TEXT,
        advertisement_until TEXT,
        advertisement_country TEXT,
        advertisement_region TEXT,
        advertisement_city TEXT,
        advertisement_status TEXT,
        advertisement_changes TEXT,
        advertisement_condition TEXT,
        FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
    )""")

    # Таблиця вибраних
    cursor.execute("""CREATE TABLE IF NOT EXISTS favorites(
        favorite_id TEXT PRIMARY KEY,
        telegram_id TEXT,
        advertisement_id TEXT,
        favorite_date TEXT,
        FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
        FOREIGN KEY (advertisement_id) REFERENCES advertisements(advertisement_id)
    )""")

    # Таблиця скарг
    cursor.execute("""CREATE TABLE IF NOT EXISTS complaints(
        complaint_id TEXT PRIMARY KEY,
        telegram_id TEXT,
        advertisement_id TEXT,
        complaint_text VARCHAR(60),
        complaint_status VARCHAR(60),
        complaint_date TEXT,
        FOREIGN KEY (telegram_id) REFERENCES users(telegram_id),
        FOREIGN KEY (advertisement_id) REFERENCES advertisements(advertisement_id)
    )""")

    # Таблиця заблокованих юзерів
    cursor.execute("""CREATE TABLE IF NOT EXISTS blocked_users(
        blocked_id TEXT PRIMARY KEY,
        telegram_id TEXT,
        blocked_date TEXT,
        blocked_until TEXT,
        blocked_reason text,
        admin_id,
        FOREIGN KEY (telegram_id) REFERENCES users(telegram_id),
        FOREIGN KEY (admin_id) REFERENCES users(telegram_id)
    )""")

    # Таблиця дій модерації
    cursor.execute("""CREATE TABLE IF NOT EXISTS moderation_actions(
        action_id TEXT PRIMARY KEY,
        telegram_id TEXT,
        advertisement_id TEXT,
        advertisement_status TEXT,
        action_date TEXT,
        FOREIGN KEY (telegram_id) REFERENCES users(telegram_id),
        FOREIGN KEY (advertisement_id) REFERENCES advertisements(advertisement_id)
    )""")

    # Таблиця дій відповідей
    cursor.execute("""CREATE TABLE IF NOT EXISTS answer_actions(
        action_id TEXT PRIMARY KEY,
        telegram_id TEXT,
        question_id TEXT,
        answer_text TEXT,
        action_date TEXT,
        FOREIGN KEY (telegram_id) REFERENCES users(telegram_id),
        FOREIGN KEY (question_id) REFERENCES questions(question_id)
    )""")

    # Таблиця сповіщень
    cursor.execute("""CREATE TABLE IF NOT EXISTS notifications(
        notification_id TEXT PRIMARY KEY,
        telegram_id TEXT,
        notification_title TEXT,
        notification_text TEXT,
        notification_status TEXT,
        notification_date TEXT,
        FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
    )""")

    # Таблиця запитань
    cursor.execute("""CREATE TABLE IF NOT EXISTS questions(
        question_id TEXT PRIMARY KEY,
        telegram_id TEXT,
        question_text TEXT,
        question_status TEXT,
        question_date TEXT,
        FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
    )""")

    # Створення таблиці, якщо вона ще не існує
    cursor.execute('''CREATE TABLE IF NOT EXISTS notified_users_ad_deactivation (
                    notified_id TEXT PRIMARY KEY,
                    telegram_id INTEGER,
                    advertisement_id TEXT,
                    notified_date text,
                    FOREIGN KEY (telegram_id) REFERENCES users(telegram_id),
                    FOREIGN KEY (advertisement_id) REFERENCES advertisements(advertisement_id)
    )''')

    connect.commit()
    connect.close()


def make_folder_photo():
    photo_folder = "photos"
    if not os.path.exists(photo_folder):
        os.makedirs(photo_folder)


def notify_user_about_ad():
    ads_to_deactivate = print_ads_for_deactivation()

    for ad in ads_to_deactivate:
        advertisement_id = ad[0]
        telegram_id = ad[1]
        ad_id = ad[0]
        ad_name = ad[4]
        existing_notification = check_notified(telegram_id, ad_id)

        # Якщо повідомлення ще не було надіслано, надсилаємо його і зберігаємо інформацію про це
        if not existing_notification:
            bot.send_message(telegram_id,
                             f"<b>❗️ Оголошення '{ad_name}' буде активним ще 3 дні</b>\n\n<i><b>📝 Примітка:</b> перейдіть в <b>'📂 Мої оголошення'</b> -> <b>'📌 Активні оголошення'</b> -> <b>Оберіть потрібне оголошення</b> -> Натисніть кнопку <b>'🔄 Продовжити оголошення'</b></i>.\n\n Тоді оголошення буде знову активним на 30 днів!", parse_mode='HTML')
            create_new_notified(telegram_id, advertisement_id)


if __name__ == "__main__":
    try:
        user_bd_create()
        make_folder_photo()
        # adv_bd_create()
        print('Бот успішно запустився!')

        # Планувальник розблокувань юзерів
        scheduler = BackgroundScheduler()
        scheduler.add_job(check_and_unblock_users, 'interval', seconds=1)
        scheduler.add_job(check_and_deactivate_ads, 'interval', seconds=1)
        scheduler.add_job(notify_user_about_ad, 'interval', seconds=1)
        scheduler.start()
        # console_menu_for_bot()
        # Запуск циклу обробки повідомлень бота
        bot.polling(none_stop=True)

    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
# bot.polling()
