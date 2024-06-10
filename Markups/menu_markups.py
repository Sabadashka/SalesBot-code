from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telebot import types


keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
review_advertisement = types.KeyboardButton("🔍 Пошук оголошень")
#review1_advertisement = types.KeyboardButton("Пошук")
add_advertisement = types.KeyboardButton("📝 Створити оголошення")
my_advertisement = types.KeyboardButton("📂 Мої оголошення")
help_btn = types.KeyboardButton("❓ Допомога")
my_favorites_btn = types.KeyboardButton("❤️ Вибрані")
notifications_btn = types.KeyboardButton("🔔️ Сповіщення")
profile_btn = types.KeyboardButton("👤 Мій обліковий запис")
keyboard_menu.add(review_advertisement, add_advertisement, my_advertisement, my_favorites_btn, help_btn, notifications_btn, profile_btn)

#🚀 Виконати пошук
keyboard_search_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
start_search = types.KeyboardButton("🚀 Виконати пошук")
go_back_from_search = types.KeyboardButton("◀️ Вийти з пошуку")
keyboard_search_menu.add(start_search, go_back_from_search)

markup_ad_types = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
btn_active_ads = types.KeyboardButton("📌 Активні оголошення")
btn_pending_approval = types.KeyboardButton("⏳ Очікують перевірку")
btn_deactivated_ads = types.KeyboardButton("🚫 Деактивовані оголошення")
btn_deleted_ads = types.KeyboardButton("🗑️ Видалені оголошення")
btn_main_menu = types.KeyboardButton("◀️ Головне меню")
markup_ad_types.add(btn_active_ads, btn_pending_approval, btn_deactivated_ads, btn_deleted_ads, btn_main_menu)

#admin_keyboard_menu.add(add_advertisement, review_advertisement, my_advertisement, my_favorites_btn, profile_btn, help_btn, admin_panel)

admin_keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
admin_panel = types.KeyboardButton("👑️ Адмінська панель")
admin_keyboard_menu.add(admin_panel)

moderator_keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
moderator_panel = types.KeyboardButton("🛡️ Модераторська панель")
moderator_keyboard_menu.add(moderator_panel)


#
admin_menu_keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
show_complains = types.KeyboardButton("⚠️ Переглянути скарги")
check_new_ads = types.KeyboardButton("👁 Перевірити оголошення")
#show_users_list = types.KeyboardButton("👥 Показати список користувачів")
#show_moderators_list = types.KeyboardButton("🛡️ Показати список модераторів")
make_notification = types.KeyboardButton("📢 Створити сповіщення")
#show_top_moderators_list = types.KeyboardButton("🏆 Топ модераторів")
show_questions = types.KeyboardButton("📝 Переглянути запитання")
#show_top_moderators_list = types.KeyboardButton("🏆 Топ модераторів")
database_actions = types.KeyboardButton("🗃️ Дії з Базою Даних")
# show_blocked_users_list = types.KeyboardButton("🚫 Показати список заблокованих користувачів")
# block_user = types.KeyboardButton("🔒 Заблокувати користувача")
# unblock_user = types.KeyboardButton("🔓 Розблокувати користувача")
go_back_from_apanel = types.KeyboardButton("◀️ Вийти в головне меню")

#admin_menu_keyboard_menu.add(show_complains, check_new_ads, show_users_list, show_moderators_list, show_admins_list, show_blocked_users_list, block_user, unblock_user, go_back_from_apanel)
admin_menu_keyboard_menu.add(show_complains, check_new_ads, show_questions, make_notification, database_actions, go_back_from_apanel)

top_moderators_keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
by_moderation = types.KeyboardButton("🏆 [Перевірка оголошень]")
by_answers = types.KeyboardButton("🏆 [Відповіді на запитання]")
exit_from_top = types.KeyboardButton("◀️ Назад")
top_moderators_keyboard_menu.add(by_moderation, by_answers, exit_from_top)


admin_menu_database_keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
show_users_list = types.KeyboardButton("👥 Список користвувачів")
#show_moderators_list = types.KeyboardButton("🛡️ Показати список модераторів")
#show_admins_list = types.KeyboardButton("👑️ Показати список адміністраторів")
#show_blocked_users_list = types.KeyboardButton("🚫 Показати список заблокованих користувачів")
#show_top_moderators_list = types.KeyboardButton("🏆 Топ модераторів")
block_user = types.KeyboardButton("🔒 Заблокувати користувача")
unblock_user = types.KeyboardButton("🔓 Розблокувати користувача")
#make_notification = types.KeyboardButton("📢 Створити сповіщення")
change_role_user = types.KeyboardButton("🎭 Змінити роль")
go_back_apanel = types.KeyboardButton("◀️ Повернутися назад")
admin_menu_database_keyboard_menu.add(show_users_list, change_role_user, block_user, unblock_user, go_back_apanel)


admin_show_users_list_keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
show_users_list = types.KeyboardButton("👥 Користувачів")
show_moderators_list = types.KeyboardButton("🛡️ Модераторів")
show_admins_list = types.KeyboardButton("👑️ Адміністраторів")
show_blocked_users_list = types.KeyboardButton("🚫 Заблокованих")
go_back = types.KeyboardButton("❌ Не показувати нічого")
admin_show_users_list_keyboard_menu.add(show_users_list, show_moderators_list, show_admins_list, show_blocked_users_list, go_back)


moderator_menu_keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
check_new_ads = types.KeyboardButton("👁 Перевірити оголошення")
#show_top_moderators_list = types.KeyboardButton("🏆 Топ модераторів")
show_questions = types.KeyboardButton("📝 Переглянути запитання")
go_back_from_apanel = types.KeyboardButton("◀️ Вийти в головне меню")

moderator_menu_keyboard_menu.add(check_new_ads, show_questions, go_back_from_apanel)

# Адміністрація (перегляд скарг)

admin_next_complaint = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
admin_next_complaint_btn = types.KeyboardButton("➡️ Наступна скарга")
admin_exit_from_complaints_btn = types.KeyboardButton("◀️ Завершити перегляд скарг")
admin_next_complaint.add(admin_exit_from_complaints_btn, admin_next_complaint_btn)

admin_complaint_exit = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
admin_complaint_exit.add(admin_exit_from_complaints_btn)

# Модерація оголошень
moderator_next_moderation = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
moderator_next_moderation_btn = types.KeyboardButton("➡️ Наступне оголошення")
moderator_exit_from_moderation_btn = types.KeyboardButton("◀️ Завершити перегляд оголошень")
moderator_next_moderation.add(moderator_exit_from_moderation_btn, moderator_next_moderation_btn)

moderator_moderation_exit = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
moderator_moderation_exit.add(moderator_exit_from_moderation_btn)

# Перегляд запитань
admin_next_question = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
admin_next_question_btn = types.KeyboardButton("Наступне запитання ➡️")
admin_exit_from_answers_btn = types.KeyboardButton("◀️ Завершити перегляд запитань")
admin_next_question.add(admin_exit_from_answers_btn, admin_next_question_btn)

admin_question_exit = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
admin_question_exit.add(admin_exit_from_answers_btn)


ad_steps_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
previous_ad_btn = types.KeyboardButton("◀️ Попереднє оголошення")
next_ad_btn = types.KeyboardButton("Наступне оголошення ▶️")
end_search_btn = types.KeyboardButton("❌ Завершити пошук")
ad_steps_keyboard.add(previous_ad_btn, next_ad_btn, end_search_btn)


