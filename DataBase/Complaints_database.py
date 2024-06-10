import uuid
from datetime import datetime
import sqlite3


def generate_unique_complaint_id():
    while True:
        unique_id = "ad_" + str(uuid.uuid4())
        existing_complain_id = get_complaints_id(unique_id)

        if existing_complain_id is None:
            return unique_id


def create_new_complaint(telegram_id, advertisement_id):
    with sqlite3.connect('users.db') as connect:
        cursor = connect.cursor()

        complaint_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        complaint_id = generate_unique_complaint_id()

        complaint_text = "No info"

        # Вставка нової скарги у таблицю "complaints"
        cursor.execute("""
            INSERT INTO complaints (complaint_id, telegram_id, advertisement_id, complaint_text, complaint_status, complaint_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (complaint_id, telegram_id, advertisement_id, complaint_text, "none", complaint_date))

        connect.commit()


def get_complaints_id(complaint_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT advertisement_id FROM advertisements WHERE advertisement_id = ?", (complaint_id,))
    existing_complain_id = cursor.fetchone()
    connect.close()

    return existing_complain_id


def is_advertisement_in_complaints(telegram_id, ad_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE telegram_id = ? AND advertisement_id = ?",
                   (telegram_id, ad_id))
    count = cursor.fetchone()[0]

    connect.close()

    return count > 0


def get_complaints_with_status_none(acc_id):
    with sqlite3.connect('users.db') as connect:
        cursor = connect.cursor()

        cursor.execute(f"SELECT * FROM complaints WHERE complaint_status = 'none' OR complaint_status = 'on review {acc_id}'")

        return cursor.fetchall()


def get_complaints_where_admin_on_review(acc_id):
    with sqlite3.connect('users.db') as connect:
        cursor = connect.cursor()

        # Отримати скарги зі статусом 'none'
        cursor.execute(f"SELECT * FROM complaints WHERE complaint_status = 'on review {acc_id}'")
        #complaint_id = cursor.fetchone()
        return cursor.fetchall()


def set_status_for_ad_without_violation(complaint_id, new_status):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("UPDATE complaints SET complaint_status = ? WHERE complaint_id = ?", (new_status, complaint_id))

    connect.commit()
    connect.close()


def get_info_complaint_by_complaint_id(complaint_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute('SELECT * FROM complaints WHERE complaint_id = ?', (complaint_id,))
    result = cursor.fetchone()

    return result


def get_user_from_complaint(ad_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT telegram_id FROM complaints WHERE advertisement_id = ?", (ad_id,))
    user = cursor.fetchone()

    connect.close()
    user_id = user[0] if user else None
    return user_id
