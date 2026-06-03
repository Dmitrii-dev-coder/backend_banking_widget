from typing import List, Dict, Iterator, Generator

def filter_by_currency(
    transactions: List[Dict], 
    currency: str
) -> Iterator[Dict]:
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


def transaction_descriptions(
    transactions: List[Dict]
) -> Generator[str, None, None]:
    """
    Принимает на вход список словарей с транзакциями.

    Возвращает описание каждой операции по очереди.
    """
    for transaction in transactions:
        description = transaction["description"]
        yield description


def card_number_generator(
    start: int, 
    stop: int
) -> Generator[str, None, None]:
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