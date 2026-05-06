def filter_by_state(my_list_dict: list, state: str = "EXECUTED") -> list:
    """Функция filter_by_state, которая принимает список словарей и опционально значение для ключа state (по умолчанию
    'EXECUTED'). Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state
    соответствует указанному значению."""

    filtered_list = []
    for dict_ in my_list_dict:
        if dict_["state"] == state:
            filtered_list.append(dict_)

    return filtered_list


def sort_by_date(my_list_dir: list, descending: bool = True) -> list:
    """Функция sort_by_date, которая принимает список словарей и необязательный параметр, задающий
    порядок сортировки (по умолчанию — убывание). Функция должна возвращать новый список, отсортированный по
    дате (date)."""
    sorted_list = sorted(my_list_dir, key=lambda employee: employee["date"], reverse=descending)

    return sorted_list
