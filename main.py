# Импорт функция из модулей masks.py и widget.py
from typing import Dict, Generator, Iterator, List

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card


# Проверка правильной работы функций из модуля masks
def checking_masks_functions() -> None:
    """Тест на правильность маскировки номера карты и счета"""

    card_number = "7000792289606361"  # пример номера карты
    account_number = "73654108430135874305"  # пример номера счета

    masked_card = get_mask_card_number(card_number)
    masked_account = get_mask_account(account_number)

    print(f"Замаскированный номер карты: {masked_card}")
    print(f"Замаскированный номер счета: {masked_account}")


# Проверка правильности функций mask_account_card из модуля widget
def checking_widget_functions1(account_card: str) -> str:
    """Тест правильности маскировки номера карты и счета"""

    hidden_account_card = mask_account_card(account_card)

    return hidden_account_card


# Проверка правильности работы функции get_date из модуля widget
def checking_widget_functions2(date_iso_8601: str) -> str:
    """Тест правильности извлечения даты в обычном формате из международного стандарта написания даты и времени"""

    extracted_date = get_date(date_iso_8601)

    return extracted_date


# Проверка работы функций из модуля processing.py
def checking_filter_by_state(my_list: list, state: str = "EXECUTED") -> list:
    """Тест правильности фильтрации данных в виде списка словарей - my_list по 'state'"""
    filtered_list = filter_by_state(my_list, state)

    return filtered_list


def checking_sort_by_date(my_list: list, descending: bool = True) -> list:
    """Тест правильности сортировки данных в виде списка словарей - my_list по 'date'"""
    sorted_list = sort_by_date(my_list, descending)

    return sorted_list


# Примеры использования функций модуля generators.py:
# 0. filter_by_currency.
transaction = [
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


def checking_filter_by_currency(transaction_list: List[Dict], currency: str) -> Iterator[Dict]:
    """
    Пример использования функции filter_by_currency.
    Принимает:
        transaction (List[Dict]): Список словарей с транзакциями.
    Возвращает:
        при обращении (через next()) возвращает отфильтрованные по коду валюты транзакции.
    """
    usd_transactions = filter_by_currency(transaction_list, currency)

    return usd_transactions


# 1. transaction_descriptions.
def checking_transaction_descriptions(transactions: List[Dict]) -> Generator[str, None, None]:
    """
    Пример использования функции transaction_descriptions.
    Принимает:
        transaction (List[Dict]): Список словарей с транзакциями.
    Возвращает:
        через next() - описание транзакции str ("description").
    """
    descriptions = transaction_descriptions(transactions)

    return descriptions


# 2. card_number_generator.
def checking_card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """
    Пример использования функции card_number_generator.
    Принимает:
        start - начальное значение диапазона;
        stop - конечное значение диапазона.
    Возвращает:
        номера банковских карт в формате XXXX XXXX XXXX XXXX.
    """
    number_generator = card_number_generator(start, stop)

    return number_generator


# 3. decorators - log.
def checking_log_to_file() -> None:
    """
    Пример использования декоратора log с записью в файл.
    Декоратор логирует время запуска/завершения работы функции с микросекундами.
    """
    from src.decorators import log

    @log(filename="test_log_example.txt")
    def my_function(x: (int, float), y: (int, float)) -> (int, float):
        return x + y

    result = my_function(5, 7)
    return result


def checking_log_to_console() -> None:
    """
    Пример использования декоратора log с выводом в консоль.
    Декоратор логирует время запуска/завершения работы функции с микросекундами.
    """
    from src.decorators import log

    @log()
    def my_function(x: (int, float), y: (int, float)) -> (int, float):
        return x * y

    result = my_function(3, 4)
    return result


# Запуск функций из модулей
if __name__ == "__main__":
    checking_masks_functions()
    print(checking_widget_functions1("Счет 64686473678894779589"))
    print(checking_widget_functions2("2024-03-11T02:26:18.671407"))

    """
    Примеры входных данных для проверки функции модуля widget.py
    Maestro 1596837868705199
    Счет 64686473678894779589
    MasterCard 7158300734726758
    Счет 35383033474447895560
    Visa Classic 6831982476737658
    Visa Platinum 8990922113665229
    Visa Gold 5999414228426353
    Счет 73654108430135874305
    """

    # Данные для проверки функций из модуля processing.py

    print(
        checking_filter_by_state(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            "CANCELED",
        )
    )

    print(
        sort_by_date(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            False,
        )
    )

    # Примеры использования функций модуля generators.py:
    # 0. filter_by_currency.

    result_filtering = checking_filter_by_currency(transaction, "USD")
    try:
        for _ in range(2):
            print(next(result_filtering))
    except StopIteration:
        print("Итератор исчерпан.")

    # Сверка результат:
    """
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
    """

# 1. transaction_descriptions.
result_descriptions = checking_transaction_descriptions(transaction)
try:
    for _ in range(5):
        print(next(result_descriptions))
except StopIteration:
    print("Итератор исчерпан.")

# Сверка результат:
"""
"Перевод организации",
"Перевод со счета на счет",
"Перевод со счета на счет",
"Перевод с карты на карту",
"Перевод организации"
"""

# 2. card_number_generator.

for card_number in checking_card_number_generator(1, 5):
    print(card_number)

# Сверка результат:
"""
0000 0000 0000 0001
0000 0000 0000 0002
0000 0000 0000 0003
0000 0000 0000 0004
0000 0000 0000 0005
"""

# 3. log.
print("\nДекоратор log с записью в файл:")
print(checking_log_to_file())

# Сверка результата:
"""
Декоратор log с записью в файл:
Запуск my_function в 12:47:04.127582
12
"""

print("\nДекоратор log с выводом в консоль:")
print(checking_log_to_console())

# Сверка результата:
"""
Декоратор log с выводом в консоль:
Запуск my_function в 12:47:04.128235
Завершение my_function c результатом: 12 в 12:47:04.128252.
12
"""
