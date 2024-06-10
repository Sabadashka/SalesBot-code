import requests


def get_exchange_rates():
    base_url = 'https://api.privatbank.ua/p24api/pubinfo'

    response = requests.get(f'{base_url}?json&exchange&coursid=5')
    data = response.json()

    if response.status_code == 200:
        return data
    else:
        print(f"Помилка отримання курсів валют. Статус: {response.status_code}")
        return None


def convert_currency(amount, from_currency, to_currency):
    rates = get_exchange_rates()

    if rates is not None:
        for rate in rates:
            if from_currency == 'UAH' and rate['ccy'] == to_currency:
                converted_amount = round(amount / float(rate['sale']), 2)
                return converted_amount
            elif to_currency == 'UAH' and rate['ccy'] == from_currency:
                converted_amount = round(amount * float(rate['buy']), 2)
                return converted_amount
            elif rate['ccy'] == from_currency:
                from_rate = float(rate['buy'])
            elif rate['ccy'] == to_currency:
                to_rate = float(rate['sale'])
        exchange_rate = to_rate / from_rate
        converted_amount = round(amount * exchange_rate, 2)
        return converted_amount
    else:
        print("Неможливо конвертувати валюту. Перевірте наявність потрібних курсів.")
        return None
