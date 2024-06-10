import sqlite3
import uuid
from datetime import datetime


def generate_unique_question_id():
    while True:
        unique_id = "question_" + str(uuid.uuid4())[:8]
        existing_question_id = get_question_id(unique_id)

        if existing_question_id is None:
            return unique_id


def create_new_question(telegram_id, question_text):
    with sqlite3.connect('users.db') as connect:
        cursor = connect.cursor()

        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        question_id = generate_unique_question_id()

        question_status = 'none'

        cursor.execute("""
            INSERT INTO questions (question_id, telegram_id, question_text, question_status, question_date)
            VALUES (?, ?, ?, ?, ?)
        """, (question_id, telegram_id, question_text, question_status, current_datetime))

        connect.commit()


def get_question_id(question_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT question_id FROM questions WHERE question_id = ?", (question_id,))
    existing_question_id = cursor.fetchone()
    connect.close()

    return existing_question_id


def get_questions_with_status_none(acc_id):
    with sqlite3.connect('users.db') as connect:
        cursor = connect.cursor()

        cursor.execute(
            f"SELECT * FROM questions WHERE question_status = 'none' OR question_status = 'on review {acc_id}'")

        return cursor.fetchall()


def set_status_question(question_id, new_status):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("UPDATE questions SET question_status = ? WHERE question_id = ?", (new_status, question_id))

    connect.commit()
    connect.close()


def get_info_question(question_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM questions WHERE question_id = ?", (question_id,))

    question_data = cursor.fetchone()

    connect.close()

    return question_data


def get_questions_where_status_on_moderation_id(acc_id):
    with sqlite3.connect('users.db') as connect:
        cursor = connect.cursor()

        cursor.execute(f"SELECT * FROM questions WHERE question_status = 'on review {acc_id}'")

        return cursor.fetchall()
