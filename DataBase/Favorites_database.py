import sqlite3
import uuid
from datetime import datetime


def generate_unique_favorite_id():
    while True:
        unique_id = "favorite_" + str(uuid.uuid4())[:8]
        existing_favorite_id = get_favorite_id(unique_id)

        if existing_favorite_id is None:
            return unique_id


def create_new_favorite(telegram_id, advertisement_id):
    with sqlite3.connect('users.db') as connect:
        cursor = connect.cursor()

        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        favorite_id = generate_unique_favorite_id()

        cursor.execute("""
            INSERT INTO favorites (favorite_id, telegram_id, advertisement_id, favorite_date)
            VALUES (?, ?, ?, ?)
        """, (favorite_id, telegram_id, advertisement_id, current_datetime))

        connect.commit()


def get_favorite_id(favorite_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT favorite_id FROM favorites WHERE favorite_id = ?", (favorite_id,))
    existing_favorite_id = cursor.fetchone()
    connect.close()

    return existing_favorite_id


def delete_advertisement_from_favorites(adv_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("DELETE FROM favorites WHERE advertisement_id = ?", (adv_id,))

    connect.commit()
    connect.close()


def get_user_favorites(telegram_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM favorites WHERE telegram_id = ?", (telegram_id,))
    favorites = cursor.fetchall()

    connect.close()
    return favorites


def is_advertisement_in_favorites(telegram_id, ad_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT COUNT(*) FROM favorites WHERE telegram_id = ? AND advertisement_id = ?", (telegram_id, ad_id))
    count = cursor.fetchone()[0]

    connect.close()

    return count > 0


