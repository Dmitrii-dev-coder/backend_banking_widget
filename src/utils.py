import json
from typing import Any

from src.logger import setup_logger

logger = setup_logger("utils", "logs/utils.log")


def get_transactions_from_json_file(file_path: str) -> list[dict[str, Any]]:
    """
    Получает транзакции из файла в JSON формате.

    Принимает:
        file_path: путь к JSON-файлу.

    Возвращает:
        список словарей с данными о финансовых транзакциях.
        Если файл пустой, содержит не список или не найден,
        функция возвращает пустой список.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as operations_file:
            try:
                transactions = json.loads(operations_file.read())
                logger.debug(f"Транзакции успешно загружены из файла {file_path}")
                if not isinstance(transactions, list):
                    logger.error(f"Ошибка при загрузке транзакций из файла {file_path}:")
                    return []
            except json.JSONDecodeError:
                logger.error(f"Ошибка при декодировании JSON в файле {file_path}:")
                return []
    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден.")
        return []

    return transactions
