import pytest

from processing import filter_by_state, sort_by_date


# 0. Проверка функции filter_by_state.
# Тест 001: Тестирование правильности фильтрации списка словарей по заданному статусу 'state'.

@pytest.fixture
def delivery_valid_data():
    my_list_dict = [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ]

    return my_list_dict

@pytest.fixture
def delivery_invalid_data():
    my_list_dict = [
                {"id": 41428829, "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "date": "2018-10-14T08:21:33.419441"},
            ]

    return my_list_dict

def test_filter_by_state_valid_data(delivery_valid_data):
    assert filter_by_state(delivery_valid_data, "CANCELED") == [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"}]

# Тест 002: Проверка работы функции без передачи аргумента параметру 'state'.

    # Проверка на то, что функция использует значение state по умолчанию.

def test_filter_by_state_valid_data_default_state(delivery_valid_data):
    assert filter_by_state(delivery_valid_data) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}]

# Тест 003: Проверка работы функции если входные данные это пустой список.
def test_filter_by_state_empty_list():
    my_list_dict = []
    with pytest.raises(ValueError):
        filter_by_state(my_list_dict)

# Тест 004: Проверка того, что функция возвращает пустой список если во входных данных отcутствет "state".
def test_filter_by_state_without_state(delivery_invalid_data):
    assert filter_by_state(delivery_invalid_data) == []

# Тест 005: Проверка того, что функция правильно фильтрует списки для каждого из различных значений "state".
@pytest.mark.parametrize("my_list_dict, state, expected", [
    (
        [
            {"id": 41428829, "state": "active", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "inactive", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 327553912, "state": "pending", "date": "2020-01-14T08:10:41.527639"}
        ],
        "active",
        [{"id": 41428829, "state": "active", "date": "2019-07-03T18:35:29.512364"}]
    ),
    (
        [
            {"id": 41428829, "state": "active", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "inactive", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 327553912, "state": "pending", "date": "2020-01-14T08:10:41.527639"}
        ],
        "inactive",
        [{"id": 594226727, "state": "inactive", "date": "2018-09-12T21:27:25.241689"}]
    ),
    (
        [
            {"id": 41428829, "state": "active", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "inactive", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 327553912, "state": "pending", "date": "2020-01-14T08:10:41.527639"}
        ],
        "pending",
        [{"id": 327553912, "state": "pending", "date": "2020-01-14T08:10:41.527639"}]
    ),
])
def test_filter_by_state_diff_state(my_list_dict, state, expected):
    assert filter_by_state(my_list_dict, state) == expected

# 1. Проверка функции sort_by_date.
# Тест 101: Тестирование правильности сортировки списка словарей по датам в порядке убывания.
def test_sort_by_date_valid_data_descending(delivery_valid_data):
    assert sort_by_date(delivery_valid_data) == [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]

# Тест 102: Тестирование правильности сортировки списка словарей по датам в порядке возрастания.
def test_sort_by_date_valid_data_ascending(delivery_valid_data):
    assert sort_by_date(delivery_valid_data, False) == [
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}]


# Тест 103: Проверка корректности сортировки при одинаковых датах.
def test_sort_by_date_same_date():
    my_list_dict = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2019-07-03T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2019-07-03T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2019-07-03T08:21:33.419441"},
    ]
    assert sort_by_date(my_list_dict) == [
        {"id": 594226727, "state": "CANCELED", "date": "2019-07-03T21:27:25.241689"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2019-07-03T08:21:33.419441"},
        {"id": 939719570, "state": "EXECUTED", "date": "2019-07-03T02:08:58.425572"}]


# Тест 104: Проверка работы функции с некорректными или нестандартными форматами дат.
def test_sort_by_date_invalid_data():
    error_text = (
        "Функция обрабатывает данные только в международном стандарте времени ISO 8601, "
        "возможно вы ввели не верную дату, с несуществующим месяцем, или днем, "
        "а так же время указанно не верно, не принимаются не существующие часы, минуты или секунды"
    )
    my_list_dict = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30"},  # Некорректный формат
        {"id": 594226727, "state": "CANCELED", "date": "12-09-2018T21:27:25"},  # Нестандартный формат
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 615064592, "state": "CANCELED", "date": "2018-02-30T08:21:33"},  # Нереальная дата
    ]
    with pytest.raises(ValueError) as exc_info:
        sort_by_date(my_list_dict)