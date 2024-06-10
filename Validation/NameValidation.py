import re


def validate_name(name):
    name_pattern = re.compile(r'^[А-ЯІЇЄҐ][а-яіїєґ]+\s[А-ЯІЇЄҐ][а-яіїєґ]+$')
    return bool(name_pattern.match(name))
