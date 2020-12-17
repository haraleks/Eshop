import re
from datetime import datetime


def calculate_age(born):
    today = datetime.today()
    try:
        birthday = born.replace(year=today.year)
    except ValueError:
        birthday = born.replace(year=today.year, month=born.month+1, day=1)
    if birthday.date() > today.date():
        return today.year - born.year - 1
    else:
        return today.year - born.year


def vaildation_password(data):
    errors_dct = {}
    if len(data) < 8:
        errors_dct['length:'] = ['length < 8 symbol']
    if not re.search(r'[a-z]', data):
        errors_dct['lowercase:'] = ['not lowercase']
    if not re.search(r'[A-Z]', data):
        errors_dct['uppercase:'] = ['not upercase']
    if not re.search(r'\d', data):
        errors_dct['numeric:'] = ['not numeric']
    if not re.search(r'[&$#]', data):
        errors_dct['symbols:'] = ['not symbol: (&,$,#)']
    return errors_dct
