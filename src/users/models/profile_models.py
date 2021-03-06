from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.constants import SexTypes
from users.utils import calculate_age

User = get_user_model()


class Customer(models.Model):
    user = models.OneToOneField(
        User, related_name='customer_profile', on_delete=models.CASCADE)
    first_name = models.CharField(_('First name'), max_length=155)
    last_name = models.CharField(_('Last name'), max_length=155, blank=True, default='')
    sex = models.CharField(
        _('Sex'),
        max_length=1,
        choices=SexTypes.CHOISES(),
        blank=True,
        default=SexTypes.MALE.value
    )
    date_of_birth = models.DateField(_('Date of birth'), null=True, blank=True)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    is_active = models.BooleanField(_('is_active'), default=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def age(self):
        return calculate_age(self.date_of_birth)

    @property
    def count_product_desired(self):
        return self.wish_lists.all().count()

    def __str__(self):
        return str(self.full_name)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()
        self.user.delete()

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        default_permissions = []
