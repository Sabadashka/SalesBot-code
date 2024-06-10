import sqlite3
import uuid
from datetime import datetime


def generate_unique_action_id():
    while True:
        unique_id = "action_" + str(uuid.uuid4())[:8]
        existing_action_id = get_action_id(unique_id)

        if existing_action_id is None:
            return unique_id


def create_answer_action(telegram_id, question_id, answer_text):
    with sqlite3.connect('users.db') as connect:
        cursor = connect.cursor()

        action_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        action_id = generate_unique_action_id()

        cursor.execute("""INSERT INTO answer_actions(action_id, telegram_id, question_id, answer_text, action_date) 
                          VALUES (?, ?, ?, ?, ?)""",
                       (action_id, telegram_id, question_id, answer_text, action_date))

        connect.commit()


def get_action_id(action_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("SELECT action_id FROM answer_actions WHERE action_id = ?", (action_id,))
    existing_action_id = cursor.fetchone()
    connect.close()

    return existing_action_id


def get_top_moderators_by_answers():
    try:
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()

        cursor.execute("""
            SELECT aa.telegram_id, COUNT(*) AS actions_count 
            FROM answer_actions AS aa
            JOIN users AS u ON aa.telegram_id = u.telegram_id 
            WHERE u.role = '1' 
            GROUP BY aa.telegram_id 
            ORDER BY actions_count DESC
        """)

        top_moderators_by_answers = cursor.fetchall()

        connection.close()

        return top_moderators_by_answers
    except sqlite3.Error as e:
        print("SQLite error:", e)
