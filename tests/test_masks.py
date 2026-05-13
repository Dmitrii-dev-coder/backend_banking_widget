import pytest

from src.masks import get_mask_account, get_mask_card_number

# 0. Проверка функции get_mask_card_number.
# Тест 001: Тестирование правильности маскирования номера карты.


@pytest.fixture
def valid_card_number() -> str:
    """Фикстура: валидный 16-значный номер карты."""
    return "7000792289606361"


def test_get_mask_card_number_with_valid_number(valid_card_number: str) -> None:
    """Корректное маскирование 16-значного номера карты."""
    assert get_mask_card_number(valid_card_number) == "7000 79** **** 6361"


#  Тест 002: Проверка функции на превращение номера карты типа int в тип str.


def test_get_mask_card_number_with_int_number() -> None:
    """Номер карты как int преобразуется в str и маскируется."""
    assert get_mask_card_number(7000792289606361) == "7000 79** **** 6361"


# Тест 003: Проверка работы функции на различных входных форматах номеров карт,
#           включая граничные случаи.


@pytest.mark.parametrize(
    "card_number",
    [
        "1234567890123abc",  # Буквы в номере
        12.34567890123456,  # Float
    ],
)
def test_get_mask_card_number_invalid_characters(card_number: str | float) -> None:
    """Некорректные символы в номере карты вызывают ValueError."""
    with pytest.raises(
        ValueError,
        match="Номер карты должен содержать 16 цифр и никаких других символов",
    ):
        get_mask_card_number(card_number)  # type: ignore[arg-type]


# Тест 004: Проверка работы функции с нестандартной длиной номера карты.


@pytest.mark.parametrize(
    "card_number",
    [
        "",  # Пустая строка
        "12345",  # 5 цифр
        "123456789012345",  # 15 цифр
        "12345678901234567",  # 17 цифр
    ],
)
def test_get_mask_card_number_invalid_length(card_number: str) -> None:
    """Номер карты неверной длины вызывает ValueError."""
    with pytest.raises(
        ValueError,
        match="Номер карты должен содержать 16 цифр и никаких других символов",
    ):
        get_mask_card_number(card_number)


# Тест 005: Проверка, что функция корректно обрабатывает входные строки, где отсутствует номер карты.


def test_get_mask_card_number_invalid_input() -> None:
    """Передача None вызывает ValueError или TypeError."""
    card_number = None
    with pytest.raises((ValueError, TypeError)):
        get_mask_card_number(card_number)  # type: ignore[arg-type]


# Тест 006: Проверка на то, что функция очищает номер карты от пробелов и дефисов.


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234 5678 9012 3456", "1234 56** **** 3456"),
        ("1234-5678-9012-3456", "1234 56** **** 3456"),
        ("1234 - 5678 - 9012 - 3456", "1234 56** **** 3456"),
        ("12 34-56 78-90 12-34 56", "1234 56** **** 3456"),
    ],
)
def test_get_mask_card_number_clean(card_number: str, expected: str) -> None:
    """Функция удаляет пробелы и дефисы перед маскированием."""
    assert get_mask_card_number(card_number) == expected


# Тест 007: Проверка на то, что функция не принимает номера карт состоящие из одинаковых цифр (залипание клавиши).


@pytest.mark.parametrize(
    "card_number",
    [
        "0000000000000000",  # 16 нулей
        "1111111111111111",  # 16 единиц
    ],
)
def test_get_mask_card_number_repeating_digits(card_number: str) -> None:
    """Номер из одинаковых цифр («залипание клавиши») вызывает ValueError."""
    with pytest.raises(ValueError):
        get_mask_card_number(card_number)


# 1. Проверка функции get_mask_account.
# Тест 101: Тестирование правильности маскирования номера карты.


@pytest.fixture
def valid_account_number() -> str:
    """Фикстура: валидный 20-значный номер счёта."""
    return "73654108430135874305"


def test_get_mask_account_with_valid_number(valid_account_number: str) -> None:
    """Корректное маскирование номера счёта (последние 4 цифры)."""
    assert get_mask_account(valid_account_number) == "**4305"


#  Тест 102: Проверка функции на превращение номера счета типа int в тип str.


def test_get_mask_account_with_int_number() -> None:
    """Номер счёта как int преобразуется в str и маскируется."""
    assert get_mask_account(73654108430135874305) == "**4305"


# Тест 103: Проверка работы функции на различных входных форматах номеров счетов,
#           включая граничные случаи.


@pytest.mark.parametrize(
    "account_number",
    [
        "12345678901234567abc",  # Буквы в номере
        12.345678901234567890,  # Float
    ],
)
def test_get_mask_account_invalid_characters(account_number: str | float) -> None:
    """Некорректные символы в номере счёта вызывают ValueError."""
    with pytest.raises(
        ValueError,
        match="Номер счета должен содержать 20 цифр и никаких других символов",
    ):
        get_mask_account(account_number)  # type: ignore[arg-type]


# Тест 104: Проверка работы функции с нестандартной длиной номера счета.


@pytest.mark.parametrize(
    "account_number",
    [
        "",  # Пустая строка
        "1234567890",  # 10 цифр
        "1234567890123456789",  # 19 цифр
        "1234567890123456789012345",  # 25 цифр
    ],
)
def test_get_mask_account_invalid_length(account_number: str) -> None:
    """Номер счёта неверной длины вызывает ValueError."""
    with pytest.raises(
        ValueError,
        match="Номер счета должен содержать 20 цифр и никаких других символов",
    ):
        get_mask_account(account_number)


# Тест 105: Проверка, что функция корректно обрабатывает входные строки, где отсутствует номер счета.


def test_get_mask_account_invalid_input() -> None:
    """Передача None вызывает ValueError или TypeError."""
    account_number = None
    with pytest.raises((ValueError, TypeError)):
        get_mask_account(account_number)  # type: ignore[arg-type]


# Тест 106: Проверка номера счета c повторяющейся цифрой, например "00000000000000000000" (залипание клавиши).


@pytest.mark.parametrize(
    "account_number",
    [
        "00000000000000000000",  # 20 нулей
        "11111111111111111111",  # 20 единиц
    ],
)
def test_get_mask_account_repeating_digits(account_number: str) -> None:
    """Номер счёта из одинаковых цифр («залипание клавиши») вызывает ValueError."""
    with pytest.raises(ValueError):
        get_mask_account(account_number)
