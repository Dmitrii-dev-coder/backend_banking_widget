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



def card_number_generator(start, stop):
    """
    Принимает: начальное (start) и конечное (stop) значение карты.

    Возвращает: номера банковских карт в формате XXXX XXXX XXXX XXXX, где X — цифра номера карты.
    """
    if start > stop:
        raise ValueError("Начальное значение задаваемого диапазона не может быть больше конечного значения диапазона!")

    for number in range(start, stop + 1):
        if number < 0:
            raise ValueError("Число не может быть отрицательным")
        numbers = str(number).zfill(16)
        format_num = f"{numbers[:4]} {numbers[4:8]} {numbers[8:12]} {numbers[12:]}"
        yield format_num


if __name__ == '__main__':
    new_number = card_number_generator(123456788, 123456789)

    print(next(new_number))

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


