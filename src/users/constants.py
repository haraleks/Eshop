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