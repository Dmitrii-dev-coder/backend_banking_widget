def filter_by_currency():
    pass


def transaction_descriptions():
    pass


def card_number_generator():
    pass


if __name__ == '__main__':

    # Проверка работы filter_by_currency.

    usd_transactions = filter_by_currency(transactions, "USD")
    for _ in range(2):
        print(next(usd_transactions))

    >> > {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    }
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188"
    }

    # Проверка работы transaction_descriptions.

    descriptions = transaction_descriptions(transactions)
    for _ in range(5):
        print(next(descriptions))

    >>> Перевод организации
        Перевод со счета на счет
        Перевод со счета на счет
        Перевод с карты на карту
        Перевод организации

    # Проверка работы card_number_generator.

for card_number in card_number_generator(1, 5):
    print(card_number)

>>> 0000 0000 0000 0001
    0000 0000 0000 0002
    0000 0000 0000 0003
    0000 0000 0000 0004
    0000 0000 0000 0005


