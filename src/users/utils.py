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
