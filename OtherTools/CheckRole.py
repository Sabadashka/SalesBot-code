from DataBase.BlockedUsers_database import get_all_data_blocked_user
from DataBase.Questions_database import get_questions_where_status_on_moderation_id
from DataBase.Advertisement_database import get_ads_where_moderation_on_review
from DataBase.Complaints_database import get_complaints_where_admin_on_review
from FunctionsMenuBtn.FunctionsAdminMenuBtn.AdminBlockUser import block_user
from FunctionsMenuBtn.FunctionsAdminMenuBtn.AdminChangeRoleUser import change_role
from FunctionsMenuBtn.FunctionsAdminMenuBtn.AdminCheckComplaints import check_complaints
from FunctionsMenuBtn.FunctionsAdminMenuBtn.AdminCheckModeration import check_moderation
from FunctionsMenuBtn.FunctionsAdminMenuBtn.AdminCheckQuestions import check_questions
from FunctionsMenuBtn.FunctionsAdminMenuBtn.AdminShowTopModerators import show_top_moderators_by_moderation, show_top_moderators_by_answers
from FunctionsMenuBtn.FunctionsAdminMenuBtn.AdminCreateNotification import start_creating_notification
from FunctionsMenuBtn.FunctionsAdminMenuBtn.AdminShowBlockedUsers import show_blocked_users
from FunctionsMenuBtn.FunctionsAdminMenuBtn.AdminUnblockUser import unblock_user
from FunctionsMenuBtn.FunctionsAdminMenuBtn.AdminShowUsersList import show_users_by_role
from Markups.menu_markups import keyboard_menu, moderator_menu_keyboard_menu, \
    admin_menu_database_keyboard_menu, admin_menu_keyboard_menu, top_moderators_keyboard_menu, \
    admin_show_users_list_keyboard_menu


# [MODERATOR] функції перевірки ролі


def check_role_to_enter_moderator_panel(role, bot, message):
    if role == 1:
        role_name = '*🛡️ Модераторська панель*'
        bot.send_message(message.chat.id, f"❗️ Оберіть пункт в '{role_name}'", parse_mode='Markdown',
                         reply_markup=moderator_menu_keyboard_menu)

    else:
        bot.send_message(message.chat.id, "❗️ Ви не *Модератор*. У Вас немає таких прав!",
                         parse_mode='Markdown',
                         reply_markup=keyboard_menu)


def check_role_for_moderation(role, bot, message):
    if role == 2:
        check_moderation(bot, message)
    elif role == 1:
        check_moderation(bot, message)
    else:
        bot.send_message(message.chat.id, "❗️ У Вас немає таких прав!",
                         parse_mode='Markdown',
                         reply_markup=keyboard_menu)


def check_exists_moderation(role, acc_id, bot, message):
    info = get_ads_where_moderation_on_review(acc_id)

    if info:
        bot.send_message(message.chat.id,
                         f"❗️ Ви не можете завершити перегляд оголошень. Потрібно опублікувати оголошення, яке розглядаєте")
        return
    else:
        if role == 2:
            role = '*👑 Адмінська панель*'
            bot.send_message(message.chat.id, f"❗️ Ви повернулися в '{role}'", parse_mode='Markdown',
                             reply_markup=admin_menu_keyboard_menu)
            return

        if role == 1:
            role = '*🛡️ Модераторська панель*'
            bot.send_message(message.chat.id, f"❗️ Ви повернулися в '{role}'", parse_mode='Markdown',
                             reply_markup=moderator_menu_keyboard_menu)
            return

        else:
            bot.send_message(message.chat.id, f"❗️ Ви вийшли в '*головне меню*'", parse_mode='Markdown',
                             reply_markup=keyboard_menu)
            return


# ---------------------------------


# [ADMIN] функції перевірки ролі


def check_role_to_enter_admin_panel(role, bot, message):
    if role == 2:
        role_name = '*👑 Адмінська панель*'
        bot.send_message(message.chat.id, f"❗️ Оберіть пункт в '{role_name}'", parse_mode='Markdown',
                         reply_markup=admin_menu_keyboard_menu)

    else:
        bot.send_message(message.chat.id, "❗️ Ви не *Адміністратор*. У Вас немає таких прав!",
                         parse_mode='Markdown',
                         reply_markup=keyboard_menu)


def check_role_for_complaints(role, bot, message):
    if role == 2:
        check_complaints(bot, message)
    else:
        bot.send_message(message.chat.id, "❗️ У Вас немає таких прав!",
                         parse_mode='Markdown',
                         reply_markup=keyboard_menu)


def check_exists_complaints(role, acc_id, bot, message):
    info = get_complaints_where_admin_on_review(acc_id)

    if info:
        bot.send_message(message.chat.id,
                         f"❗️ Ви не можете завершити перегляд скарг. Потрібно прийняти рішення для скарги!")
        return
    else:
        if role == 2:
            role = '*👑 Адмінська панель*'
            bot.send_message(message.chat.id, f"❗️ Ви повернулися в '{role}'", parse_mode='Markdown',
                             reply_markup=admin_menu_keyboard_menu)
            return
        else:
            bot.send_message(message.chat.id, f"❗️ Ви вийшли в '*головне меню*'", parse_mode='Markdown',
                             reply_markup=keyboard_menu)
            return


def check_role_for_database_actions(role, bot, message):
    if role == 2:
        # block_user(bot, admin_id, message)
        bot.send_message(message.chat.id, "❗️ Оберіть пункт в *'🗃️ Дії з Базою Даних'*", parse_mode='Markdown',
                         reply_markup=admin_menu_database_keyboard_menu)

    else:
        bot.send_message(message.chat.id, '❗️ Невідома команда...', reply_markup=keyboard_menu)


def check_role_for_block_user(role, admin_id, bot, message):
    if role == 2:
        block_user(bot, admin_id, message, role)

    else:
        bot.send_message(message.chat.id, '❗️ Невідома команда...', reply_markup=keyboard_menu)


def check_role_for_unblock_user(role, bot, message):
    if role == 2:
        unblock_user(bot, message, role)

    else:
        bot.send_message(message.chat.id, '❗️ Невідома команда...', reply_markup=keyboard_menu)


def check_role_for_change_role_user(role, bot, message):
    if role == 2:
        change_role(bot, message, role)
    else:
        bot.send_message(message.chat.id, '❗️ Невідома команда...', reply_markup=keyboard_menu)


def check_role_for_choice_type_show_users(role, bot, message):
    if role == 2:
        bot.send_message(message.chat.id, "<b>❗️ Оберіть, який список показати</b>", parse_mode='HTML',
                         reply_markup=admin_show_users_list_keyboard_menu)

    else:
        bot.send_message(message.chat.id, '❗️ Невідома команда...', reply_markup=keyboard_menu)


def check_role_for_show_users(role, bot, message):
    if role == 2:
        show_users_by_role(bot, message, 0)

    else:
        bot.send_message(message.chat.id, '❗️ Невідома команда...', reply_markup=keyboard_menu)


def check_role_for_show_moderators(role, bot, message):
    if role == 2:
        show_users_by_role(bot, message, 1)

    else:
        bot.send_message(message.chat.id, '❗️ Невідома команда...', reply_markup=keyboard_menu)


def check_role_for_show_admins(role, bot, message):
    if role == 2:
        show_users_by_role(bot, message, 2)

    else:
        bot.send_message(message.chat.id, '❗️ Невідома команда...', reply_markup=keyboard_menu)


def check_role_for_show_blocked_users(role, bot, message):
    if role == 2:
        show_blocked_users(bot, message)

    else:
        bot.send_message(message.chat.id, '❗️ Невідома команда...', reply_markup=keyboard_menu)


def check_role_to_return_to_apanel_menu(role, bot, message):
    if role == 2:
        bot.send_message(message.chat.id, "❗️ Ви повернулися назад в *'👑️ Адмінська панель'*", parse_mode='Markdown',
                         reply_markup=admin_menu_keyboard_menu)
    else:
        bot.send_message(message.chat.id, f"❗️ Ви вийшли в '*Головне меню*'", parse_mode='Markdown',
                         reply_markup=keyboard_menu)


def check_role_for_make_notification(role, bot, message):
    if role == 2:
        start_creating_notification(bot, message, role)
    else:
        bot.send_message(message.chat.id, '❗️ Невідома команда...', parse_mode='Markdown',
                         reply_markup=keyboard_menu)


# ЗАГАЛЬНЕ

def role_check_to_return_to_menu(role, bot, message):
    if role == 2:
        role = '*👑 Адмінська панель*'
        bot.send_message(message.chat.id, f"❗️ Ви вийшли з '{role}'", parse_mode='Markdown',
                         reply_markup=keyboard_menu)
    elif role == 1:
        role = '*🛡️ Модераторська панель*'
        bot.send_message(message.chat.id, f"❗️ Ви вийшли з '{role}'", parse_mode='Markdown',
                         reply_markup=keyboard_menu)
    else:
        bot.send_message(message.chat.id, f"❗️ Ви вийшли в '*Головне меню*'", parse_mode='Markdown',
                         reply_markup=keyboard_menu)


def check_role_for_show_top_moderators(role, bot, message):
    if role == 2:
        #show_top_moderators(bot, message)
        bot.send_message(message.chat.id, "<b>❗️ Оберіть, який ТОП модераторів показати</b>", parse_mode='HTML', reply_markup=top_moderators_keyboard_menu)

    elif role == 1:
        bot.send_message(message.chat.id, "<b>❗️ Оберіть, який ТОП модераторів показати</b>", parse_mode='HTML', reply_markup=top_moderators_keyboard_menu)
        #show_top_moderators(bot, message)

    else:
        bot.send_message(message.chat.id, f"❗️ Невідома команда...", parse_mode='Markdown',
                         reply_markup=keyboard_menu)


def check_role_for_show_top_moderators_by_moderation(role, bot, message):
    if role == 2:
        show_top_moderators_by_moderation(bot, message)

    elif role == 1:
        show_top_moderators_by_moderation(bot, message)

    else:
        bot.send_message(message.chat.id, f"❗️ Невідома команда...", parse_mode='Markdown',
                         reply_markup=keyboard_menu)


def check_role_for_show_top_moderators_by_answers(role, bot, message):
    if role == 2:
        show_top_moderators_by_answers(bot, message)

    elif role == 1:
        show_top_moderators_by_answers(bot, message)

    else:
        bot.send_message(message.chat.id, f"❗️ Невідома команда...", parse_mode='Markdown',
                         reply_markup=keyboard_menu)


def check_role_exit_from_top_moderators(role, bot, message):
    if role == 2:
        bot.send_message(message.chat.id, "❗️ Ви повернулися назад в *'👑️ Адмінська панель'*", parse_mode='Markdown',
                         reply_markup=admin_menu_keyboard_menu)

    elif role == 1:
        bot.send_message(message.chat.id, "❗️ Ви повернулися назад в *'🛡️ Модераторська панель*'", parse_mode='Markdown',
                         reply_markup=moderator_menu_keyboard_menu)
    else:
        bot.send_message(message.chat.id, f"❗️ Ви вийшли в '*Головне меню*'", parse_mode='Markdown',
                         reply_markup=keyboard_menu)


def check_role_for_show_questions(role, bot, message):
    if role == 2:
        check_questions(bot, message)

    elif role == 1:
        check_questions(bot, message)

    else:
        bot.send_message(message.chat.id, f"❗️ Невідома команда...", parse_mode='Markdown',
                         reply_markup=keyboard_menu)


def check_exist_answer(role, acc_id, bot, message):
    info = get_questions_where_status_on_moderation_id(acc_id)

    if info:
        bot.send_message(message.chat.id,
                         f"❗️ Ви не можете завершити перегляд запитань. Потрібно відповісти на запитання, яке розглядаєте")
        return
    else:
        if role == 2:
            role = '*👑 Адмінська панель*'
            bot.send_message(message.chat.id, f"❗️ Ви повернулися в '{role}'", parse_mode='Markdown',
                             reply_markup=admin_menu_keyboard_menu)
            return

        if role == 1:
            role = '*🛡️ Модераторська панель*'
            bot.send_message(message.chat.id, f"❗️ Ви повернулися в '{role}'", parse_mode='Markdown',
                             reply_markup=moderator_menu_keyboard_menu)
            return

        else:
            bot.send_message(message.chat.id, f"❗️ Ви вийшли в '*головне меню*'", parse_mode='Markdown',
                             reply_markup=keyboard_menu)
            return


# ДЛЯ ЗАБЛОКОВАНИХ
def blocked_user_info(bot, message, acc_id):
    blocked_user_data = get_all_data_blocked_user(acc_id)
    blocked_date = blocked_user_data[2]
    blocked_until = blocked_user_data[3]
    blocked_reason = blocked_user_data[4]

    bot.send_message(message.chat.id,
                     f'❗️ Ваш аккаунт заблоковано *{blocked_date}* до *{blocked_until}*\n*⚠️ Причина:* {blocked_reason}',
                     parse_mode='Markdown')