import sqlite3
from datetime import datetime


def create_new_user(telegram_id, name, mail, phone_number):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    # Отримуємо поточну дату та час
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO users (telegram_id, name, mail, phone_number, registration_time, role)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (telegram_id, name, mail, phone_number, current_datetime, 0))  # Додавання 0 для поля 'role'

    connect.commit()
    connect.close()


def set_new_login(telegram_id, new_login):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("UPDATE users SET login = ? WHERE telegram_id = ?", (new_login, telegram_id))

    connect.commit()
    connect.close()


def set_new_name(telegram_id, new_name):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("UPDATE users SET name = ? WHERE telegram_id = ?", (new_name, telegram_id))

    connect.commit()
    connect.close()


def set_new_mail(telegram_id, new_mail):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("UPDATE users SET mail = ? WHERE telegram_id = ?", (new_mail, telegram_id))

    connect.commit()
    connect.close()


def set_new_phone_number(telegram_id, new_phone_number):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("UPDATE users SET phone_number = ? WHERE telegram_id = ?", (new_phone_number, telegram_id))

    connect.commit()
    connect.close()


def get_user_data(acc_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (acc_id,))

    user_data = cursor.fetchone()

    if user_data:
        columns = [column[0] for column in cursor.description]
        user_dict = dict(zip(columns, user_data))
        return user_dict
    else:
        return None


def get_user_mail(acc_id):
    with sqlite3.connect('users.db') as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT mail FROM users WHERE telegram_id = ?", (acc_id,))
        user_mail_data = cursor.fetchone()

    return user_mail_data[0] if user_mail_data is not None else None


def get_user_mail_by_id(telegram_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT mail FROM users WHERE telegram_id = ?", (telegram_id,))

    user_mail_data = cursor.fetchone()

    connect.close()

    return user_mail_data[0] if user_mail_data else None


def delete_user_data(acc_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(f"DELETE FROM users WHERE telegram_id = {acc_id}")
    connect.commit()


def get_user_data_by_telegram_id(telegram_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user_data = cursor.fetchone()

    return user_data


def check_password(acc_id, entered_password):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("SELECT password FROM users WHERE telegram_id = ?", (acc_id,))
    user_password = cursor.fetchone()
    connect.close()

    return user_password and entered_password == user_password[0]


def get_user_role(acc_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("SELECT role FROM users WHERE telegram_id = ?", (acc_id,))
    user_role = cursor.fetchone()
    connect.close()

    return user_role


def get_owner_email_by_advertisement_id_from_complaints(advertisement_id):
    try:
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()

        query = """
            SELECT users.mail
            FROM users
            JOIN advertisements ON users.telegram_id = advertisements.telegram_id
            WHERE advertisements.advertisement_id = ?
            """

        cursor.execute(query, (advertisement_id,))

        result = cursor.fetchone()

        connection.close()

        return result[0] if result else None

    except sqlite3.Error as error:
        print("Помилка з'єднання з базою даних:", error)
        return None


def get_user_email_by_complaint_id(complaint_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    try:
        cursor.execute("SELECT telegram_id FROM complaints WHERE complaint_id = ?", (complaint_id,))
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
    finally:
        connect.close()


# Для адміна
def get_all_users_from_db():
    with sqlite3.connect('users.db') as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM users")

    users_data = cursor.fetchall()
    connect.close()

    return users_data


def change_role_by_id(acc_id, new_role):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE users SET role = ? WHERE telegram_id = ?", (new_role, acc_id))
    connect.commit()
    connect.close()


def check_user_exists(user_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (user_id,))
    user_data = cursor.fetchone()

    connection.close()

    return user_data is not None


def get_all_users_id():
    users_id = []
    with sqlite3.connect('users.db') as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT telegram_id FROM users")
        rows = cursor.fetchall()
        for row in rows:
            users_id.append(row[0])

    return users_id