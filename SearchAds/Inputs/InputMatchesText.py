from SearchAds.SearchMessage import search_message


def process_matches_text_step(bot, message, user_search):
    user_search.matches_text = message.text
    bot.send_message(message.chat.id, "Текст збігів збережено.")
    search_message(bot, message, user_search)
