# 0. ================================== СОДЕРЖАНИЕ МОДУЛЯ MAIN ====================================
# I. ИМПОРТ БИБЛИОТЕК, ФУНКЦИЙ И МОДУЛЕЙ ПРОЕКТА
# II. ОСНОВНАЯ ФУНКЦИЯ ПРОЕКТА - main()


# I. =============================== ИМПОРТ ФУНКЦИЙ И МОДУЛЕЙ ПРОЕКТА ==============================
from typing import Any, Dict, Generator, Hashable, Iterator, List

import pandas as pd

from src.search import process_bank_search, process_bank_operations
from src.decorators import log
from src.external_api import get_sum_of_transaction
from src.generators import card_number_generator, filter_by_currency, transaction_descriptions
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.readers import get_transactions_from_csv_file, get_transactions_from_excel_file
from src.utils import get_transactions_from_json_file
from src.widget import get_date, mask_account_card


# II. ======================== ОСНОВНАЯ ФУНКЦИЯ ПРОЕКТА - main() ==================================
def main() -> None:
    """Основная функция программы — связывает всю функциональность проекта."""

    # Приветствие и меню
    print("Программа: Привет! Добро пожаловать в программу работы")
    print("с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # Выбор источника
    choice = input("Программа: ")

    if choice == "1":
        print("Программа: Для обработки выбран JSON-файл.")
        data = get_transactions_from_json_file("data/operations.json")
    elif choice == "2":
        print("Программа: Для обработки выбран CSV-файл.")
        data = get_transactions_from_csv_file("data/transactions.csv")
    elif choice == "3":
        print("Программа: Для обработки выбран XLSX-файл.")
        data = get_transactions_from_excel_file("data/transactions_excel.xlsx")
    else:
        print("Программа: Неверный выбор. Используйте 1, 2 или 3.")
        return

    # Фильтрация по статусу (цикл до ввода корректного значения)
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = input(
            "Программа: Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
            "Программа: "
        ).strip().upper()

        if status in valid_statuses:
            print(f'Программа: Операции отфильтрованы по статусу "{status}"')
            data = filter_by_state(data, status)
            break
        else:
            print(f'Программа: Статус операции "{status}" недоступен.')

    # Сортировка по дате
    sort_choice = input("Программа: Отсортировать операции по дате? Да/Нет ").strip().lower()
    if sort_choice in ("да", "yes", "y"):
        order = input("Программа: Отсортировать по возрастанию или по убыванию? ").strip().lower()
        if order in ("возрастание", "по возрастанию"):
            data = sort_by_date(data, descending=False)
        elif order in ("убывание", "по убыванию"):
            data = sort_by_date(data, descending=True)

    # Рублевые транзакции
    ruble_choice = input("Программа: Выводить только рублевые транзакции? Да/Нет ").strip().lower()
    if ruble_choice in ("да", "yes", "y"):
        try:
            data = list(filter_by_currency(data, "RUB"))
        except KeyError:
            data = [t for t in data if t.get("currency_code") == "RUB"]

    # Поиск по слову
    search_choice = input(
        "Программа: Отфильтровать список транзакций по определенному слову\nв описании? Да/Нет "
    ).strip().lower()
    if search_choice in ("да", "yes", "y"):
        search = input("Программа: Введите слово для поиска: ").strip()
        data = process_bank_search(data, search)

    # Вывод результата
    print("Программа: Распечатываю итоговый список транзакций...")

    if not data:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши")
        print("условия фильтрации")
        return

    print(f"Программа: Всего банковских операций в выборке: {len(data)}")

    for transaction in data:
        print()
        print(f"{get_date(transaction['date'])} {transaction['description']}")
        if 'from' in transaction:
            try:
                print(mask_account_card(transaction['from']))
            except ValueError:
                print(transaction['from'])
        if 'to' in transaction:
            try:
                print(mask_account_card(transaction['to']))
            except ValueError:
                print(transaction['to'])
        if 'operationAmount' in transaction:
            print(
                f"Сумма: {transaction['operationAmount']['amount']} {transaction['operationAmount']['currency']['code']}"
            )
        elif 'amount' in transaction and 'currency_code' in transaction:
            print(
                f"Сумма: {transaction['amount']} {transaction['currency_code']}"
            )


if __name__ == "__main__":
    main()
