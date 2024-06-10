from datetime import datetime

from DataBase.Users_database import get_user_data_by_telegram_id
from Markups.user_profile_markups import profile_settings_markups
from OtherTools.MonthConverter import format_ukrainian_datetime_with_year


def show_user_profile_back(message):
    header = "<b>Ваш обліковий запис:</b>"

    acc_id = message.chat.id
    user_data = get_user_data_by_telegram_id(acc_id)

    if user_data:
        name, mail, phone_number, registration_time, role = user_data[1], user_data[2], user_data[3], user_data[4], user_data[5]

        registration_date = datetime.strptime(registration_time, "%Y-%m-%d %H:%M:%S")
        current_date = datetime.now()
        registration_duration = current_date - registration_date
        registration_days = max(1, registration_duration.days)

        formatted_date = format_ukrainian_datetime_with_year(registration_time)

        if registration_days == 1:
            days_suffix = "день"
        elif 2 <= registration_days <= 4:
            days_suffix = "дня"
        else:
            days_suffix = "днів"

        if role == 1:
            role_info = "🛡️ Ви авторизовані як <b>Модератор</b>"
        elif role == 2:
            role_info = "👑 Ви авторизовані як <b>Адміністратор</b>"
        else:
            role_info = "👤 Ви авторизовані як <b>Користувач</b>"

        #profile_info = header + f"\n👤 Ім'я: {name}\n📧 Електронна скринька: {mail}\n📞 Номер телефону: {phone_number}\n🕒 Зареєстровано: {registration_time}\n\n{role_info}"
        profile_info = f"{header}\n👤 <b>Ім'я:</b> {name}\n📧 <b>Електронна скринька:</b> {mail}\n📞 <b>Номер телефону:</b> <code>{phone_number}</code>\n🕒 <b>Зареєстровано:</b> {formatted_date} ({registration_days} {days_suffix})\n\n{role_info}"

        return profile_info
    else:
        return "❌ Інформація про користувача не знайдена."
