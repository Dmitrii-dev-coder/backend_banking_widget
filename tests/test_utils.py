# Проверка функции get_transactions_from_file.
from unittest.mock import mock_open, patch

from src.utils import get_transactions_from_json_file


# Тест 001: Позитивный сценарий, когда файл существует.
def test_get_transactions_from_file_positive() -> None:
    """Передает существующий путь и проверяет что вернулся список словарей."""
    result = get_transactions_from_json_file("data/operations.json")
    assert isinstance(result, list)  # Проверяет, что результат является списком.
    assert len(result) > 0  # Проверяет, что список не пустой.
    assert isinstance(result[0], dict)  # Проверяет, что элементы списка являются словарями.

    assert result[0]["id"] == 441945886  # Проверяет первый элемент списка, что id равен 44194
    assert result[0]["state"] == "EXECUTED"  # Проверяет, что статус первого элемента списка равен "EXECUTED"


# Тест 002: Проверка, что при не существующем пути возвращается пустой список.
def test_get_transactions_from_file_invalid_path() -> None:
    """Передает не существующий путь к файлу и проверяет, что возвращается пустой список."""
    result = get_transactions_from_json_file("data/transactions.json")
    assert result == []


# Тест 003: Проверка функции, что при передаче ей пустого файла она возвращает пустой список.
def test_get_transactions_from_file_empty() -> None:
    """Передаете пустой файл и получаете пустой список."""
    with patch("builtins.open", mock_open(read_data="")):
        result = get_transactions_from_json_file("data/fake.json")
        assert result == []


# Тест 004: Проверка на файл с не валидным JSON.
def test_get_transactions_from_file_invalid_json() -> None:
    """Тест на чтение файла с невалидным JSON."""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        result = get_transactions_from_json_file("data/fake.json")
        assert result == []


# Тест 005: Проверка, что функция, принимая JSON-файл в котором валидный JSON, но не список а например -
# {"key": "value"}, возвращает пустой список.
def test_get_transactions_from_file_not_list() -> None:
    """Тест на чтение файла с валидным JSON но не списком."""
    with patch("builtins.open", mock_open(read_data='{"key": "value"}')):
        result = get_transactions_from_json_file("data/fake.json")
        assert result == []
