# Импорт встроенных модулей Python - re и datetime
import re
from datetime import datetime

# Импорт функций проекта из masks
from src.masks import get_mask_account, get_mask_card_number

# Текст ошибки для валидации номера карты или счёта
ERROR_TEXT = (
    "Неправильный номер карты (<Логотип платежной системы (Visa Classic, Visa Platinum, "
    "Visa Gold, MasterCard, Maestro) ________________ (16 цифр)>) или неправильный номер счета "
    "(<Счет ____________________ (20 цифр)>)"
)

# Допустимые логотипы карт
VALID_CARD_LOGOS = ["Visa Classic", "Visa Platinum", "Visa Gold", "MasterCard", "Maestro"]


def mask_account_card(account_card: str) -> str:
    """Маскирует полученный номер карты или счёта.

    Проверяет корректность формата номера карты или счёта.
    В случае ошибки выбрасывает ValueError с текстом ERROR_MESSAGE.
    """

    # Извлекаем буквенную и числовую части
    letters_part = "".join(re.findall(r"\D+", account_card))
    numbers_part = "".join(re.findall(r"\d+", account_card))

    # Переменная для результата (требуется для совместимости с проектом)
    hidden_account_card = ""

    # Проверка для счёта
    if letters_part.strip() == "Счет":
        if len(numbers_part) != 20 or not numbers_part.isdigit():
            raise ValueError(ERROR_TEXT)
        hidden_account_card = f"{letters_part} {get_mask_account(numbers_part)}"

    # Проверка для карты
    elif letters_part.strip() in VALID_CARD_LOGOS:
        if len(numbers_part) != 16 or not numbers_part.isdigit():
            raise ValueError(ERROR_TEXT)
        hidden_account_card = f"{letters_part} {get_mask_card_number(numbers_part)}"

    # Если не счёт и не известная карта — ошибка
    else:
        raise ValueError(ERROR_TEXT)

    return hidden_account_card


def get_date(date_iso_8601: str) -> str:
    """Конвертирует дату из международного стандарта в обычный формат 'ДД.ММ.ГГГГ'"""

    error_text = (
        "Функция обрабатывает данные только в международном стандарте времени ISO 8601, "
        "возможно вы ввели не верную дату, с несуществующим месяцем, или днем, "
        "а так же время указанно не верно, не принимаются не существующие часы, минуты или секунды"
    )
    try:
        formatted_date = datetime.strptime(date_iso_8601, "%Y-%m-%dT%H:%M:%S.%f")
        return formatted_date.strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError(error_text)
