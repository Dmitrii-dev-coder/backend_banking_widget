from datetime import datetime
import re

from masks import get_mask_card_number, get_mask_account

def mask_account_card(account_card: str) -> str:
    """Маскирует полученный номер карты или счета"""

    if "Счет" in account_card:
        letters_part = "".join(re.findall(r"\D+", account_card))
        numbers_part = "".join(re.findall(r"\d+", account_card))
        hidden_account_card = f"{letters_part} {get_mask_account(numbers_part)}"
    else:
        letters_part = "".join(re.findall(r"\D+", account_card))
        numbers_part = "".join(re.findall(r"\d+", account_card))
        hidden_account_card = f"{letters_part} {get_mask_card_number(numbers_part)}"

    return hidden_account_card


def get_date(date_iso_8601: str) -> str:
    """Конвертирует дату в необходимый формат 'ДД.ММ.ГГГГ'"""

    #formatted_date = 'f"{unformatted_date[8:10]}.{unformatted_date[5:7]}.{unformatted_date[:4]}"'
    formatted_date = datetime.strptime(date_iso_8601, "%Y-%m-%dT%H:%M:%S.%f")
    return formatted_date.strftime("%d.%m.%Y")


if __name__ == '__main__':
    print(mask_account_card("Visa Platinum 7000792289606361"))  # Visa Platinum 7000 79** **** 6361

    print(get_date("2024-03-11T02:26:18.671407"))  # "11.03.2024"