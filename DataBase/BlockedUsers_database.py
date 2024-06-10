import sqlite3
import uuid
from datetime import datetime

from DataBase.Users_database import change_role_by_id


def generate_unique_blocked_id():
    while True:
        unique_id = "ban_" + str(uuid.uuid4())
        existing_blocked_id = get_blocked_id(unique_id)

        if existing_blocked_id is None:
            return unique_id


def create_new_blocked_user(telegram_id, blocked_until, blocked_reason, admin_id):
    with sqlite3.connect('users.db') as connect:
        cursor = connect.cursor()

        blocked_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        blocked_id = generate_unique_blocked_id()

        cursor.execute("""INSERT INTO blocked_users(blocked_id, telegram_id, blocked_date, blocked_until, blocked_reason, admin_id) 
                          VALUES (?, ?, ?, ?, ?, ?)""",
                       (blocked_id, telegram_id, blocked_date, blocked_until, blocked_reason, admin_id))

        connect.commit()


def get_blocked_id(blocked_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT blocked_id FROM blocked_users WHERE blocked_id = ?", (blocked_id,))
    existing_blocked_id = cursor.fetchone()
    connect.close()

    return existing_blocked_id


def get_all_data_blocked_user(user_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM blocked_users WHERE telegram_id = ?", (user_id,))
    blocked_user_data = cursor.fetchone()
    connect.close()

    return blocked_user_data


def get_all_blocked_users_from_db():
    with sqlite3.connect('users.db') as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM blocked_users")

    users_data = cursor.fetchall()
    connect.close()

    return users_data


def delete_user_from_blocked(acc_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(f"DELETE FROM blocked_users WHERE telegram_id = {acc_id}")
    connect.commit()


def check_and_unblock_users():
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM blocked_users WHERE blocked_until <= ?", (current_date,))
    blocked_users = cursor.fetchall()

    for user in blocked_users:
        user_id = user[1]
        delete_user_from_blocked(user_id)
        change_role_by_id(user_id, 0)

    connection.commit()
    connection.close()


def check_blocked_user_exists(user_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM blocked_users WHERE telegram_id = ?", (user_id,))
    user_data = cursor.fetchone()

    connection.close()

    return user_data is not None
