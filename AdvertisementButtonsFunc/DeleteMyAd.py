from DataBase.Advertisement_database import delete_advertisement, get_all_info_about_advertisement, change_status


def delete_my_ad(bot, call, ad_id):
    info = get_all_info_about_advertisement(ad_id)

    if info is not None:
        name = info[4]
        name_markdown = f"*{name}*"

        message_id = call.message.message_id

        bot.send_message(call.message.chat.id, f"❗️ Ви усішно видалили своє оголошення '{name_markdown}'",
                         parse_mode='Markdown')

        bot.delete_message(call.message.chat.id, message_id)

        new_status = 'deleted'
        change_status(ad_id, new_status)
    else:
        bot.send_message(call.message.chat.id, "❗️ Помилка при отриманні інформації про оголошення. Спробуйте ще раз.")
