import re
import typing
from datetime import datetime


def check_phone(phone:str):
    if isinstance(phone, str):
        pattern = re.compile("^[0-9]{10}$")
        result = bool(re.match(pattern=pattern, string=phone))
    else:
        result = False
    return result


def check_birthday(birthday:str):
    if isinstance(birthday, str):
        pattern = re.compile("^(19|20)[0-9]{2}-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1])$")
        result = bool(re.match(pattern=pattern, string=birthday))
    else:
        result = False
    if result:
        year, month, day = birthday.split("-")
        if int(month) == 2:
            result = int(day) <= 29 if int(year) % 4 == 0 else 28
        elif int(month) in [4, 6, 9, 11]:
            result = int(day) <= 30
    if result:
        result = int(year) <= datetime.now().year
    return result
