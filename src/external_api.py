import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_sum_of_transaction(transaction: dict[str, Any]) -> float:
    """
    Считает сумму транзакции в рублях.

    Принимает:
        transaction: одна транзакция из списка транзакций.

    Возвращает:
        сумму транзакции в рублях.

    Если транзакция была в USD или EUR, происходит обращение к внешнему API
    для получения текущего курса валюты и конвертации суммы операции в рубли.
    """
    if transaction["operationAmount"]["currency"]["code"] != "RUB":
        exchange_to = "RUB"
        exchange_from = transaction["operationAmount"]["currency"]["code"]
        transaction_amount = float(transaction["operationAmount"]["amount"])
        if API_KEY is None:
            raise ValueError("API_KEY not found in environment variables")
        headers = {"apikey": API_KEY}
        url = (
            f"https://api.apilayer.com/exchangerates_data/convert"
            f"?to={exchange_to}&from={exchange_from}&amount={transaction_amount}"
        )
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise ValueError("Failed to get currency rate")
        return float(response.json()["result"])

    transaction_amount = float(transaction["operationAmount"]["amount"])
    return transaction_amount
