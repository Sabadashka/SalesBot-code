import datetime


def format_ukrainian_datetime(date_str):
    month_translation = {
        'January': 'січ.',
        'February': 'лют.',
        'March': 'бер.',
        'April': 'квіт.',
        'May': 'трав.',
        'June': 'черв.',
        'July': 'лип.',
        'August': 'серп.',
        'September': 'вер.',
        'October': 'жов.',
        'November': 'лист.',
        'December': 'груд.'
    }

    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

    month_name = date_obj.strftime('%B')
    translated_month = month_translation.get(month_name, month_name)

    formatted_date = date_obj.strftime(f'%d {translated_month} %H:%M')

    return formatted_date


def format_ukrainian_datetime_with_year(date_str):
    month_translation = {
        'January': 'січ.',
        'February': 'лют.',
        'March': 'бер.',
        'April': 'квіт.',
        'May': 'трав.',
        'June': 'черв.',
        'July': 'лип.',
        'August': 'серп.',
        'September': 'вер.',
        'October': 'жов.',
        'November': 'лист.',
        'December': 'груд.'
    }

    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

    month_name = date_obj.strftime('%B')
    translated_month = month_translation.get(month_name, month_name)

    year = date_obj.year

    formatted_date_with_year = date_obj.strftime(f'%d {translated_month} {year}')

    return formatted_date_with_year


def format_ukrainian_datetime_with_year_for_notifications(date_str):
    month_translation = {
        'January': 'січ.',
        'February': 'лют.',
        'March': 'бер.',
        'April': 'квіт.',
        'May': 'трав.',
        'June': 'черв.',
        'July': 'лип.',
        'August': 'серп.',
        'September': 'вер.',
        'October': 'жов.',
        'November': 'лист.',
        'December': 'груд.'
    }

    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

    month_name = date_obj.strftime('%B')
    translated_month = month_translation.get(month_name, month_name)

    year = date_obj.year

    formatted_date_with_year = date_obj.strftime(f' %H:%M | %d {translated_month} {year}')

    return formatted_date_with_year
