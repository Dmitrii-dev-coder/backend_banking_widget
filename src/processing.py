def filter_by_state(my_list_dict: list, state='EXECUTED') -> list:
    """Функция filter_by_state, которая принимает список словарей и опционально значение для ключа state (по умолчанию
    'EXECUTED'). Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state
    соответствует указанному значению."""

    filtered_list = []
    for dict_ in my_list_dict:
        if dict_['state'] == state:
            filtered_list.append(dict_)

    return filtered_list


def sort_by_date(my_list_dir: list) -> list:
    """Функция sort_by_date, которая принимает список словарей и необязательный параметр, задающий
    порядок сортировки (по умолчанию — убывание). Функция должна возвращать новый список, отсортированный по
    дате (date)."""
    sorted_list = sorted(my_list_dir, key=lambda employee: employee['date'], reverse=True)

    return sorted_list


if __name__ == '__main__':
    print(filter_by_state(
        [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}],
        'CANCELED'
    ))

    print(sort_by_date(
        [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
    ))