import os

import requests
from dotenv import load_dotenv


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
        exchange_to = "RUB"
        exchange_from = transaction["operationAmount"]["currency"]["code"]
        transaction_amount = float(transaction["operationAmount"]["amount"])
        headers = {"apikey": API_KEY}
        url = f'https://api.apilayer.com/exchangerates_data/convert?to={exchange_to}&from={exchange_from}&amount={transaction_amount}'
        response = requests.get(url, headers=headers)

        return response.json()["result"]

    else:
        transaction_amount = float(transaction["operationAmount"]["amount"])

        return transaction_amount


transaction = {
"id": 41428829,
"state": "EXECUTED",
"date": "2019-07-03T18:35:29.512364",
"operationAmount": {
  "amount": "8221.37",
  "currency": {
    "name": "USD",
    "code": "USD"
  }
},
"description": "Перевод организации",
"from": "MasterCard 7158300734726758",
"to": "Счет 35383033474447895560"
}

result = get_sum_of_transaction(transaction)
print(result)


