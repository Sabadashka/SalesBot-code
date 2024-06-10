from DataBase.Advertisement_database import get_user_info_by_advertisement_id
from OtherTools.GetUserNameTelegram import get_username_from_acc_id, get_nick_from_acc_id
from OtherTools.MonthConverter import format_ukrainian_datetime_with_year
from datetime import datetime


def show_owner_info(bot, call, ad_id):
    get_owner_info = get_user_info_by_advertisement_id(ad_id)

    header = 'ℹ️ <b>Інформація про користувача:</b>'

    if get_owner_info:
        telegram_id, name, mail, phone_number, registration_time = get_owner_info[0], get_owner_info[1], get_owner_info[
            2], get_owner_info[3], \
            get_owner_info[4]

        registration_date = datetime.strptime(get_owner_info[4], "%Y-%m-%d %H:%M:%S")
        current_date = datetime.now()
        registration_duration = current_date - registration_date
        registration_days = max(1, registration_duration.days)

        formatted_date = format_ukrainian_datetime_with_year(get_owner_info[4])

        if registration_days == 1:
            days_suffix = "день"
        elif 2 <= registration_days <= 4:
            days_suffix = "дня"
        else:
            days_suffix = "днів"

        user_link = get_nick_from_acc_id(bot, telegram_id, name)
        #user_link = f"<a href='tg://openmessage?user_id={telegram_id}'>{name}</a>"

        profile_info = f"{header}\n👤 <b>Ім'я:</b> {user_link}\n📧 <b>Електронна скринька:</b> {mail}\n📞 <b>Номер телефону:</b> <code>{phone_number}</code>\n🕒 <b>Зареєстровано: </b>{formatted_date} \n⚠️ <b>Користувач з нами:</b> {registration_days} {days_suffix}!"
        bot.send_message(call.message.chat.id, profile_info, reply_to_message_id=call.message.message_id,
                         parse_mode='HTML', disable_web_page_preview=True)

    else:
        bot.send_message(call.message.chat.id, "❗️ Сталась якась невідома помилка...\nКористувача не знайдено...", reply_to_message_id=call.message.message_id)