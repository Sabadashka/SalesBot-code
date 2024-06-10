import re


def validate_phone_number(phone_number):
    # Перевірка, чи номер телефону має правильний формат
    phone_number_pattern = re.compile(r'^\+\d{12}$')  # Формат: +380XXXXXXXXX
    return bool(phone_number_pattern.match(phone_number))
