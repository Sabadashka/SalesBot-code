import sqlite3
import uuid
from datetime import datetime


def generate_unique_notification_id():
    while True:
        unique_id = "notification_" + str(uuid.uuid4())[:8]
        existing_notification_id = get_notification_id(unique_id)

        if existing_notification_id is None:
            return unique_id


def create_notification(telegram_id, notification_title, notification_text):
    with sqlite3.connect('users.db') as connect:
        cursor = connect.cursor()

        notification_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        notification_id = generate_unique_notification_id()

        notification_status = 'Нове'

        cursor.execute("""INSERT INTO notifications(notification_id, telegram_id, notification_title, notification_text, notification_status, notification_date) 
                          VALUES (?, ?, ?, ?, ?, ?)""",
                       (notification_id, telegram_id, notification_title, notification_text, notification_status, notification_date))

        connect.commit()


def get_notification_id(notification_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT notification_id FROM notifications WHERE notification_id = ?", (notification_id,))
    existing_notification_id = cursor.fetchone()
    connect.close()

    return existing_notification_id


def get_notifications_by_user_id(telegram_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM notifications WHERE telegram_id = ?", (telegram_id,))
    notifications = cursor.fetchall()

    connect.close()

    return notifications


def get_notification_by_id(notification_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM notifications WHERE notification_id = ?", (notification_id,))
    notification = cursor.fetchone()

    connect.close()

    return notification


def change_notification_status(notification_id, new_status):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    #cursor.execute("SELECT * FROM advertisements WHERE advertisement_status = 'on moderation'", (ad_id,))
    cursor.execute("UPDATE notifications SET notification_status = ? WHERE notification_id = ?", (new_status, notification_id))
    connect.commit()
    connect.close()

