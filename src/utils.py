import json

def get_transactions_from_file(file_path):
    """
    Получает транзакции из файла в JSON формате.
    Принимает: path_file - путь к файлу.
    Возвращает: список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """

    with open(file_path, 'r', encoding='utf-8') as operations_file:
        try:
            transactions = json.loads('operations_file')
        except json.JSONDecodeError:
            transactions = []

    return transactions

if __name__ == "__main__":
    result = get_transactions_from_file('data/operations.json')
    print(result)
