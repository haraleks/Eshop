from django.contrib.auth.models import (PermissionsMixin, BaseUserManager, AbstractBaseUser)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a users with the given email, and password.
        """
        if not email:
            raise ValueError(_('The given email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('E-mail', blank=False, unique=True)
    is_active = models.BooleanField(default=True, blank=True)
    deleted_at = models.DateTimeField(_('Date deleted'), null=True, default=None, blank=True)
    is_staff = models.BooleanField(_('Admin'), default=False)
    is_superuser = models.BooleanField(_('Super Admin'), default=False)
    date_joined = models.DateTimeField(_('Created'), default=timezone.now, blank=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        permissions = []
        default_permissions = []
        verbose_name = _('users')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return f'{self.email}'


class User(AbstractUser):
    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        permissions = [
            ('change_user_accounts', _('Change users account')),
        ]
