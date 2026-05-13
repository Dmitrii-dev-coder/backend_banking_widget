import re

import pytest

from src.widget import get_date, mask_account_card

# 0. Проверка функции mask_account_card.
# Тест 001: Тестирование правильности маскирования номера счета и номера карты.


@pytest.mark.parametrize(
    "account_card, expected",
    [
        ("Maestro 1596837868705199", "Maestro  1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет  **9589"),
        ("MasterCard 7158300734726758", "MasterCard  7158 30** **** 6758"),
        ("Счет 35383033474447895560", "Счет  **5560"),
        ("Visa Classic 6831982476737658", "Visa Classic  6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum  8990 92** **** 5229"),
        ("Visa Gold 5999414228426353", "Visa Gold  5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет  **4305"),
    ],
)
def test_mask_account_card_valid_account_card(account_card: str, expected: str) -> None:
    """Корректное маскирование номеров карт и счетов различных платёжных систем."""
    assert mask_account_card(account_card) == expected


# Тест 002 Тестирование правильности работы функции с не правильным форматом номера карты или счета.


@pytest.mark.parametrize(
    "account_card",
    [
        "Счет 1234567890123456",  # 16 цифр (вставили номер карты)
        "Maestro abcde12345",  # в цифровом номере карты присутствуют буквы
        "Visa Cosmos 5999414228426353",  # Неизвестный логотип
        "Account 64686473678894779589",  # Вместо слова "Счет" другое слово
        "64686473678894779589",  # пропущено слово "Счет"
        "Счет ",  # нет цифр номера счета
        "Maestro ",  # нет цифр номера карты
        "Visa Gold 35383033474447895560",  # 20 цифр (вставили номер счета)
        "",
    ],
)
def test_mask_account_card_not_correct_account_card(account_card: str) -> None:
    """Некорректный формат строки вызывает ValueError с читаемым сообщением."""
    error_text = (
        "Неправильный номер карты (<Логотип платежной системы (Visa Classic, Visa Platinum, "
        "Visa Gold, MasterCard, Maestro) ________________ (16 цифр)>) или неправильный номер счета "
        "(<Счет ____________________ (20 цифр)>)"
    )
    expected_error = re.escape(error_text)

    with pytest.raises(ValueError, match=expected_error):
        mask_account_card(account_card)


# Тест 003: Проверка, что функция корректно обрабатывает None вместо валидных номеров счета и карты.


def test_get_mask_card_number_none_input() -> None:
    """Передача None в mask_account_card вызывает ValueError или TypeError."""
    account_card = None
    with pytest.raises((ValueError, TypeError)):
        mask_account_card(account_card)  # type: ignore[arg-type]


# 1. Проверка функции get_date.
# Тест 101: Тестирование правильности конвертации времени из международного стандарта в обычный (дд.мм.гггг).


def test_get_date_with_valid_data() -> None:
    """Корректное преобразование ISO-даты в формат ДД.ММ.ГГГГ."""
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"


# Тест 102: Тестирование правильности работы функции если входящие данные имею граничные значения.


@pytest.mark.parametrize(
    "date_iso_8601, expected",
    [
        ("2024-03-11T00:00:00.000000", "11.03.2024"),
        ("2025-05-12T23:59:59.999999", "12.05.2025"),
        ("2024-02-29T02:26:18.671407", "29.02.2024"),
    ],
)
def test_get_date_with_boundary_values_data(date_iso_8601: str, expected: str) -> None:
    """Граничные значения дат (начало/конец дня, 29 февраля) корректно преобразуются."""
    assert get_date(date_iso_8601) == expected


# Тест 103: Тестирование функции на вход не корректных данных.


@pytest.mark.parametrize(
    "invalid_data",
    [
        "2024-03-11",  # Обычный стандарт вместо международного
        "2024/03/11T14:45",  # Не соответствие международному стандарту
        "2024-13-20T02:26:18.671407",  # Не существующий месяц
        "2024-04-31T02:26:18.671407",  # Не существующий день в апреле
        "2025-02-29T02:26:18.671407",  # 29 февраля в не високосный год
        "2024-04-20T25:26:18.671407",  # Не существующий час
        "2024-04-20T02:61:18.671407",  # Не существующие минуты
        "2024-04-20T02:26:61.671407",  # Не существующие секунды
        "2024-04-20T02:26:-18.671407",  # Отрицательное значение времени (минуты)
    ],
)
def test_get_date_with_invalid_data(invalid_data: str) -> None:
    """Некорректные значения дат вызывают ValueError с сообщением из функции."""
    error_text = (
        "Функция обрабатывает данные только в международном стандарте времени ISO 8601, "
        "возможно вы ввели не верную дату, с несуществующим месяцем, или днем, "
        "а так же время указанно не верно, не принимаются не существующие часы, минуты или секунды"
    )

    with pytest.raises(ValueError) as exc_info:
        get_date(invalid_data)

    assert str(exc_info.value) == error_text


# Тест 104: Тестирование функции на пустую строку или None.


@pytest.mark.parametrize(
    "date_iso_8601",
    [
        None,
        "",
    ],
)
def test_get_date_with_no_date(date_iso_8601: str | None) -> None:
    """Пустая строка или None вызывают ValueError либо TypeError."""
    with pytest.raises((ValueError, TypeError)):
        get_date(date_iso_8601)  # type: ignore[arg-type]
