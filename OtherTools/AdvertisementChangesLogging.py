from datetime import datetime

from DataBase.Advertisement_database import write_new_changes_ad


def save_new_changes(ad_id, text, old, new):
    # write_new_changes_ad
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if text == 'name_log':
        new_changes_text = f'\n>>> *{current_datetime}* >>> Назву змінено змінено з "{old}" на "{new}"'
        write_new_changes_ad(ad_id, new_changes_text)

    elif text == 'description_log':
        new_changes_text = f'\n>>> *{current_datetime}* >>> Опис змінено з "{old}" на "{new}"'
        write_new_changes_ad(ad_id, new_changes_text)

    elif text == 'photos_log':
        new_changes_text = f'\n>>> *{current_datetime}* >>> Оновлено фотографії оголошення'
        write_new_changes_ad(ad_id, new_changes_text)

    elif text == 'price_log':
        new_changes_text = f'\n>>> *{current_datetime}* >>> Ціну змінено з "{old}" на "{new}"'
        write_new_changes_ad(ad_id, new_changes_text)

    elif text == 'location_log':
        new_changes_text = f'\n>>> *{current_datetime}* >>> Місцезнаходження змінено з "{old}" на "{new}"'
        write_new_changes_ad(ad_id, new_changes_text)

    elif text == 'deactivate_log':
        new_changes_text = f'\n>>> *{current_datetime}* >>> Оголошення деактивовано власником'
        write_new_changes_ad(ad_id, new_changes_text)

    elif text == 'activate_log':
        new_changes_text = f'\n>>> *{current_datetime}* >>> Оголошення активовано власником'
        write_new_changes_ad(ad_id, new_changes_text)

    elif text == 'extend_log':
        new_changes_text = f'\n>>> *{current_datetime}* >>> Оголошення продовжено на 30 днів власником'
        write_new_changes_ad(ad_id, new_changes_text)