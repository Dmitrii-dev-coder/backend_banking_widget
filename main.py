# ============================= ИМПОРТ ФУНКЦИЙ И МОДУЛЕЙ ПРОЕКТА ==============================
from typing import Any, Dict, Generator, Iterator, List

import pandas as pd

from src.decorators import log
from src.external_api import get_sum_of_transaction
from src.generators import card_number_generator, filter_by_currency, transaction_descriptions
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.readers import get_transactions_from_csv_file, get_transactions_from_excel_file
from src.utils import get_transactions_from_json_file
from src.widget import get_date, mask_account_card


# ============================= ФУНУКЦИИ - ОБЁРТКИ ДЛЯ ВЫЗОВА ФУНКЦИЙ МОДУЛЕЙ =====================
# 0. Модуль masks:
# 0.1 Функция get_mask_card_number.
def run_mask_card_number(card_number: str) -> str:
    """
    Обёртка для функции get_mask_card_number из модуля masks.
    Принимает:
        card_number: номер карты для маскировки.
    Возвращает:
        замаскированный номер карты в формате XXXX XX** **** XXXX.
    """
    masked_card = get_mask_card_number(card_number)

    return masked_card


# 0.2 Функция get_mask_account.
def run_mask_account(account_number: str) -> str:
    """
    Обёртка для функции get_mask_account из модуля masks.
    Принимает:
        account_number: номер счета для маскировки.
    Возвращает:
        замаскированный номер счета в формате **XXXX.
    """
    masked_account = get_mask_account(account_number)

    return masked_account


# 1. Модуль widget:
# 1.1 Функция mask_account_card.
def run_mask_account_card(account_card: str) -> str:
    """
    Обёртка для функции mask_account_card из модуля widget.
    Принимает:
        account_card: номер карты или счёта для маскировки.
    Возвращает:
        замаскированный номер карты или счёта.
    """
    hidden_account_card = mask_account_card(account_card)

    return hidden_account_card


# 1.2 Функция get_date.
def run_get_date(date_iso_8601: str) -> str:
    """
    Обёртка для функции get_date из модуля widget.
    Принимает:
        date_iso_8601: дата в международном формате ISO 8601.
    Возвращает:
        дату в формате ДД.ММ.ГГГГ.
    """
    extracted_date = get_date(date_iso_8601)

    return extracted_date


# 2. Модуль processing:
# 2.1 Функция filter_by_state.
def run_filter_by_state(my_list: list, state: str = "EXECUTED") -> list:
    """
    Обёртка для функции filter_by_state из модуля processing.
    Принимает:
        my_list: список словарей с транзакциями.
        state: статус для фильтрации (по умолчанию EXECUTED).
    Возвращает:
        отфильтрованный список транзакций по заданному статусу.
    """
    filtered_list = filter_by_state(my_list, state)

    return filtered_list


# 2.2 Функция sort_by_date.
def run_sort_by_date(my_list: list, descending: bool = True) -> list:
    """
    Обёртка для функции sort_by_date из модуля processing.
    Принимает:
        my_list: список словарей с транзакциями.
        descending: порядок сортировки (по умолчанию по убыванию).
    Возвращает:
        отсортированный список транзакций по дате.
    """
    sorted_list = sort_by_date(my_list, descending)

    return sorted_list


# 3. Модуль generators:
# 3.1 Функция filter_by_currency.
def run_filter_by_currency(transaction_list: List[Dict], currency: str) -> Iterator[Dict]:
    """
    Обёртка для функции filter_by_currency из модуля generators.
    Принимает:
        transaction_list: список словарей с транзакциями.
        currency: код валюты для фильтрации (например, USD).
    Возвращает:
        итератор транзакций, отфильтрованных по валюте.
    """
    usd_transactions = filter_by_currency(transaction_list, currency)

    return usd_transactions


# 3.2 Функция transaction_descriptions.
def run_transaction_descriptions(transactions: List[Dict]) -> Generator[str, None, None]:
    """
    Обёртка для функции transaction_descriptions из модуля generators.
    Принимает:
        transactions: список словарей с транзакциями.
    Возвращает:
        генератор описаний каждой транзакции.
    """
    descriptions = transaction_descriptions(transactions)

    return descriptions


# 3.3 Функция card_number_generator.
def run_card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """
    Обёртка для функции card_number_generator из модуля generators.
    Принимает:
        start: начальное значение диапазона.
        stop: конечное значение диапазона.
    Возвращает:
        генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.
    """
    number_generator = card_number_generator(start, stop)

    return number_generator


# 4. Модуль decorators:
# 4.1 Функция log.
def run_log_to_file() -> None:
    """
    Обёртка для демонстрации работы декоратора log с записью в файл.
    Декоратор логирует время запуска и завершения работы функции.
    """

    @log(filename="test_log_example.txt")
    def my_function(x: Any, y: Any) -> Any:
        return x + y

    _ = my_function(5, 7)


# 4.2 Функция log.
def run_log_to_console() -> None:
    """
    Обёртка для демонстрации работы декоратора log с выводом в консоль.
    Декоратор логирует время запуска и завершения работы функции.
    """

    @log()
    def my_function(x: Any, y: Any) -> Any:
        return x * y

    _ = my_function(3, 4)


# 5. Модуль utils:
# 5.1 Функция get_transactions_from_file.
def run_get_transactions_from_json_file(file_path: str) -> list[dict[str, Any]]:
    """
    Обёртка для функции get_transactions_from_file из модуля utils.
    Принимает:
        file_path: путь к JSON-файлу с транзакциями.
    Возвращает:
        список словарей с данными о финансовых транзакциях.
    """
    result = get_transactions_from_json_file(file_path)

    return result


# 6. Модуль external_api:
# 6.1 Функция get_sum_of_transaction.
def run_get_sum_of_transaction(transaction: dict[str, Any]) -> float:
    """
    Обёртка для функции get_sum_of_transaction из модуля external_api.
    Принимает:
        transaction: словарь с данными одной транзакции.
    Возвращает:
        сумму транзакции в рублях (float).
    """
    result = get_sum_of_transaction(transaction)

    return result


# 7. Модуль readers:
# 7.1 Функция get_transactions_from_csv_file.
def run_get_transactions_from_csv_file(file_path: str) -> list[dict[str, Any]]:
    """
    Обёртка для функции get_transactions_from_csv_file из модуля readers.
    Принимает:
        file_path: путь к CSV-файлу с транзакциями.
    Возвращает:
        список словарей с данными о финансовых транзакциях.
    """
    result = get_transactions_from_csv_file(file_path)

    return result


# 7.2 Функция get_transactions_from_excel_file.
def run_get_transactions_from_excel_file(file_path: str) -> list[dict[str, Any]]:
    """
    Обёртка для функции get_transactions_from_excel_file из модуля readers.
    Принимает:
        file_path: путь к excel-файлу с транзакциями.
    Возвращает:
        список словарей с данными о финансовых транзакциях.
    """
    result = get_transactions_from_excel_file(file_path)

    return result


# =========================== ЗАПУСК ФУНКЦИЙ ИЗ МОДУЛЕЙ ===========================================================
if __name__ == "__main__":
    # 0. ---------------- Запуск функций из модуля masks ----------------:
    # 0.1 Вызов функции mask_card_number, маскировки номера карты.
    print("\n------ Модуль masks ------ :")
    print("Результат работы функции get_mask_card_number:")
    print(run_mask_card_number("7000792289606361"))

    # 0.2 Вызов функции mask_account, маскировки номера счета.
    print(" ")
    print("Результат работы функции mask_account:")
    print(run_mask_account("73654108430135874305"))

    # 1. ----------------- Запуск функций из модуля widget -----------------:
    # 1.1 Вызов функции mask_account_card, маскировки номера карты и номера счета.
    print("\n------ Модуль widget ------ :")
    print("Результат работы функции mask_account_card:")
    print(run_mask_account_card("Счет 64686473678894779589"))

    # 1.2 Вызов функции get_date, конвертации даты из международного стандарта в обычный формат 'ДД.ММ.ГГГГ'.
    print(" ")
    print("Результат работы функции get_date:")
    print(run_get_date("2024-03-11T02:26:18.671407"))

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

    # 2. ------------------ Запуск функций из модуля processing ------------------:
    # 2.1 Вызов функции filter_by_state, фильтрации данных по ключу "state" (по умолчанию 'EXECUTED').
    print("\n------ Модуль processing ------ :")
    print("Результат работы функции filter_by_state:")
    print(
        run_filter_by_state(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            "CANCELED",
        )
    )

    # 2.2 Вызов функции sort_by_date, сортирующей данные по дате (по умолчанию по убыванию).
    print(" ")
    print("Результат работы функции sort_by_date:")
    print(
        run_sort_by_date(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            False,
        )
    )

    # 3. ------------------ Запуск функций модуля generators ---------------------:
    # 3.1 Вызов функции filter_by_currency - фильтрация по валюте.
    # Тестовые данные для функций генераторов
    test_transactions = [
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

    result_filtering = run_filter_by_currency(test_transactions, "USD")
    try:
        print("\n------ Модуль generators ------ :")
        print("Результат работы функции filter_by_currency:")
        for _ in range(2):
            print(next(result_filtering))
    except StopIteration:
        print("Результат работы функции filter_by_currency:")
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

    # 3.2 Вызов функции transaction_descriptions, которая возвращает описание каждой транзакций по очереди.
    result_descriptions = run_transaction_descriptions(test_transactions)
    try:
        print(" ")
        print("Результат работы функции transaction_descriptions:")
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

    # 3.3 Вызов функции card_number_generator, которая генерирует заданное количество номеров карт.
    print(" ")
    print("Результат работы функции card_number_generator:")
    for card in run_card_number_generator(1, 5):
        print(card)

    # Сверка результат:
    """
    0000 0000 0000 0001
    0000 0000 0000 0002
    0000 0000 0000 0003
    0000 0000 0000 0004
    0000 0000 0000 0005
    """

    # 4. ---------------------- Запуск функций модуля decorators ------------------------:
    # 4.1 Вызов функции log, которая принимает функцию и имя файла и логирует ее вызов в файл.
    print("\n------ Модуль decorators ------ :")
    print("Результат работы функции log записи в файл:")
    run_log_to_file()

    # Сверка результата:
    """
    Декоратор log с записью в файл:
    Запуск my_function в 12:47:04.127582
    12
    """

    # 4.2 Вызов функции log, которая принимает функцию и логирует ее вызов в консоль.
    print(" ")
    print("Результат работы функции log:")
    run_log_to_console()

    # Сверка результата:
    """
    Декоратор log с выводом в консоль:
    Запуск my_function в 12:47:04.128235
    Завершение my_function c результатом: 12 в 12:47:04.128252.
    12
    """

    # 5. -------------------- Запуск функций модуля utils -------------------------------:
    # 5.1 Вызов get_transactions_from_file, которая принимает данные из файла и возвращает список словарей с транзакциями.
    print("\n------ Модуль utils ------ :")
    print("Результат работы функции get_transactions_from_file:")
    print(run_get_transactions_from_json_file("data/operations.json"))

    # Сверка результата:
    """
    Вывод списка транзакций из файла в консоль:
    [{'id': 441945886, 'state': 'EXECUTED', 'date': '2019-08-26T10:50:58.294041',
    'operationAmount': {'amount': '31957.58', 'currency': {'name': 'руб.', 'code': 'RUB'}},
    'description': 'Перевод организации', 'from': 'Maestro 1596837868705199',
    'to': 'Счет 64686473678894779589'},
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364',
    ... (список обрезан для краткости) ...    ]
    """

    # 6. ------------------- Запуск функции модуля external_api ------------------------:
    # 6.1 Вызов функции get_sum_of_transaction, которая считает сумму транзакций в рублях.
    print("\n------ Модуль external_api ------ :")
    print("Результат работы функции get_sum_of_transaction:")
    single_transaction = {
        "id": 214024827,
        "state": "EXECUTED",
        "date": "2018-12-20T16:43:26.929246",
        "operationAmount": {"amount": "70946.18", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 10848359769870775355",
        "to": "Счет 21969751544412966366",
    }
    print(run_get_sum_of_transaction(single_transaction))

    # Сверка результата:
    """
    Вывод суммы выбранной транзакций из файла в рублях:
    5849382.922329 # По курсу на 12.08.2026
    """

    # 7. ------------------- Запуск функций модуля readers ------------------------:
    # 7.1 Вызов функции run_get_transaction_from_csv_file, которая принимает данные из файла и возвращает список словарей с транзакциями.
    print("\n------ Модуль readers ------ :")
    print("Результат работы функции get_transaction_from_csv_file:")

    # Сохраняем данные в переменную, чтобы обработать их через DataFrame
    csv_data = run_get_transactions_from_csv_file("data/transactions.csv")
    print(pd.DataFrame(csv_data).head(3))  # Выводим только первые 3 строки таблицы

    # Сверка результата:
    """
        Результат работы функции get_transaction_from_csv_file:
      id;state;date;amount;currency_name;currency_code;from;to;description
    0  650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol...                  
    1  3598919;EXECUTED;2020-12-06T23:00:58Z;29740;Pe...                  
    2  593027;CANCELED;2023-07-22T05:02:01Z;30368;Shi...                  
    """

    # 7.2 Вызов функции run_get_transaction_from_excel_file, которая принимает данные из файла и возвращает список словарей с транзакциями.
    print(" ")
    print("Результат работы функции get_transaction_from_excel_file:")

    excel_data = run_get_transactions_from_excel_file("data/transactions_excel.xlsx")
    print(pd.DataFrame(excel_data).head(3))  # Выводим только первые 3 строки таблицы

    # Сверка результата:
    """
        Результат работы функции get_transaction_from_excel_file:
              id     state  ...                         to               description
    0   650703.0  EXECUTED  ...  Счет 39745660563456619397       Перевод организации
    1  3598919.0  EXECUTED  ...  Discover 0720428384694643  Перевод с карты на карту
    2   593027.0  CANCELED  ...      Visa 6804119550473710  Перевод с карты на карту
    
    [3 rows x 9 columns]
    """
