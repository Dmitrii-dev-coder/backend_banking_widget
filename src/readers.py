import pandas as pd
import numpy as np
from typing import Any

from src.logger import setup_logger

logger = setup_logger("readers", "logs/readers.log")


def get_transactions_from_csv_file(file_path: str) -> list[dict[str, Any]]:
    """
     Получает транзакции из csv-файла.

     Принимает:
        file_path: путь к csv-файлу.

    Возвращает:
        список словарей с данными о финансовых транзакциях.
    """
    try:
        logger.debug(f"Функция get_transactions_from_csv_file запущена с параметром {file_path}")
        df = pd.read_csv(file_path)

        # Заменяем NaN на None для безопасной конвертации и возможной сериализации
        df = df.replace({np.nan: None})

        transactions = df.to_dict('records')
        logger.debug(f"Транзакции успешно загружены из файла {file_path}")
        return transactions
    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден.")
        return []
    except pd.errors.EmptyDataError:
        logger.error(f"Файл {file_path} пуст.")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {type(e).__name__}: {e}")
        return []


def get_transactions_from_excel_file(file_path: str) -> list[dict[str, Any]]:
    """
    Получает транзакции из excel-файла.

     Принимает:
        file_path: путь к excel-файлу.

    Возвращает:
        список словарей с данными о финансовых транзакциях.
    """
    try:
        logger.debug(f"Функция get_transactions_from_excel_file запущена с параметром {file_path}")
        df = pd.read_excel(file_path)
        df = df.replace({np.nan: None})
        transactions = df.to_dict('records')
        logger.debug(f"Транзакции успешно загружены из файла {file_path}")
        return transactions
    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден.")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {type(e).__name__}: {e}")
        return []