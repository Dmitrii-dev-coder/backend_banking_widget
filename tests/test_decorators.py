from src.decorators import log
import os

# 0. Проверка функции декоратора log.
# Тест 001: Проверяет, что функция корректно записывает логи в файл если указано имя файла.
def test_log():
    @log(filename="test_log.txt")
    def my_function(x, y):
        return x + y

    result = my_function(1, 2)
    assert result == 3

    result_2 = my_function(-1, -2)
    assert result_2 == -3

    # Проверяем, что файл создан и содержит оба результата
    with open("test_log.txt", "r", encoding="utf-8") as f:
        content = f.read()
        assert "Завершение my_function c результатом: 3 в" in content
        assert "Завершение my_function c результатом: -3 в" in content

    # Удаляем файл после теста
    os.remove("test_log.txt")

# Тест 002: Проверяет вывод логов в консоль при отсутствии имени файла.
def test_log_to_console(capsys):
    """Проверяет вывод логов в консоль, когда filename не указан"""
    @log()  # Нет filename - логи идут в консоль
    def my_function(x, y):
        return x + y

    result = my_function(5, 3)
    assert result == 8

    # Перехватываем вывод консоли
    captured = capsys.readouterr()
    
    # Проверяем, что в консоли есть логи
    assert "Запуск my_function" in captured.out
    assert "Завершение my_function c результатом: 8 в" in captured.out
    # Проверяем формат времени HH:MM:SS.ffffff (микросекунды)
    import re
    time_pattern = r'\d{2}:\d{2}:\d{2}\.\d{6}'
    assert re.search(time_pattern, captured.out) is not None

# Тест 003: Проверяет, что декоратор корректно: обрабатывает неправильные типы данных переданных в функцию;
# и логирует их.
def test_log_with_exception():
    """Проверяет, что декоратор логирует исключения при передаче неверных типов аргументов"""
    @log(filename="test_error.txt")
    def my_function(x, y):
        return x + y

    # Проверяем, что TypeError возникает при передаче строки
    try:
        my_function("abc", 5)
        assert False, "Должна быть ошибка TypeError"
    except TypeError as e:
        assert "Аргумент abc должен быть числом" in str(e)

    # Проверяем, что файл создан с логом ошибки
    with open("test_error.txt", "r", encoding="utf-8") as f:
        content = f.read()
        assert "Завершение my_function error: TypeError" in content
        assert "Inputs: ('abc', 5)" in content

    # Удаляем файл после теста
    os.remove("test_error.txt")

# Тест 004: Проверяет правильность логирования декоратором в случае ошибки если не указано имя файла.
def test_log_with_exception_console(capsys):
    """Проверяет, что декоратор логирует исключения в консоль при отсутствии filename"""
    @log()  # Нет filename - логи идут в консоль
    def my_function(x, y):
        return x + y

    # Проверяем, что TypeError возникает при передаче строки
    try:
        my_function("abc", 5)
        assert False, "Должна быть ошибка TypeError"
    except TypeError as e:
        assert "Аргумент abc должен быть числом" in str(e)

    # Перехватываем вывод консоли
    captured = capsys.readouterr()
    
    # Проверяем, что в консоли есть лог об ошибке
    assert "Завершение my_function error: TypeError" in captured.out
    assert "Inputs: ('abc', 5)" in captured.out

# Тест 005: Проверяет, что декоратор корректно обрабатывает неправильные типы данных в именованных аргументах (kwargs).
def test_log_with_exception_kwargs():
    """Проверяет, что декоратор логирует исключения при передаче неверных типов в именованных аргументах"""
    @log(filename="test_kwargs_error.txt")
    def my_function(x, y=None):
        return x + y

    # Проверяем, что TypeError возникает при передаче строки в kwargs
    try:
        my_function(5, y="abc")
        assert False, "Должна быть ошибка TypeError"
    except TypeError as e:
        assert "Аргумент abc должен быть числом" in str(e)

    # Проверяем, что файл создан с логом ошибки
    with open("test_kwargs_error.txt", "r", encoding="utf-8") as f:
        content = f.read()
        assert "Завершение my_function error: TypeError" in content
        assert "Inputs: (5,), {'y': 'abc'}" in content

    # Удаляем файл после теста
    os.remove("test_kwargs_error.txt")
