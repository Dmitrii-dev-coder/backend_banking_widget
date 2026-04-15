# Импорт функция из модулей masks.py и widget.py
from src.masks import get_mask_account, get_mask_card_number
from src.widget import get_date, mask_account_card


# Проверка правильной работы функция из модуля masks
def checking_masks_functions() -> None:
    """Тест на правильность маскировки номера карты и счета"""

    card_number = "7000792289606361"  # пример номера карты
    account_number = "73654108430135874305"  # пример номера счета

    masked_card = get_mask_card_number(card_number)
    masked_account = get_mask_account(account_number)

    print(f"Замаскированный номер карты: {masked_card}")
    print(f"Замаскированный номер счета: {masked_account}")


# Проверка правильности функций mask_account_card из модуля widget
def checking_widget_functions1(account_card: str) -> str:
    """Тест правильности маскировки номера карты и счета"""

    hidden_account_card = mask_account_card(account_card)

    return hidden_account_card


# Проверка правильности работы функции get_date из модуля widget
def checking_widget_functions2(date_iso_8601: str) -> str:
    """Тест правильности извлечения даты в обычном формате из международного стандарта написания даты и времени"""

    extracted_date = get_date(date_iso_8601)

    return extracted_date


if __name__ == "__main__":
    checking_masks_functions()
    print(checking_widget_functions1("Счет 64686473678894779589"))
    print(checking_widget_functions2("2024-03-11T02:26:18.671407"))

    """
    Примеры входных данных для проверки функции модуля widget.py
    Maestro 1596837868705199
    Счет 64686473678894779589
    MasterCard 7158300734726758
    Счет 35383033474447895560
    Visa Classic 6831982476737658
    Visa Platinum 8990922113665229
    Visa Gold 5999414228426353
    Счет 73654108430135874305
    """
