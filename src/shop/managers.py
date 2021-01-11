import random

from django.db import models
from django.db.models import Q


class ProductManager(models.Manager):
    def random(self, sex=None, subcategory=None, exclude_id=None, age=None):
        instance = list(self.filter(
            Q(age_to__gte=age) & Q(age_from__lte=age),
            sex=sex, subcategory=subcategory).exclude(pk=exclude_id))
        random.shuffle(instance)
        return instance
