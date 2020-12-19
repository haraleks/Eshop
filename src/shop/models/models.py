from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from users.constants import TypeValue, Status
from users.models.profile_models import Customer


class AbstarctModels(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(_('Date created'), auto_now_add=True)

    class Meta:
        permissions = []
        abstract = True


class Category(AbstarctModels):

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        permissions = []

    def __str__(self):
        return self.name


class Subcategory(AbstarctModels):
    category = models.ForeignKey(
        Category, blank=True,
        on_delete=models.CASCADE,
        default=None,
        related_name='subcategory')

    class Meta:
        verbose_name = _('Subcategory')
        verbose_name_plural = _('Subcategories')
        permissions = []

    def __str__(self):
        return f'{self.category.name} - {self.name}'


class Product(AbstarctModels):
    """
    Price -  в копейках
    """
    price = models.IntegerField(_('Price'), default=0)
    sku = models.CharField(_('SKU'), max_length=50, blank=True, default='')
    description = models.TextField(_('Description product'), blank=True)
    subcategory = models.ForeignKey(
        Subcategory, blank=True,
        on_delete=models.CASCADE,
        default=None,
        related_name='product')
    is_active = models.BooleanField(_("Is active"), default=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        permissions = []


class Attribute(AbstarctModels):
    type = models.CharField(choices=TypeValue.CHOISES(), max_length=8,
                            default=TypeValue.CHAR)

    class Meta:
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attribute')
        permissions = []

    def __str__(self):
        return f'{self.name} : {self.type}'


class Value(models.Model):
    product = models.ForeignKey(
        Product, blank=True,
        on_delete=models.CASCADE,
        default=None,
        related_name='value')
    attribute = models.ForeignKey(
        Attribute, blank=True,
        on_delete=models.CASCADE,
        default=None,
        related_name='value')
    value_char = models.CharField(max_length=300, blank=True, default='')
    value_int = models.IntegerField(blank=True, null=True)
    value_float = models.FloatField(blank=True, null=True)
    value_bool = models.BooleanField(null=True)
    value_txt = models.TextField(blank=True)
    value_date = models.DateField(blank=True, null=True)
    value_datetime = models.DateTimeField(blank=True, null=True)

    def _get_value(self):
        value = getattr(self, f'value_{self.attribute.type}')
        if hasattr(value, 'all'):
            value = value.all()
        return value

    def _set_value(self, new_value):
        attr_name = f'value_{self.attribute.type}'
        setattr(self, attr_name, new_value)
        return

    value = property(_get_value, _set_value)

    class Meta:
        verbose_name = _('Value')
        verbose_name_plural = _('Value')
        permissions = []

    def __str__(self):
        return f'{self.attribute.name} : {self.value}'


class ProductItems(models.Model):
    """
    model is count quantity product
    """
    product = models.ForeignKey(
        Product, blank=True,
        on_delete=models.CASCADE,
        default=None,
        related_name='product_items')
    quantity = models.PositiveIntegerField(_('Quantity of products'), default=0)
    create_at = models.DateTimeField(_('Создан'), auto_now_add=True)
    is_active = models.BooleanField(_("Is active"), default=True)

    @property
    def remains(self):
        if self.quantity == 0:
            return 0
        quantity_dct = self.position_product.aggregate(Sum('quantity'))
        return self.quantity - quantity_dct['quantity__sum']

    class Meta:
        verbose_name = _('Product Items')
        verbose_name_plural = _('Products Items')
        permissions = []


class PromoCode(AbstarctModels):
    code = models.CharField(_('Code'), max_length=50, blank=True, default='')
    quantity = models.PositiveIntegerField(_('Quantity of cods'), default=0)
    is_active = models.BooleanField(_("Is active code"), default=True)

    class Meta:
        verbose_name = _('Promo code')
        verbose_name_plural = _('Promo cods')
        permissions = []

    @property
    def remains(self):
        if self.quantity == 0:
            return 0
        return self.quantity - self.basket.all().count()


class Basket(models.Model):
    customer = models.ForeignKey(
        Customer, blank=True,
        on_delete=models.CASCADE,
        default=None,
        related_name='basket')
    create_at = models.DateTimeField(_('Создан'), auto_now_add=True)
    promocode = models.ForeignKey(
        PromoCode, blank=True,
        on_delete=models.CASCADE,
        default=None,
        related_name='basket')
    status = models.CharField(choices=Status.CHOISES(), max_length=9, blank=True)

    class Meta:
        verbose_name = _('Basket')
        verbose_name_plural = _('Baskets')
        permissions = []


class PositionProduct(models.Model):
    """
    Позиция товара + количество
    """
    product_items = models.ForeignKey(
        ProductItems, blank=True,
        on_delete=models.CASCADE,
        default=None,
        related_name='position_product')
    quantity = models.PositiveIntegerField(_('Quantity of products'), default=0)
    basket = models.ForeignKey(
        Basket, blank=True,
        on_delete=models.CASCADE,
        default=None,
        related_name='position_product')
    create_at = models.DateTimeField(_('Создан'), auto_now_add=True)

    class Meta:
        verbose_name = _('Position product')
        verbose_name_plural = _('Position products')
        permissions = []


class ProductsCompare(models.Model):
    """
    сделать ограничение на запись не больше 5 на одного юзера
    сортировка по лучшему значению
    """
    products = models.ForeignKey(
        Product, blank=True,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name='products_compare')
    customer = models.ForeignKey(
        Customer, blank=True,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name='products_compare')
    create_at = models.DateTimeField(_('Создан'), auto_now_add=True)

    class Meta:
        verbose_name = _('Products for compare')
        verbose_name_plural = _('Products for compare')
        permissions = []


class DesiredProducts(models.Model):
    customer = models.ForeignKey(
        Customer, blank=True,
        on_delete=models.CASCADE,
        default=None,
        related_name='desired_products')
    items = models.ForeignKey(
        ProductItems, blank=True,
        on_delete=models.CASCADE,
        default=None,
        related_name='desired_products')

    class Meta:
        verbose_name = _('Desired Products')
        verbose_name_plural = _('Desired Products')
        permissions = []


class Feedback(models.Model):
    customer = models.ForeignKey(
        Customer, blank=True,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name='feedback')
    text = models.TextField(blank=True)
    product = models.ForeignKey(
        Product, blank=True,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name='feedback')

    class Meta:
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedbacks')
        permissions = []
