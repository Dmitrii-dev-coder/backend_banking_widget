# Импорт встроенных модулей Python - re и datetime
import re
from datetime import datetime

# Импорт функций проекта из masks
from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str) -> str:
    """Маскирует полученный номер карты или счета"""

    if "Счет" in account_card:  # Создается маска для счета
        letters_part = "".join(re.findall(r"\D+", account_card))
        numbers_part = "".join(re.findall(r"\d+", account_card))
        hidden_account_card = f"{letters_part} {get_mask_account(numbers_part)}"
    else:  # Создается маска для номера карты
        letters_part = "".join(re.findall(r"\D+", account_card))
        numbers_part = "".join(re.findall(r"\d+", account_card))
        hidden_account_card = f"{letters_part} {get_mask_card_number(numbers_part)}"

    return hidden_account_card


def get_date(date_iso_8601: str) -> str:
    """Конвертирует дату из международного стандарта в обычный формат 'ДД.ММ.ГГГГ'"""

    formatted_date = datetime.strptime(date_iso_8601, "%Y-%m-%dT%H:%M:%S.%f")

    return formatted_date.strftime("%d.%m.%Y")
