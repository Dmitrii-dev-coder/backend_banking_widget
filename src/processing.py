from datetime import datetime

def filter_by_state(my_list_dict: list, state: str = "EXECUTED") -> list:
    """Функция filter_by_state, которая принимает список словарей и опционально значение для ключа state (по умолчанию
    'EXECUTED'). Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state
    соответствует указанному значению."""

    # Проверка на пустой список.
    if not my_list_dict:
        raise ValueError("Входной список не должен быть пустым.")

    # Проверка наличия пары "state" : "значение ("EXECUTED" или "CANCELED")".
    for person in my_list_dict:
        if "state" not in person:
            return []

    filtered_list = []
    for dict_ in my_list_dict:
        if dict_["state"] == state:
            filtered_list.append(dict_)

    return filtered_list


def sort_by_date(my_list_dir: list, descending: bool = True) -> list:
    """Функция sort_by_date, которая принимает список словарей и необязательный параметр, задающий
    порядок сортировки (по умолчанию — убывание). Функция должна возвращать новый список, отсортированный по
    дате (date)."""

    error_text = (
        "Функция обрабатывает данные только в международном стандарте времени ISO 8601, "
        "возможно вы ввели не верную дату, с несуществующим месяцем, или днем, "
        "а так же время указанно не верно, не принимаются не существующие часы, минуты или секунды"
    )

    # Проверяем каждый элемент: если дата не соответствует ISO 8601 или невалидна — выбрасываем исключение.
    for item in my_list_dir:
        date_str = item["date"]
        try:
            datetime.fromisoformat(date_str)
        except (ValueError, TypeError):
            raise ValueError(error_text)

    # После успешной проверки выполняем сортировку по преобразованной дате.
    sorted_list = sorted(
        my_list_dir,
        key=lambda emp: datetime.fromisoformat(emp["date"]),
        reverse=descending
    )
    return sorted_list
