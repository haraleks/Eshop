import calendar
from datetime import timedelta

from django.utils import timezone


def discount_birthday(birthday, discount=15):
    now = timezone.now()
    date_10_ago = now - timedelta(days=10)
    date_10_next = now + timedelta(days=10)
    date_first = date_10_next.replace(day=1)
    date_last = date_10_ago.replace(day=calendar.monthrange(date_10_ago.year, date_10_ago.month)[1])

    if date_10_ago.month == date_10_next.month:
        if date_10_ago.day <= birthday.day <= date_10_next.day:
            return discount
        return 0
    elif birthday.month == date_10_ago.month:
        if date_10_ago.day <= birthday.day <= date_last.day:
            return discount
        return 0
    elif birthday.month == date_10_next.month:
        if date_first.day <= birthday.day <= date_10_next.day:
            return discount
        return 0
    return 0
