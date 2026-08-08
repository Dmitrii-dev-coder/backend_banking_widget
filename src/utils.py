import json

def get_transactions_from_file(path_file):
    """
    Получает транзакции из файла в JSON формате.
    Принимает: path_file - путь к файлу.
    Возвращает: список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """

    with open(f'{path_file}/transactions.json', 'r', encoding='utf-8') as transactions_file:
        try:
            transactions = json.loads(transactions_file)
        except json.JSONDecodeError:
            transactions = []

    return transactions