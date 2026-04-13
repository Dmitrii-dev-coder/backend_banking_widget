def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты и возвращает его замаскированным."""

    # Превращаем номер карты в строку, если пришло число
    card_number_str = str(card_number)

    # Вставление пробела после каждых четыре знака
    card_mask = card_number_str[0:4] + " " + card_number_str[4:6] + "**" + " " + "****" + " " + card_number_str[12:16]

    return card_mask


def get_mask_account(account_number: str) -> str:
    """Функция принимает на вход номер счета и возвращает его замаскированным."""

    # Превращаем номер счета в строку, если пришло число
    account_number_str = str(account_number)

    # Берем последние 4 цифры и добавляем две звездочки перед ними
    account_mask = f"**{account_number_str[-4:]}"

    return account_mask
