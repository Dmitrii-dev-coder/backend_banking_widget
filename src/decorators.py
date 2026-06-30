from datetime import datetime


def log(filename=None):
    """
    Принимает функцию и опционально имя файла для логирования работы функции.

    Возвращает обёртку над функцией.
    Обертка записывает в файл логи о работе функции.

    Если filename не указан, логи выводятся в консоль.

    Логирование должно включать:
      - Имя функции и результат выполнения при успешной операции. А так же время запуска/завершения.
      - Имя функции, тип возникшей ошибки и входные параметры, если выполнение функции привело к ошибке.

    Обработка ошибок:
      * Функция перехватывает исключения TypeError в случае невалидных аргументов.
      * Перехватывает все возможные исключения логируя их тип;
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                start_time = datetime.now().strftime("%H:%M:%S.%f")
                print(f"Запуск {func.__name__} в {start_time}")
                # Проверка валидности аргументов, что это числа, а не строки.
                for arg in args:
                    if not isinstance(arg, (int, float)):
                        raise TypeError(
                            f"Аргумент {arg} должен быть числом (int или float), получено {type(arg).__name__}"
                        )
                for kwarg in kwargs.values():
                    if not isinstance(kwarg, (int, float)):
                        raise TypeError(
                            f"Аргумент {kwarg} должен быть числом (int или float), получено {type(kwarg).__name__}"
                        )

                result = func(*args, **kwargs)
                end_time = datetime.now().strftime("%H:%M:%S.%f")
                if filename is None:
                    print(f"Завершение {func.__name__} c результатом: {result} в {end_time}.")
                else:
                    with open(filename, "a", encoding="utf-8") as fh:
                        fh.write(f"Завершение {func.__name__} c результатом: {result} в {end_time}.\n")
                return result
            except Exception as e:
                end_time = datetime.now().strftime("%H:%M:%S")
                error_type = type(e).__name__
                if filename is None:
                    print(f"Завершение {func.__name__} error: {error_type}. Inputs: {args}, {kwargs}.")
                else:
                    with open(filename, "a", encoding="utf-8") as fh:
                        fh.write(f"Завершение {func.__name__} error: {error_type}. Inputs: {args}, {kwargs}.\n")
                raise

        return wrapper

    return decorator
