import itertools
import json
import pytest
import re

from pathlib import Path

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


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
# Тест 201: Проверяет, что генератор выдает правильные номера карт в заданном диапазоне.
def test_card_number_generator_1_to_5():
    """
    Проверяет, что генератор выдает правильные номера карт в заданном диапазоне.
    Начальное значение (start) = 1.
    Конечное значение (stop) = 5.
    """
    number_generator = card_number_generator(1, 5)
    assert next(number_generator) == "0000 0000 0000 0001"
    assert next(number_generator) == "0000 0000 0000 0002"
    assert next(number_generator) == "0000 0000 0000 0003"
    assert next(number_generator) == "0000 0000 0000 0004"
    assert next(number_generator) == "0000 0000 0000 0005"

# Тест 202: Проверяет корректность форматирования номеров карт
def test_card_number_generator_correct_format():
    """
    Проверяет что функция генерирует номера карт в правильном формате: "XXXX XXXX XXXX XXXX" то есть это строка
    с 16-ю цифрами собранными в группы по четыре, а группы разделены пробелами.
    """

    # Создаем генератор для небольшого диапазона
    generator = card_number_generator(1, 5)

    # Регулярное выражение для проверки формата
    pattern = r'^\d{4} \d{4} \d{4} \d{4}$'

    # Перебираем все значения из генератора и проверяем каждое
    for card_number in generator:
        assert re.match(pattern, card_number) is not None, \
            f"Неверный формат номера: {card_number}"

# Тест 203: Проверяет, что генератор правильно завершает генерацию.
def test_card_number_generator_correct_stop_generation():
    """
    Проверяет, что функция генерирует лишь то количество номеров карт, которое соответствует заданным параметрам.
    """
    start = 1
    stop = 101

    generator = card_number_generator(start, stop)
    count = 0

    # Итерируемся по генератору.
    for _ in generator:
        count += 1

    # Ожидаемое количество элементов: (stop - start + 1)
    expected_count = stop - start + 1

    if count != expected_count:
        raise ValueError(f"Неверное количество сгенерированных номеров. Ожидалось: {expected_count}, получено: {count}")

# Тест 204: Проверяет, что генератор корректно обрабатывает крайние значения диапазона.
def test_card_number_generator_invalid_range():
    """
    Проверяет поведение генератора при некорректном диапазоне (start > stop).
    """
    with pytest.raises(ValueError) as error_info:
        generator = card_number_generator(10, 5)
        # Преобразование в список запустит генератор и вызовет ошибку.
        result = list(generator)

    # Проверка текста ошибки.
    assert "не может быть больше конечного" in str(error_info.value)

# Тест 205: Проверяет, когда начальное диапазона равно конечному.
def test_card_number_generator_single_value():
    """
    Проверяет генерацию, когда start == stop.
    """
    start = 1234567890123456
    stop = 1234567890123456
    expected = ["1234 5678 9012 3456"]

    result = list(card_number_generator(start, stop))

    assert result == expected, f"При start == stop должен быть сгенерирован один номер: {expected}"

# Тест 206: Проверяет генерацию в том случае когда начальное значение равно нулю.
def test_card_number_generator_start_from_zero():
    """
    Проверяет генерацию, начиная с нуля.
    """
    start = 0
    stop = 1
    expected = ["0000 0000 0000 0000", "0000 0000 0000 0001"]

    result = list(card_number_generator(start, stop))

    assert result == expected, "Генерация с нуля должна работать корректно"

# Тест 207: Проверяет правильность форматирования номера карты если конечное значение больше четырех цифр.
def test_card_number_generator_different_digit_lengths():
    """
    Проверяет корректное форматирование номера карты если stop больше XXXX,
    используя itertools.islice для быстрой прокрутки генератора.
    Тестируем на диапазоне от 1 до 10001.
    """
    start = 1
    stop = 10001

    # Создаем генератор
    generator = card_number_generator(start, stop)

    # --- Проверка начала диапазона ---
    assert next(generator) == "0000 0000 0000 0001"
    assert next(generator) == "0000 0000 0000 0002"

    # --- Быстрая прокрутка к концу диапазона ---
    last_element = next(itertools.islice(generator, 9998, None))

    # --- Проверка конца диапазона ---
    # Последнее число должно быть отформатировано правильно
    assert last_element == "0000 0000 0001 0001"
