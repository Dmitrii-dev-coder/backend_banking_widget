# Проверка функции get_sum_of_transaction.
from unittest.mock import patch

from external_api import get_sum_of_transaction


# Тест 001: Позитивная проверка, транзакция в рублях, API  не вызывается.
def test_get_sum_of_transaction_positive_rub():
    """ """
    transaction = {
    "id": 587085106,
    "state": "EXECUTED",
    "date": "2018-03-23T10:45:06.972075",
    "operationAmount": {
      "amount": "48223.05",
      "currency": {
        "name": "руб.",
        "code": "RUB"
      }
    },
    "description": "Открытие вклада",
    "to": "Счет 41421565395219882431"
  }

    result = get_sum_of_transaction(transaction)
    assert result == 48223.05

# Тест 002: Позитивная проверка, транзакция в иностранной валюте, Mock имитирует ответ API, возвращает result.
@patch('external_api.get_sum_of_transaction.requests.get')
def test_get_sum_of_transaction_not_in_rub(mock_requests_get):
    """ """

    transaction = {
    "id": 142264268,
    "state": "EXECUTED",
    "date": "2019-04-04T23:20:05.206878",
    "operationAmount": {
      "amount": "79114.93",
      "currency": {
        "name": "USD",
        "code": "USD"
      }
    }

    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {
  "success": true,
  "query": {
    "from": "USD",
    "to": "RUB",
    "amount": 79114.93
  },
  "info": {
    "rate": 92.5
  },
  "result": 7318131.03
}

    assert get_sum_of_transaction(transaction) == 7318131.03
    mock_requests_get.assert_called_once_with(transaction)





# Тест 003: Негативная проверка, Mock — requests.get не вернул 200 — имитируется ошибка, проверка на обработку.

