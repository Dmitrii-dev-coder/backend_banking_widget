def filter_by_currency(transactions, currency):
    """
    Принимает на вход список словарей, представляющих транзакции.

    Функция должна возвращать итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной (например, USD).

    """

    transactions_in_currency = []

    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            transactions_in_currency.append(transaction)

    return iter(transactions_in_currency)



def transaction_descriptions(transactions):
    """
    Принимает на вход список словарей с транзакциями.

    Возвращает описание каждой операции по очереди.
    """
    for transaction in transactions:
        description = transaction["description"]
        yield description



def card_number_generator():
    pass


# if __name__ == '__main__':

    # Проверка работы filter_by_currency.


    # Проверка работы transaction_descriptions.

#     descriptions = transaction_descriptions(transactions)
#     for _ in range(5):
#         print(next(descriptions))
#
#     >>> Перевод организации
#         Перевод со счета на счет
#         Перевод со счета на счет
#         Перевод с карты на карту
#         Перевод организации
#
#     # Проверка работы card_number_generator.
#
# for card_number in card_number_generator(1, 5):
#     print(card_number)
#
# >>> 0000 0000 0000 0001
#     0000 0000 0000 0002
#     0000 0000 0000 0003
#     0000 0000 0000 0004
#     0000 0000 0000 0005


