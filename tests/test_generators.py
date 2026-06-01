import pytest
import json
from pathlib import Path

from src.generators import filter_by_currency, transaction_descriptions


# 0. Проверка функции filter_by_currency.
# Тест 001: Проверяет, что функция корректно фильтрует транзакции по заданной валюте.
@pytest.fixture
def valid_data():
    transactions = [
                {
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
                },
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
                },
                {
                    "id": 873106923,
                    "state": "EXECUTED",
                    "date": "2019-03-23T01:09:46.296404",
                    "operationAmount": {
                        "amount": "43318.34",
                        "currency": {
                            "name": "руб.",
                            "code": "RUB"
                        }
                    },
                    "description": "Перевод со счета на счет",
                    "from": "Счет 44812258784861134719",
                    "to": "Счет 74489636417521191160"
                },
                {
                    "id": 895315941,
                    "state": "EXECUTED",
                    "date": "2018-08-19T04:27:37.904916",
                    "operationAmount": {
                        "amount": "56883.54",
                        "currency": {
                            "name": "USD",
                            "code": "USD"
                        }
                    },
                    "description": "Перевод с карты на карту",
                    "from": "Visa Classic 6831982476737658",
                    "to": "Visa Platinum 8990922113665229"
                },
                {
                    "id": 594226727,
                    "state": "CANCELED",
                    "date": "2018-09-12T21:27:25.241689",
                    "operationAmount": {
                        "amount": "67314.70",
                        "currency": {
                            "name": "руб.",
                            "code": "RUB"
                        }
                    },
                    "description": "Перевод организации",
                    "from": "Visa Platinum 1246377376343588",
                    "to": "Счет 14211924144426031657"
                }
            ]


    return transactions
def test_filter_by_currency_valid_data(valid_data):
    """
    Проверяет, что функция корректно фильтрует транзакции по заданной валюте.

    Принимает: список словарей, представляющих транзакции - transactions, код валюты (например "USD")

    Возвращает: список словарей транзакций, в выбранной валюте.
    """


    usd_transactions = filter_by_currency(valid_data, "USD")
    expected_result1 = {
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

    assert next(usd_transactions) == expected_result1

    expected_result2 = {
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


    assert next(usd_transactions) == expected_result2
# Тест 002: Проверяет, что функция правильно обрабатывает случаи, когда транзакции в заданной валюте отсутствуют.

def test_filter_by_currency_no_currency(valid_data):
    """
    Проверяет, что функция корректно работает если нет транзакций по заданной валюте.

    Принимает: список словарей, представляющих транзакции - transactions, код валюты (например "EUR")

    Возвращает: пустой список.
    """

    assert len(list(filter_by_currency(valid_data, 'EUR'))) == 0

# Тест 003: Проверяет, что генератор не завершается ошибкой при обработке пустого списка.

def test_filter_by_currency_empty_data():
    """
    Проверяет, что функция корректно работает если список транзакций пустой.

    Принимает: пустой список словарей.

    Возвращает: пустой список.
    """
    empty_data = []

    assert len(list(filter_by_currency(empty_data, 'EUR'))) == 0


# 1. Проверка функции transaction_descriptions.
# Тест 101: Проверяет, что функция возвращает корректные описания для каждой транзакции.

def test_transaction_descriptions_valid_data(valid_data):
    """
    Проверяет, что функция корректно и поочередно возвращает описание каждой транзакции.

    Принимает: список словарей, представляющих транзакции - transactions.

    Возвращает поочередно описание ("description") транзакций.
    """

    descriptions = transaction_descriptions(valid_data)
    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод с карты на карту"
    assert next(descriptions) == "Перевод организации"

# Тест 102: Проверяет работу функции с различным количеством входных транзакций, включая пустой список.
def test_transaction_descriptions_diff_length_data():
    """
    Проверяет, что функция корректно обрабатывает списки различной длины:
    а) пустой список;
    б) короткий список - одна транзакция;
    в) длинный список - 100 транзакций.
    Принимает список транзакций.
    Возвращает описание транзакций.
    """

    # Проверка работы функции с пустым списком.
    empty_data = []
    descriptions = list(transaction_descriptions(empty_data))
    assert len(descriptions) == 0

    # Проверка работы функции с коротким списком (одна транзакция).
    short_data = [
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
    ]

    descriptions = transaction_descriptions(short_data)
    assert next(descriptions) == "Перевод со счета на счет"

    # Проверка работы функции с длинным списком (100 транзакций в файле transactions.json).
    with open('test_data\\transactions.json', 'r', encoding='utf-8') as f:
        long_data = json.load(f)
    descriptions = list(transaction_descriptions(long_data))
    assert len(descriptions) == 100



# 2. Проверка функции card_number_generator.