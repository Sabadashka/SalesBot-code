import sqlite3
from datetime import datetime, timedelta


def create_advertisement(adv_id, telegram_id, category, subcategory, name, description, photo_folder, price, condition, region, city):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    current_time = datetime.now()

    new_advertisement_until = current_time + timedelta(days=30)

    advertisement_until = new_advertisement_until.strftime("%Y-%m-%d %H:%M:%S")

    text = f'>>> Оголошення створено {current_datetime}\n'

    cursor.execute("""
        INSERT INTO advertisements (advertisement_id, telegram_id, advertisement_category, advertisement_subcategory, advertisement_name, advertisement_description, advertisement_photo_folder, advertisement_price, advertisement_date, advertisement_until, advertisement_country, advertisement_region, advertisement_city, advertisement_status, advertisement_changes, advertisement_condition)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (adv_id, telegram_id, category, subcategory, name, description, photo_folder, price, current_datetime, advertisement_until, 'Україна', region, city, 'on moderation', text, condition))

    connect.commit()
    connect.close()


def get_user_advertisements(user_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM advertisements WHERE telegram_id = ?", (user_id,))
    advertisements = cursor.fetchall()

    connect.close()

    return advertisements


def get_user_advertisements_with_status_published(user_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM advertisements WHERE telegram_id = ? AND advertisement_status = 'published'", (user_id,))
    advertisements = cursor.fetchall()

    connect.close()

    return advertisements


def get_user_advertisements_with_status_on_moderation(user_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM advertisements WHERE telegram_id = ? AND advertisement_status = 'on moderation'", (user_id,))
    advertisements = cursor.fetchall()

    connect.close()

    return advertisements


def get_user_advertisements_with_status_deactivated(user_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM advertisements WHERE telegram_id = ? AND advertisement_status = 'deactivated'", (user_id,))
    advertisements = cursor.fetchall()

    connect.close()

    return advertisements


def get_user_advertisements_with_status_deleted(user_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM advertisements WHERE telegram_id = ? AND advertisement_status = 'deleted'", (user_id,))
    advertisements = cursor.fetchall()

    connect.close()

    return advertisements


def delete_advertisement(adv_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("DELETE FROM advertisements WHERE advertisement_id = ?", (adv_id,))

    connect.commit()
    connect.close()


def get_ads_id(adv_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT advertisement_id FROM advertisements WHERE advertisement_id = ?", (adv_id,))
    existing_ad = cursor.fetchone()
    connect.close()

    return existing_ad


def get_all_info_about_advertisement(ad_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM advertisements WHERE advertisement_id = ?", (ad_id,))

    ad_data = cursor.fetchone()

    connect.close()

    return ad_data


def get_all_info_about_add_by_subcategory(subcategory):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM advertisements WHERE advertisement_subcategory = ? AND advertisement_status = 'published'", (subcategory,))
    ad_info_by_subcategory = cursor.fetchall()
    connect.close()

    return ad_info_by_subcategory


def get_info_for_moderation(acc_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute(f"SELECT * FROM advertisements WHERE advertisement_status = 'on moderation' OR advertisement_status = 'on review {acc_id}'")
    ad_info_by_subcategory = cursor.fetchall()
    connect.close()

    return ad_info_by_subcategory


def get_ads_where_moderation_on_review(acc_id):
    with sqlite3.connect('users.db') as connect:
        cursor = connect.cursor()

        # Отримати скарги зі статусом 'none'
        cursor.execute(f"SELECT * FROM advertisements WHERE advertisement_status = 'on review {acc_id}'")
        return cursor.fetchall()


def set_status_for_ad_on_review(ad_id, new_status):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("UPDATE advertisements SET advertisement_status = ? WHERE advertisement_id = ?", (new_status, ad_id))

    connect.commit()
    connect.close()


def change_status(ad_id, new_status):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("UPDATE advertisements SET advertisement_status = ? WHERE advertisement_id = ?", (new_status, ad_id))
    connect.commit()
    connect.close()


def change_status_with_new_time(ad_id, new_status):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    current_time = datetime.now()
    new_advertisement_until = current_time + timedelta(days=30)

    until = new_advertisement_until.strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("UPDATE advertisements SET advertisement_status = ?, advertisement_date = ?, advertisement_until = ? WHERE advertisement_id = ?", (new_status, date, until, ad_id))
    connect.commit()
    connect.close()


def delete_ad_with_violation(adv_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("DELETE FROM favorites WHERE advertisement_id = ?", (adv_id,))

    connect.commit()
    connect.close()


def get_user_id_by_ad_id(ad_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT telegram_id FROM advertisements WHERE advertisement_id = ?", (ad_id,))
    user_info_by_ad_id = cursor.fetchone()
    connect.close()

    return user_info_by_ad_id


def get_user_info_by_advertisement_id(advertisement_id):
    # З'єднання з базою даних
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    try:
        query = """
        SELECT * FROM users
        WHERE telegram_id = (
            SELECT telegram_id FROM advertisements
            WHERE advertisement_id = ?
        );
        """
        cursor.execute(query, (advertisement_id,))
        user_info = cursor.fetchone()

        return user_info

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None

    finally:
        connection.close()


def get_user_email_by_advertisement_id(advertisement_id):
    with sqlite3.connect('users.db') as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT telegram_id FROM advertisements WHERE advertisement_id = ?", (advertisement_id,))
        result = cursor.fetchone()

        if result:
            telegram_id = result[0]

            cursor.execute("SELECT mail FROM users WHERE telegram_id = ?", (telegram_id,))
            email_result = cursor.fetchone()

            if email_result:
                return email_result[0]
            else:
                return None
        else:
            return None


def set_new_photo_folder_with_photos_ad(ad_id, new_folder_ad):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("UPDATE advertisements SET advertisement_photo_folder = ? WHERE advertisement_id = ?", (new_folder_ad, ad_id))

    connect.commit()
    connect.close()


def set_new_name_ad(ad_id, new_name_ad):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("UPDATE advertisements SET advertisement_name = ? WHERE advertisement_id = ?", (new_name_ad, ad_id))

    connect.commit()
    connect.close()


def set_new_description_ad(ad_id, new_description_ad):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("UPDATE advertisements SET advertisement_description = ? WHERE advertisement_id = ?", (new_description_ad, ad_id))

    connect.commit()
    connect.close()


def set_new_price_ad(ad_id, new_rice_ad):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("UPDATE advertisements SET advertisement_price = ? WHERE advertisement_id = ?", (new_rice_ad, ad_id))

    connect.commit()
    connect.close()


def set_new_location_ad(ad_id, new_region, new_city):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("UPDATE advertisements SET advertisement_region = ?, advertisement_city = ? WHERE advertisement_id = ?", (new_region, new_city, ad_id))

    connect.commit()
    connect.close()


def set_new_category_ad(ad_id, new_category_ad):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("UPDATE advertisements SET advertisement_category = ? WHERE advertisement_id = ?", (new_category_ad, ad_id))

    connect.commit()
    connect.close()


def set_new_subcategory_ad(ad_id, new_subcategory_ad):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("UPDATE advertisements SET advertisement_subcategory = ? WHERE advertisement_id = ?", (new_subcategory_ad, ad_id))

    connect.commit()
    connect.close()


def write_new_changes_ad(ad_id, new_changes):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    existing_text = cursor.execute("SELECT advertisement_changes FROM advertisements WHERE advertisement_id = ?", (ad_id,)).fetchone()[0]

    final_text_changes = f"{existing_text}{new_changes}"

    cursor.execute("UPDATE advertisements SET advertisement_changes = ? WHERE advertisement_id = ?", (final_text_changes, ad_id))
    connect.commit()


def check_and_deactivate_ads():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute("SELECT advertisement_id FROM advertisements WHERE advertisement_status = 'published' AND advertisement_until <= date('now')")
    ads_to_deactivate = cursor.fetchall()

    # Зміна статусу оголошень на "deactivated"
    for ad_id_tuple in ads_to_deactivate:
        ad_id = ad_id_tuple[0]
        print(f'{ad_id} - deactivated')
        deactivate_ad(ad_id)

    connection.commit()
    connection.close()


# Функція для деактивації оголошення
def deactivate_ad(ad_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute("UPDATE advertisements SET advertisement_status = 'deactivated' WHERE advertisement_id = ?", (ad_id,))

    connection.commit()
    connection.close()


# Сповіщення для юзера про деактивацію

def print_ads_for_deactivation():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM advertisements WHERE advertisement_status = 'published' AND date(advertisement_until, '-3 days') <= date('now')")
    ads_to_deactivate = cursor.fetchall()
    connection.close()

    return ads_to_deactivate


def change_date_for_extend_advertisement(ad_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    advertisement_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_datetime = datetime.now()

    new_datetime = current_datetime + timedelta(days=30)

    new_datetime_until_str = new_datetime.strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("UPDATE advertisements SET advertisement_date = ?, advertisement_until = ? WHERE advertisement_id = ?", (advertisement_date, new_datetime_until_str, ad_id))

    connection.commit()
    connection.close()
