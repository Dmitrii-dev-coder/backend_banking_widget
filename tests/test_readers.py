import pandas as pd
from pathlib import Path

from unittest.mock import patch, mock_open

from src.readers import get_transactions_from_csv_file, get_transactions_from_excel_file

# Путь к папке с данными (на два уровня выше текущей папки tests)
test_data_dir = Path(__file__).parent.parent / "data"


# 0. Проверка функции get_transactions_from_csv_file.
# Тест 001: Позитивный сценарий, когда файл существует.
def test_get_transactions_from_csv_file_positive() -> None:
    """Передает существующий путь и проверяет что вернулся список словарей."""
    file_path = test_data_dir / "transactions.csv"

    result = get_transactions_from_csv_file(str(file_path))

    assert isinstance(result, list)  # Проверяет, что результат является списком.
    assert len(result) > 0  # Проверяет, что список не пустой.
    assert isinstance(result[0], dict)  # Проверяет, что элементы списка являются словарями.

    assert result[0]["id"] == 650703  # Проверяет первый элемент списка, что id равен 650703
    assert result[0]["state"] == "EXECUTED"  # Проверяет, что статус первого элемента списка равен "EXECUTED"


# Тест 002: Проверка, что при не существующем пути возвращается пустой список.
def test_get_transactions_from_csv_file_negative() -> None:
    """Передает несуществующий путь и проверяет, что вернулся пустой список."""
    result = get_transactions_from_csv_file(str(test_data_dir / "operations.csv"))
    assert result == []


# Тест 003: Проверка функции, что при передаче ей пустого файла она возвращает пустой список.
def test_get_transactions_from_csv_file_empty() -> None:
    """Передает пустой файл и проверяет, что возвращается пустой список."""
    with patch("builtins.open", mock_open(read_data="")):
        result = get_transactions_from_csv_file(str(test_data_dir / "empty.csv"))
        assert result == []


# Тест 004: Проверка функции на CSV-файл с не валидным данными (например, если столбцы неправильно именованы).
def test_get_transactions_from_csv_file_invalid() -> None:
    """Передает файл с невалидной структурой и проверяет, что возвращается пустой список."""
    with patch("builtins.open", mock_open(read_data="id;state\ndata1\ndata2;data2;лишнее")):
        result = get_transactions_from_csv_file(str(test_data_dir / "invalid.csv"))
        assert result == []


# Тест 005: Проверка функции на обработку пустых ячеек (NaN).
@patch("builtins.open", mock_open(read_data="id;state;amount\n1;EXECUTED;\n2;CANCELED;100"))
def test_get_transactions_from_csv_file_with_nan() -> None:
    """Передает CSV с пустой ячейкой и проверяет корректную обработку данных."""
    result = get_transactions_from_csv_file(str(test_data_dir / "csv_with_nan.csv"))

    assert isinstance(result, list)
    assert len(result) == 2

    # Проверяем, что пустое поле не вызвало ошибку и было корректно обработано
    assert result[0]["amount"] is None or pd.isna(result[0]["amount"])


# Тест 006: Проверка функции, что она возвращает корректные данные (Например, проверь, что id транзакции и сумма совпадают).
def test_get_transactions_from_csv_file_verify_amount() -> None:
    """Проверяет, что данные загружены корректно (например, сумма)."""
    file_path = test_data_dir / "transactions.csv"
    result = get_transactions_from_csv_file(str(file_path))

    assert isinstance(result, list)
    assert len(result) > 0

    # Проверяем сумму (так как id уже проверяли в тесте 001)
    assert result[0]["amount"] == 16210.0
    assert result[0]["currency_name"] == "Sol"


# 1. Проверка функции get_transactions_from_excel_file.
# Тест 101: Позитивный сценарий, когда файл существует.
def test_get_transactions_from_excel_file_positive() -> None:
    """Передает существующий путь и проверяет что вернулся список словарей."""
    file_path = test_data_dir / "transactions_excel.xlsx"

    result = get_transactions_from_excel_file(str(file_path))

    assert isinstance(result, list)  # Проверяет, что результат является списком.
    assert len(result) > 0  # Проверяет, что список не пустой.
    assert isinstance(result[0], dict)  # Проверяет, что элементы списка являются словарями.

    assert result[0]["id"] == 650703.0  # Проверяет первый элемент списка, что id равен 650703.0
    assert result[0]["state"] == "EXECUTED"  # Проверяет, что статус первого элемента списка равен "EXECUTED"


# Тест 102: Проверка, что при не существующем пути возвращается пустой список.
def test_get_transactions_from_excel_file_negative() -> None:
    """Передает несуществующий путь и проверяет, что вернулся пустой список."""
    result = get_transactions_from_excel_file(str(test_data_dir / "operations_excel.xlsx"))
    assert result == []


# Тест 103: Проверка функции, что при передаче ей пустого файла она возвращает пустой список.
def test_get_transactions_from_excel_file_empty() -> None:
    """Передает пустой файл и проверяет, что возвращается пустой список."""
    with patch("builtins.open", mock_open(read_data="")):
        result = get_transactions_from_excel_file(str(test_data_dir / "empty.xlsx"))
        assert result == []


# Тест 104: Проверка функции на excel-файл с не валидным данными (данные в строке неполные, в ячейке NaN).
@patch("src.readers.pd.read_excel")
def test_get_transactions_from_excel_file_with_nan(mock_read_excel) -> None:
    """Передает Excel с пустыми ячейками и проверяет обработку."""
    # 1. Создаем DataFrame с пустой ячейкой (float('nan'))
    df_with_nan = pd.DataFrame({"id": [1.0, float("nan")], "state": ["EXECUTED", "CANCELED"]})  # Вторая строка пустая

    # 2. Говорим библиотеке pandas, что именно этот DataFrame вернет функция read_excel
    mock_read_excel.return_value = df_with_nan

    # 3. Вызываем тестируемую функцию
    result = get_transactions_from_excel_file("data/fake.xlsx")

    # 4. Проверяем результат
    assert isinstance(result, list)
    assert len(result) > 0
    # Проверяем, что NaN преобразовался в None (если это настроено в коде)
    assert pd.isna(result[1]["id"]) or result[1]["id"] is None


# Тест 105: Проверка функции на excel-файл с неправильно именованными столбцами.
@patch("src.readers.pd.read_excel")
def test_get_transactions_from_excel_file_wrong_columns(mock_read_excel) -> None:
    """Передает Excel с невалидными именами столбцов и проверяет обработку."""
    # Создаем DataFrame с совершенно другими именами столбцов
    df_wrong = pd.DataFrame({"weird_col_1": [1, 2], "weird_col_2": ["Data", "Data"]})

    # Говорим библиотеке pandas, что именно этот DataFrame вернет функция read_excel
    mock_read_excel.return_value = df_wrong

    # Вызываем тестируемую функцию
    result = get_transactions_from_excel_file(str(test_data_dir / "wrong.xlsx"))

    # Проверяем, что она не упала и вернула словари с "крякозябрами" вместо ключей
    assert isinstance(result, list)
    assert len(result) > 0
    assert "weird_col_1" in result[0]
    assert "id" not in result[0]


# Тест 106: Проверка функции, что она возвращает корректные данные (Например, проверь, что id транзакции и сумма совпадают).
@patch("src.readers.pd.read_excel")
def test_get_transactions_from_excel_file_verify_data(mock_read_excel) -> None:
    """Передает Excel с корректными данными и проверяет, что id и amount совпадают."""
    # 1. Создаем DataFrame с корректными данными
    df_correct = pd.DataFrame({"id": [100, 200], "state": ["EXECUTED", "CANCELED"], "amount": [5000.0, 15000.0]})

    # 2. Настраиваем mock так, чтобы он возвращал наш DataFrame
    mock_read_excel.return_value = df_correct

    # 3. Вызываем тестируемую функцию
    result = get_transactions_from_excel_file(str(test_data_dir / "correct.xlsx"))

    # 4. Проверяем, что вернулся список словарей
    assert isinstance(result, list)
    assert len(result) == 2

    # 5. Проверяем конкретные значения (id и amount)
    assert result[0]["id"] == 100
    assert result[0]["amount"] == 5000.0
    assert result[1]["id"] == 200
    assert result[1]["amount"] == 15000.0


# Тест 107: Проверка функции, что при отсутствии данных в Excel-файле (пустая структура) она возвращает пустой список.
@patch("src.readers.pd.read_excel")
def test_get_transactions_from_excel_file_empty_data(mock_read_excel) -> None:
    """Симулирует ошибку pd.errors.EmptyDataError и проверяет, что возвращается пустой список."""
    mock_read_excel.side_effect = pd.errors.EmptyDataError("Excel file is empty")
    result = get_transactions_from_excel_file(str(test_data_dir / "empty_data.xlsx"))
    assert result == []
