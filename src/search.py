import re
from collections import Counter


def process_bank_search(data:list[dict], search:str)->list[dict]:
    """
    Функция ищет банковские операции по заданной строке поиска.
    Принимает:
        - data: список словарей с данными о банковских операциях;
        - search: строка поиска в поле "description" (вводит пользователь в консоль в main).
    Возвращает:
        - список словарей с данными о найденных операциях.
    """
    found_transactions = []

    pattern = re.compile(search, re.IGNORECASE)

    for transaction in data:
        found_transaction = re.search(pattern, transaction["description"])
        if found_transaction:
            found_transactions.append(transaction)

    return found_transactions


def process_bank_operations(data:list[dict], categories:list)->dict:
    """
    Функция группирует банковские операции по категориям и считает количество операций в каждой категории.
    Принимает:
        - data: список словарей с данными о банковских операциях;
        - categories: список категорий для группировки (вводит пользователь в консоль в main).
    Возвращает:
        - словарь с данными о группированных операциях в котором ключи — это названия категорий, а
        значения — это количество операций в каждой категории.
    """
    transactions_category_count = Counter()

    for transaction in data:
        description = transaction["description"]

        # Если описание есть в списке категорий — считаем
        if description in categories:
            transactions_category_count[description] += 1

    return dict(transactions_category_count)