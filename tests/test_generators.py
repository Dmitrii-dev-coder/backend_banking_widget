import itertools
import json
import re
from typing import Dict, Iterator, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# 0. Проверка функции filter_by_currency.
# Тест 001: Проверяет, что функция корректно фильтрует транзакции по заданной валюте.
@pytest.fixture
def valid_data() -> List[Dict]:
    """
    Фикстура, предоставляющая список тестовых транзакций.
    """
    transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]

    return transactions


def test_filter_by_currency_valid_data(valid_data: List[Dict]) -> None:
    """
    Проверяет, что функция корректно фильтрует транзакции по заданной валюте.

    Принимает:
        valid_data (List[Dict]): Список словарей с транзакциями.

    Возвращает:
        None. Проверяет корректность работы через `assert`.
    """

    usd_transactions: Iterator[Dict] = filter_by_currency(valid_data, "USD")

    # Проверяем, что первые две отфильтрованные транзакции верны
    assert next(usd_transactions) == valid_data[0]
    assert next(usd_transactions) == valid_data[1]


# Тест 002: Проверяет, что функция правильно обрабатывает случаи, когда транзакции в заданной валюте отсутствуют.
def test_filter_by_currency_no_currency(valid_data: List[Dict]) -> None:
    """
    Проверяет, что функция корректно работает если нет транзакций по заданной валюте.

    Принимает:
        valid_data (List[Dict]): Список словарей с транзакциями.

    Возвращает:
        None. Проверяет, что результат конвертируется в пустой список.
    """

    # Конвертируем итератор в список и проверяем его длину
    result = list(filter_by_currency(valid_data, "EUR"))
    assert len(result) == 0


# Тест 003: Проверяет, что генератор не завершается ошибкой при обработке пустого списка.
def test_filter_by_currency_empty_data() -> None:
    """
     Проверяет, что функция корректно работает если список транзакций пустой.

    Принимает:
        empty_data (List[Dict]): Пустой список.

    Возвращает:
        None. Проверяет, что результат конвертируется в пустой список.
    """

    empty_data: List[Dict] = []
    result = list(filter_by_currency(empty_data, "EUR"))
    assert len(result) == 0


# 1. Проверка функции transaction_descriptions.
# Тест 101: Проверяет, что функция возвращает корректные описания для каждой транзакции.


def test_transaction_descriptions_valid_data(valid_data: List[Dict]) -> None:
    """
    Проверяет, что функция корректно возвращает описания для каждой транзакции.

    Принимает:
        valid_data (List[Dict]): Список словарей с транзакциями.

    Возвращает:
        None. Проверяет корректность работы через `assert`.
    """

    descriptions = transaction_descriptions(valid_data)

    # Ожидаемые описания в том же порядке, что и в valid_data
    expected_descriptions = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]

    for expected in expected_descriptions:
        assert next(descriptions) == expected


# Тест 102: Проверяет работу функции с различным количеством входных транзакций, включая пустой список.
def test_transaction_descriptions_diff_length_data() -> None:
    """
    Проверяет, что функция корректно обрабатывает списки различной длины:
    а) пустой список;
    б) короткий список - одна транзакция;
    в) длинный список - 100 транзакций.
    Принимает:
        None (данные создаются внутри теста)
    Возвращает:
        None. Проверяет корректность работы через `assert`.
    """

    # Проверка работы функции с пустым списком.
    empty_data: List[Dict] = []
    descriptions = transaction_descriptions(empty_data)
    assert len(list(descriptions)) == 0

    # Проверка работы функции с коротким списком (одна транзакция).
    short_data: List[Dict] = [
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
    ]

    descriptions = transaction_descriptions(short_data)
    assert next(descriptions) == "Перевод со счета на счет"

    # Проверка работы функции с длинным списком (100 транзакций в файле transactions.json).
    with open("test_data\\transactions.json", "r", encoding="utf-8") as f:
        long_data = json.load(f)

    descriptions_generator = transaction_descriptions(long_data)  # сохраняем генератор
    descriptions_list = list(descriptions_generator)  # преобразуем в список один раз
    assert len(descriptions_list) == 100


# 2. Проверка функции card_number_generator.
# Тест 201: Проверяет, что генератор выдает правильные номера карт в заданном диапазоне.
def test_card_number_generator_1_to_5() -> None:
    """
    Проверяет генерацию номеров карт в заданном диапазоне (от 1 до 5).

    Принимает:
        Нет

    Возвращает:
        None. Проверяет корректность работы через `assert`.
    """
    number_generator = card_number_generator(1, 5)
    assert next(number_generator) == "0000 0000 0000 0001"
    assert next(number_generator) == "0000 0000 0000 0002"
    assert next(number_generator) == "0000 0000 0000 0003"
    assert next(number_generator) == "0000 0000 0000 0004"
    assert next(number_generator) == "0000 0000 0000 0005"


# Тест 202: Проверяет корректность форматирования номеров карт
def test_card_number_generator_correct_format() -> None:
    """
     Проверяет что функция генерирует номера карт в правильном формате ("XXXX XXXX XXXX XXXX").

    Принимает:
        Нет

    Возвращает:
        None. Проверяет корректность формата через регулярное выражение.
    """

    # Создаем генератор для небольшого диапазона
    generator = card_number_generator(1, 5)

    # Регулярное выражение для проверки формата
    pattern = r"^\d{4} \d{4} \d{4} \d{4}$"

    # Перебираем все значения из генератора и проверяем каждое
    for card_number in generator:
        assert re.match(pattern, card_number) is not None, f"Неверный формат номера: {card_number}"


# Тест 203: Проверяет, что генератор правильно завершает генерацию.
def test_card_number_generator_correct_stop_generation() -> None:
    """
    Проверяет, что функция генерирует лишь то количество номеров карт, которое соответствует заданным параметрам.

    Принимает:
        None (параметры создаются внутри теста)
    Возвращает:
        None. Проверяет корректность работы через `assert` и `raise`.
    """
    start: int = 1
    stop: int = 101

    generator: Iterator[str] = card_number_generator(start, stop)
    count: int = 0

    # Итерируемся по генератору.
    for _ in generator:
        count += 1

    # Ожидаемое количество элементов: (stop - start + 1)
    expected_count: int = stop - start + 1

    if count != expected_count:
        raise ValueError(
            f"Неверное количество сгенерированных номеров. Ожидалось: {expected_count}, получено: {count}"
        )


# Тест 204: Проверяет, что генератор корректно обрабатывает крайние значения диапазона.
def test_card_number_generator_invalid_range() -> None:
    """
    Проверяет поведение генератора при некорректном диапазоне (start > stop).

    Принимает:
        Нет

    Возвращает:
        None. Проверяет, что вызывается исключение ValueError с правильным сообщением.
    """
    with pytest.raises(ValueError) as error_info:
        # Вызов list() необходим для запуска генератора и генерации ошибки
        list(card_number_generator(10, 5))

    # Проверка текста ошибки.
    assert "не может быть больше конечного" in str(error_info.value)


# Тест 205: Проверяет, когда начальное диапазона равно конечному.
def test_card_number_generator_single_value() -> None:
    """
    Проверяет генерацию, когда start == stop.

    Принимает:
        None (параметры создаются внутри теста)
    Возвращает:
        None. Проверяет корректность работы через `assert`.
    """
    start: int = 1234567890123456
    stop: int = 1234567890123456
    expected: List[str] = ["1234 5678 9012 3456"]

    result: List[str] = list(card_number_generator(start, stop))

    assert result == expected, f"При start == stop должен быть сгенерирован один номер: {expected}"


# Тест 206: Проверяет генерацию в том случае когда начальное значение равно нулю.
def test_card_number_generator_start_from_zero() -> None:
    """
    Проверяет генерацию, начиная с нуля.

    Принимает:
        None (параметры создаются внутри теста)
    Возвращает:
        None. Проверяет корректность работы через `assert`.
    """
    start: int = 0
    stop: int = 1
    expected: List[str] = ["0000 0000 0000 0000", "0000 0000 0000 0001"]

    result: List[str] = list(card_number_generator(start, stop))

    assert result == expected, "Генерация с нуля должна работать корректно"


# Тест 207: Проверяет правильность форматирования номера карты если конечное значение больше четырех цифр.
def test_card_number_generator_different_digit_lengths() -> None:
    """
    Проверяет корректное форматирование на большом диапазоне чисел.

    Принимает:
        Нет

    Возвращает:
        None. Проверяет начало и конец большого диапазона.
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
    assert last_element == "0000 0000 0001 0001"
