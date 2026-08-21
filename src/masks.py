from src.logger import setup_logger

logger = setup_logger('masks', 'logs/masks.log')

def get_mask_card_number(card_number: str | int) -> str:
    """Функция принимает на вход номер карты и возвращает его замаскированным."""
    logger.debug("Функция генерации маски запущена")

    # Превращаем номер карты в строку, если пришло число
    card_number_str = str(card_number)

    # Удаляем пробелы и дефисы если они есть.
    card_number_str = card_number_str.replace(" ", '').replace("-", "")

    # Проверяем что номер карты содержит только цифры
    if not card_number_str.isdigit():
        logger.error(f"Номер карты содержит не только цифры: {card_number_str}")
        raise ValueError("Номер карты должен содержать 16 цифр и никаких других символов")

    # Проверяем длину номера карты
    elif len(card_number_str) != 16:
        logger.error(f"Не совпадает количество цифр в номере карты. Проверьте, пожалуйста, ввод: {card_number_str}")
        raise ValueError("Номер карты должен содержать 16 цифр и никаких других символов")


    # Проверяем на эффект залипания клавиши
    elif len(set(card_number_str)) == 1:
        logger.error("Номер карты содержит только одинаковые цифры (эффект залипания клавиши)")
        raise ValueError("Номер карты содержит только одинаковые цифры (эффект залипания клавиши).")


    # Вставление пробела после каждых четыре знака
    card_mask = f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[12:]}"
    logger.debug(f"Маска карты успешно сгенерирована: {card_mask}")
    logger.debug("Функция генерации маски карты завершена")

    return card_mask


def get_mask_account(account_number: str | int) -> str:
    """Функция принимает на вход номер счета и возвращает его замаскированным."""

    # Превращаем номер счета в строку, если пришло число
    account_number_str = str(account_number)

    # Проверяем что номер счета содержит только цифры
    if not account_number_str.isdigit():
        raise ValueError("Номер счета должен содержать 20 цифр и никаких других символов")

    # Проверяем длину номера счета
    if len(account_number_str) != 20:
        raise ValueError("Номер счета должен содержать 20 цифр и никаких других символов")

    # Проверяем на эффект залипания клавиши
    if len(set(account_number_str)) == 1:
        raise ValueError("Номер карты содержит только одинаковые цифры (эффект залипания клавиши).")

    # Берем последние 4 цифры и добавляем две звездочки перед ними
    account_mask = f"**{account_number_str[-4:]}"

    return account_mask
