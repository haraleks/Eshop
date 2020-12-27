import random

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum, F, Q
from django.utils.translation import ugettext_lazy as _

from shop.utils import discount_birthday
from users.constants import TypeValue, Status, SexProduct
from users.models.profile_models import Customer


class UserManager(models.Manager):
    def random(self, sex=None, subcategory=None, exclude_id=None, age=None):
        instance = list(self.filter(Q(age_to__gte=age) & Q(age_from__lte=age),
                                    sex=sex, subcategory=subcategory).exclude(pk=exclude_id))
        random.shuffle(instance)
        return instance


class AbstractModels(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(_('Date created'), auto_now_add=True)

    class Meta:
        permissions = []
        abstract = True

    def __str__(self):
        return self.name


class Category(AbstractModels):
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        permissions = []

    @property
    def count_subcategory(self):
        return self.subcategory.all().count()

    @property
    def count_product(self):
        all_subcategory = self.subcategory.all()
        return Product.objects.filter(subcategory__in=all_subcategory).count()


class Subcategory(AbstractModels):
    category = models.ForeignKey(
        Category, blank=True,
        on_delete=models.CASCADE,
        null=True,
        related_name='subcategory')

    class Meta:
        verbose_name = _('Subcategory')
        verbose_name_plural = _('Subcategories')
        permissions = []

    @property
    def count_prodact(self):
        return self.product.all().count()

    def __str__(self):
        return f'{self.category.name} - {self.name}'


class Product(AbstractModels):
    """
    Price -  в копейках
    """
    objects = UserManager()

    price = models.IntegerField(_('Price'), validators=[MinValueValidator(0)], default=0)
    sku = models.CharField(_('SKU'), max_length=50, blank=True, default='')
    description = models.TextField(_('Description product'), blank=True)
    subcategory = models.ForeignKey(
        Subcategory, blank=True,
        on_delete=models.PROTECT,
        null=True,
        related_name='product')
    sex = models.CharField(
        _('Sex'),
        choices=SexProduct.CHOISES(),
        max_length=1,
        default=SexProduct.UNISEX.value,
        blank=True)
    age_from = models.IntegerField(_('Age min'), blank=True, null=True)
    age_to = models.IntegerField(_('Age max'), blank=True, null=True)
    is_active = models.BooleanField(_("Is active"), default=True)
    main_character = models.ForeignKey(
        'Attribute', blank=True,
        on_delete=models.CASCADE,
        null=True,
        related_name='main_character_product')

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        permissions = []


class Attribute(AbstractModels):
    type = models.CharField(choices=TypeValue.CHOISES(),
                            max_length=8,
                            default=TypeValue.CHAR)

    class Meta:
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attribute')
        permissions = []

    def __str__(self):
        return f'{self.name} : {self.type}'


class Value(models.Model):
    attribute = models.ForeignKey(
        Attribute, blank=True,
        on_delete=models.CASCADE,
        null=True,
        related_name='value_model')
    product = models.ForeignKey(
        Product, blank=True,
        on_delete=models.CASCADE,
        null=True,
        related_name='value_model')
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
    product = models.OneToOneField(
        Product, blank=True,
        on_delete=models.CASCADE,
        default=None,
        related_name='product_items')
    quantity = models.IntegerField(_('Quantity of products'), validators=[MinValueValidator(0)], default=0)
    create_at = models.DateTimeField(_('Создан'), auto_now_add=True)
    is_active = models.BooleanField(_("Is active"), default=True)

    @property
    def remains(self):
        # TODO учет по активным корзинам не отменённым
        if self.quantity == 0:
            return 0
        quantity_dct = self.position_product.aggregate(Sum('quantity'))
        if not quantity_dct['quantity__sum']:
            quantity_dct['quantity__sum'] = 0
        return self.quantity - quantity_dct['quantity__sum']

    class Meta:
        verbose_name = _('Product Items')
        verbose_name_plural = _('Products Items')
        permissions = []

    def __str__(self):
        return f'{self.product.name} : {self.quantity}'


class PromoCode(AbstractModels):
    code = models.CharField(_('Code'), max_length=50, blank=True, default='')
    quantity = models.PositiveIntegerField(_('Quantity of cods'), default=0)
    discount = models.IntegerField(
        _('Discount'), blank=True, null=True,
        default=0, validators=[MinValueValidator(1), MaxValueValidator(30)])
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
        null=True,
        related_name='basket')
    create_at = models.DateTimeField(_('Создан'), auto_now_add=True)
    promocode = models.ForeignKey(
        PromoCode, blank=True,
        on_delete=models.CASCADE,
        null=True,
        related_name='basket')
    status = models.CharField(choices=Status.CHOISES(), max_length=9, blank=True)

    @property
    def total_order(self):
        total = self.position_product.annotate(
            total_price=F('product_items__product__price') * F('quantity')).\
            aggregate(Sum('total_price'))
        return total['total_price__sum']

    @property
    def promocod_discount(self):
        if self.promocode and self.promocode.is_active:
            return self.promocode.discount
        return 0

    @property
    def discount(self):
        discount_birth = discount_birthday(self.customer.date_of_birth)
        if discount_birth and discount_birth > self.promocod_discount:
            return discount_birth
        return self.promocod_discount

    @property
    def total_with_discount(self):
        if self.discount:
            return self.total_order - (self.total_order * self.discount / 100)
        return self.total_order

    class Meta:
        verbose_name = _('Basket')
        verbose_name_plural = _('Baskets')
        permissions = []


class PositionProduct(models.Model):
    """
    Позиция товара + количество
    """
    # TODO  валидацию по остаткам
    product_items = models.ForeignKey(
        ProductItems, blank=True,
        on_delete=models.PROTECT,
        null=True,
        related_name='position_product')
    quantity = models.IntegerField(_('Quantity of products'), validators=[MinValueValidator(0)], default=0)
    basket = models.ForeignKey(
        Basket, blank=True,
        on_delete=models.CASCADE,
        null=True,
        related_name='position_product')
    create_at = models.DateTimeField(_('Создан'), auto_now_add=True)

    class Meta:
        verbose_name = _('Position product')
        verbose_name_plural = _('Position products')
        permissions = []

    @property
    def product_name(self):
        return self.product_items.product.name

    @property
    def product_price(self):
        return self.product_items.product.price

    @property
    def total_product_price(self):
        return self.product_items.product.price * self.quantity

    def __str__(self):
        return f'{self.basket} : {self.product_items} | {self.quantity} ({self.basket.customer})'


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
        related_name='products_compare')
    create_at = models.DateTimeField(_('Создан'), auto_now_add=True)

    class Meta:
        verbose_name = _('Products for compare')
        verbose_name_plural = _('Products for compare')
        permissions = []


class DesiredProducts(models.Model):
    """
    model wish list products
    """
    customer = models.ForeignKey(
        Customer, blank=True,
        on_delete=models.CASCADE,
        null=True,
        related_name='desired_products')
    product = models.ForeignKey(
        Product, blank=True,
        on_delete=models.CASCADE,
        null=True,
        related_name='desired_products')

    class Meta:
        verbose_name = _('Desired Products')
        verbose_name_plural = _('Desired Products')
        permissions = []

    def __str__(self):
        return f'{self.product.name} - {self.customer.pk} {self.customer.user}'


class Feedback(models.Model):
    customer = models.ForeignKey(
        Customer, blank=True,
        on_delete=models.SET_NULL,
        null=True,
        related_name='feedback')
    text = models.TextField(blank=True)
    product = models.ForeignKey(
        Product, blank=True,
        on_delete=models.SET_NULL,
        null=True,
        related_name='feedback')

    class Meta:
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedbacks')
        permissions = []
