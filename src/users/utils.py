import re

from django.utils import timezone


def calculate_age(born):
    today = timezone.now()
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


def count_age_customer(birthday):
    now = timezone.now()
    if birthday.month == now.month:
        if birthday.day <= now.day:
            return now.year - birthday.year
        else:
            return now.year - birthday.year - 1
    elif birthday.month > now.month:
        return now.year - birthday.year - 1
    else:
        return now.year - birthday.year
