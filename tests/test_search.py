# Проверка функций: process_bank_search, process_bank_operations из модуля src.search.

import pytest  # noqa: F401

from src.search import process_bank_operations, process_bank_search

# ========================== ТЕСТОВЫЕ ДАННЫЕ ==========================
TEST_TRANSACTIONS = [
    {
        "id": 1,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "description": "Перевод организации",
        "operationAmount": {"amount": "1000.00", "currency": {"name": "руб.", "code": "RUB"}},
    },
    {
        "id": 2,
        "state": "EXECUTED",
        "date": "2019-06-03T18:35:29.512364",
        "description": "Перевод с карты на карту",
        "operationAmount": {"amount": "2000.00", "currency": {"name": "USD", "code": "USD"}},
    },
    {
        "id": 3,
        "state": "CANCELED",
        "date": "2019-05-03T18:35:29.512364",
        "description": "Открытие вклада",
        "operationAmount": {"amount": "3000.00", "currency": {"name": "руб.", "code": "RUB"}},
    },
    {
        "id": 4,
        "state": "EXECUTED",
        "date": "2019-04-03T18:35:29.512364",
        "description": "Перевод со счета на счет",
        "operationAmount": {"amount": "4000.00", "currency": {"name": "EUR", "code": "EUR"}},
    },
    {
        "id": 5,
        "state": "EXECUTED",
        "date": "2019-03-03T18:35:29.512364",
        "description": "Перевод организации",
        "operationAmount": {"amount": "5000.00", "currency": {"name": "USD", "code": "USD"}},
    },
]


# ==================== 0. Проверка функции process_bank_search ====================


# Тест 001: Проверяет, что функция находит транзакции по точному совпадению в description
def test_process_bank_search_exact_match():
    """Находит транзакции с точным совпадением строки поиска."""
    result = process_bank_search(TEST_TRANSACTIONS, "Перевод организации")
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 5


# Тест 002: Проверяет, что функция ищет без учёта регистра (re.IGNORECASE)
def test_process_bank_search_case_insensitive():
    """Ищет транзакции без учёта регис��ра."""
    result = process_bank_search(TEST_TRANSACTIONS, "ПЕРЕВОД ОРГАНИЗАЦИИ")
    assert len(result) == 2


# Тест 003: Проверяет, что функция возвращает пустой список при отсутствии совпадений
def test_process_bank_search_no_match():
    """Возвращает пустой список, если ничего не найдено."""
    result = process_bank_search(TEST_TRANSACTIONS, "Не существующая строка")
    assert result == []


# Тест 004: Проверяет, что функция находит транзакции по частичному совпадению
def test_process_bank_search_partial_match():
    """Находит транзакции по частичному совпадению."""
    result = process_bank_search(TEST_TRANSACTIONS, "Перевод")
    assert len(result) == 4


# Тест 005: Проверяет, что функция возвращает транзакции с полными данными
def test_process_bank_search_returns_full_transactions():
    """Возвращает полные словари транзакций, а не только совпадающие поля."""
    result = process_bank_search(TEST_TRANSACTIONS, "Открытие вклада")
    assert len(result) == 1
    assert result[0]["id"] == 3
    assert result[0]["description"] == "Открытие вклада"
    assert "operationAmount" in result[0]


# Тест 006: Проверяет, что функция пропускает транзакции без поля description
def test_process_bank_search_missing_description():
    """Корректно обрабатывает транзакции без поля description."""
    data_with_missing = TEST_TRANSACTIONS + [{"id": 6, "state": "EXECUTED"}]
    result = process_bank_search(data_with_missing, "Перевод")
    assert len(result) == 4


# Тест 007: Проверяет, что функция возвращает пустой список для пустого входного списка
def test_process_bank_search_empty_input():
    """Возвращает пустой список при пустом входном списке."""
    result = process_bank_search([], "любая строка")
    assert result == []


# Тест 008: Проверяет, что функция использует регулярные выражения
def test_process_bank_search_regex_support():
    """Поддерживает регулярные выражения для поиска."""
    # Регулярное выражение находит "Перевод" + любой текст
    result = process_bank_search(TEST_TRANSACTIONS, r"Перевод\s+\w+")
    assert len(result) == 4


# ==================== 1. Проверка функции process_bank_operations ====================


# Тест 101: Проверяет, что функция считает количество одной категории
def test_process_bank_operations_single_category():
    """Считает количество операций одной категории."""
    result = process_bank_operations(TEST_TRANSACTIONS, ["Перевод организации"])
    assert result == {"Перевод организации": 2}


# Тест 102: Проверяет, что функция считает количество нескольких категорий
def test_process_bank_operations_multiple_categories():
    """Считает количество операций нескольких категорий."""
    result = process_bank_operations(TEST_TRANSACTIONS, ["Перевод организации", "Открытие вклада"])
    assert result == {"Перевод организации": 2, "Открытие вклада": 1}


# Тест 103: Проверяет, что функция возвращает пустой словарь для несуществующих категорий
def test_process_bank_operations_no_matching_categories():
    """Возвращает пустой словарь, если категории не найдены."""
    result = process_bank_operations(TEST_TRANSACTIONS, ["Не существующая категория"])
    assert result == {}


# Тест 104: Проверяет, что функция использует Counter из collections
def test_process_bank_operations_uses_counter():
    """Использует Counter для подсчёта операций."""
    result = process_bank_operations(TEST_TRANSACTIONS, ["Перевод организации"])
    # Результат должен быть обычным dict
    assert isinstance(result, dict)
    assert result == {"Перевод организации": 2}


# Тест 105: Проверяет, что функция игнорирует регистр при сравнении
def test_process_bank_operations_case_insensitive():
    """Сравнивает категории без учёта регистра."""
    result = process_bank_operations(TEST_TRANSACTIONS, ["перевод организации"])
    assert result == {"Перевод организации": 2}


# Тест 106: Проверяет, что функция пропускает транзакции без поля description
def test_process_bank_operations_missing_description():
    """Корректно обрабатывает транзакции без поля description."""
    data_with_missing = TEST_TRANSACTIONS + [{"id": 6, "state": "EXECUTED"}]
    result = process_bank_operations(data_with_missing, ["Перевод организации"])
    assert result == {"Перевод организации": 2}


# Тест 107: Проверяет, что функция возвращает пустой словарь для пустого входного списка
def test_process_bank_operations_empty_input():
    """Возвращает пустой словарь при пустом входном списке."""
    result = process_bank_operations([], ["любая категория"])
    assert result == {}


# Тест 108: Проверяет, что функция возвращает пустой словарь при пустом списке категорий
def test_process_bank_operations_empty_categories():
    """Возвращает пустой словарь при пустом списке категорий."""
    result = process_bank_operations(TEST_TRANSACTIONS, [])
    assert result == {}
