# Проверка функции get_sum_of_transaction.
from unittest.mock import Mock, patch

import pytest

from src.external_api import get_sum_of_transaction


# Тест 001: Позитивная проверка, транзакция в рублях, API  не вызывается.
def test_get_sum_of_transaction_positive_rub() -> None:
    """Проверяет транзакцию в рублях — API не вызывается, возвращается исходная сумма."""
    transaction = {
        "id": 587085106,
        "state": "EXECUTED",
        "date": "2018-03-23T10:45:06.972075",
        "operationAmount": {"amount": "48223.05", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Открытие вклада",
        "to": "Счет 41421565395219882431",
    }

    result = get_sum_of_transaction(transaction)
    assert result == 48223.05


# Тест 002: Позитивная проверка, транзакция в иностранной валюте, Mock имитирует ответ API, возвращает result.
@patch("src.external_api.requests.get")
def test_get_sum_of_transaction_not_in_rub(mock_requests_get: Mock) -> None:
    """Проверяет транзакцию в иностранной валюте — Mock имитирует ответ API, возвращает result."""

    transaction = {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    }

    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {"result": 7318131.03}

    assert get_sum_of_transaction(transaction) == 7318131.03


# Тест 003: Негативная проверка, Mock — requests.get не вернул 200 — имитируется ошибка, проверка на обработку.
@patch("src.external_api.requests.get")
def test_get_sum_of_transaction_negative(mock_requests_get: Mock) -> None:
    """Проверяет обработку ошибки API (status_code != 200) — выбрасывается ValueError."""
    transaction = {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    }
    mock_requests_get.return_value.status_code = 404
    mock_requests_get.return_value.json.return_value = {"message": "Not Found"}

    with pytest.raises(ValueError, match="Failed to get currency rate"):
        get_sum_of_transaction(transaction)


# Тест 004: Проверка обработки отсутствующего API_KEY.
@patch("src.external_api.API_KEY", None)
def test_get_sum_of_transaction_no_api_key() -> None:
    """Проверяет, что функция корректно обрабатывает отсутствие API_KEY."""
    transaction = {
        "id": 1,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "100", "currency": {"name": "USD", "code": "USD"}},
    }

    # Теперь мы подменяем переменную прямо внутри модуля
    with pytest.raises(ValueError, match="API_KEY не найден"):
        get_sum_of_transaction(transaction)
