import sqlite3
import uuid
from datetime import datetime


def generate_unique_notified_id():
    while True:
        unique_id = "notified_" + str(uuid.uuid4())[:5]
        existing_notified_id = get_notified_id(unique_id)

        if existing_notified_id is None:
            return unique_id


def create_new_notified(telegram_id, advertisement_id):
    notified_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    notified_id = generate_unique_notified_id()

    with sqlite3.connect('users.db') as connect:
        cursor = connect.cursor()
        cursor.execute("""
            INSERT INTO notified_users_ad_deactivation (notified_id, telegram_id, advertisement_id, notified_date)
            VALUES (?, ?, ?, ?)
        """, (notified_id, telegram_id, advertisement_id, notified_date))


def get_notified_id(notified_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT notified_id FROM notified_users_ad_deactivation WHERE notified_id = ?", (notified_id,))
    existing_notified_id = cursor.fetchone()
    connect.close()

    return existing_notified_id


def get_notified_user(telegram_id, advertisement_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT notified_id FROM notified_users_ad_deactivation WHERE telegram_id = ? AND advertisement_id = ?", (telegram_id, advertisement_id))
    existing_notified_id = cursor.fetchone()
    connect.close()

    return existing_notified_id


def check_notified(telegram_id, advertisement_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM notified_users_ad_deactivation WHERE telegram_id = ? AND advertisement_id = ?",
                   (telegram_id, advertisement_id))
    existing_notification = cursor.fetchone()
    connect.close()

    return existing_notification


def get_notified_id_by_ids(advertisement_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT notified_id FROM notified_users_ad_deactivation WHERE advertisement_id = ?",
                   (advertisement_id,))
    existing_notification = cursor.fetchone()
    connect.close()

    return existing_notification


def delete_notified_user(notified_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("DELETE FROM notified_users_ad_deactivation WHERE notified_id = ?", notified_id)
    connect.commit()
    connect.close()
