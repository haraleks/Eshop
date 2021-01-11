from enum import Enum

from django.utils.translation import ugettext_lazy as _


class SexTypes(Enum):
    MALE = 'M'
    FEMALE = 'F'

    @classmethod
    def CHOISES(cls):
        return (
            (cls.MALE.value, _('Male')),
            (cls.FEMALE.value, _('Female')),
        )


class TypeValue(Enum):
    CHAR = 'char'
    INT = 'int'
    FLOAT = 'float'
    BOOL = 'bool'
    TXT = 'txt'
    DATE = 'date'
    DATETIME = 'datetime'

    @classmethod
    def CHOISES(cls):
        return (
            (cls.CHAR.value, _('Char max length 300')),
            (cls.INT.value, _('Integer')),
            (cls.FLOAT.value, _('Float')),
            (cls.BOOL.value, _('Bool')),
            (cls.TXT.value, _('Text')),
            (cls.DATE.value, _('Date')),
            (cls.DATETIME.value, _('Date & time')),
        )


class Status(Enum):
    CREATED = 'created'
    PAID = 'paid'
    CANCELED = 'canceled'

    @classmethod
    def CHOISES(cls):
        return (
            (cls.CREATED.value, _('Created')),
            (cls.PAID.value, _('Paid')),
            (cls.CANCELED.value, _('Canceled')),
        )


class SexProduct(Enum):
    MALE = 'M'
    FEMALE = 'F'
    UNISEX = 'U'

    @classmethod
    def CHOISES(cls):
        return (
            (cls.MALE.value, _('Male')),
            (cls.FEMALE.value, _('Female')),
            (cls.UNISEX.value, _('Unisex')),
        )
