# Проверка функции get_transactions_from_file.
from unittest.mock import Mock
from src.utils import get_transactions_from_file


# Тест 001: Позитивный сценарий, когда файл существует.
def test_get_transactions_from_file_positive():
    """Передает существующий путь и проверяет что вернулся список словарей."""
    result = get_transactions_from_file("data/operations.json")
    assert isinstance(result, list)  # Проверяет, что результат является списком.
    assert len(result) > 0  # Проверяет, что список не пустой.
    assert isinstance(result[0], dict)  # Проверяет, что элементы списка являются словарями.

    assert result[0]["id"] == 441945886  # Проверяет первый элемент списка, что id равен 44194
    assert result[0]["state"] == "EXECUTED"  # Проверяет, что статус первого элемента списка равен "EXECUTED"

# Тест 002: Проверка, что при не существующем пути возвращается пустой список.
def test_get_transactions_from_file_invalid_path():
    """ """
    result = get_transactions_from_file("data/transactions.json")
    assert result == []

# Тест 003: Проверка функции, что при передаче ей пустого файла она возвращает пустой список.
def test_get_transactions_from_file_empty():
    """ """
    mock_file = Mock(return_value="[]")  # Пустой файл, содержит"[]"
    assert get_transactions_from_file(mock_file) == []



