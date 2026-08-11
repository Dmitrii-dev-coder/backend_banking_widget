import json

def get_transactions_from_file(file_path):
    """
    Получает транзакции из файла в JSON формате.
    Принимает: path_file - путь к файлу.
    Возвращает: список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as operations_file:
            try:
                transactions = json.loads(operations_file.read())
                if not isinstance(transactions, list):
                    return []
            except json.JSONDecodeError:
                transactions = []
    except FileNotFoundError:
        return []

    return transactions


if __name__ == "__main__":
    result = get_transactions_from_file('data/operations.json')
    print(result)
