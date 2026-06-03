# Импорт функция из модулей masks.py и widget.py
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


# Проверка правильной работы функций из модуля masks
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


# Проверка работы функций из модуля processing.py
def checking_filter_by_state(my_list: list, state: str = "EXECUTED") -> list:
    """Тест правильности фильтрации данных в виде списка словарей - my_list по 'state'"""
    filtered_list = filter_by_state(my_list, state)

    return filtered_list


def checking_sort_by_date(my_list: list, descending: bool = True) -> list:
    """Тест правильности сортировки данных в виде списка словарей - my_list по 'date'"""
    sorted_list = sort_by_date(my_list, descending)

    return sorted_list


# Запуск функций из модулей
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

    # Данные для проверки функций из модуля processing.py

    print(
        checking_filter_by_state(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            "CANCELED",
        )
    )

    print(
        sort_by_date(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            False,
        )
    )



