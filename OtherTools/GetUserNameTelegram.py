def get_username_from_acc_id(bot, acc_id):
    user = bot.get_chat(acc_id)

    return user.first_name


def get_nick_from_acc_id(bot, acc_id, name):
    try:
        user = bot.get_chat(acc_id)
        if user.username:
            user_link = f"<a href='https://t.me/{user.username}'>{name}</a>"

    except Exception as e:
        print(f"{name} (Виникла непередбачувана помилка: {str(e)})")
        user_link = f"{name}"

    return user_link
