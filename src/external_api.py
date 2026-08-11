import os

import requests
from dotenv import load_dotenv

from src.utils import get_transactions_from_file

load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_sum_of_transaction(transaction):
    """
    Считает сумму транзакции в рублях.

    Принимает: transaction - одну транзакцию из transactions - списка транзакций.

    Возвращает: сумму транзакции в рублях.

    Если транзакция не в рублях, а в USD или EUR, то конвертирует ее в рубли, обращаясь для конвертации валюты к
    Exchange Rates Data API: https://apilayer.com/exchangerates_data-api. .
    """

    if transaction["operationAmount"]["currency"]["code"] != "RUB":
        exchenge_to = "RUB"
        exchenge_from = transaction["operationAmount"]["currency"]["code"]
        transaction_amount = transaction["operationAmount"]["amount"]
        headers = {"apikey": API_KEY}
        url = f'https://api.apilayer.com/exchangerates_data/convert?to={exchenge_to}&from={exchenge_from}&amount={transaction_amount}'
        response = requests.get(url, headers=headers)

        return response.json()

    else:
        if transaction["operationAmount"]["currency"]["code"] == "RUB":
            transaction_amount = float(transaction["operationAmount"]["amount"])

            return transaction_amount


