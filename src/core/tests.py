from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import include, path
from faker import Faker
from rest_framework.test import (APIClient, APITestCase,
                                 URLPatternsTestCase)
from rest_framework_simplejwt.tokens import AccessToken

from shop.models import Category, Subcategory, Product, Cart, ProductQuantity, PositionProduct
from users.models.profile_models import Customer

SIMPLE_JWT = settings.SIMPLE_JWT


class InitClass(APITestCase, URLPatternsTestCase):
    fake = Faker()
    User = get_user_model()

    urlpatterns = [
        path('api/v1/', include('shop.urls')),
        path('api/v1/', include('users.urls')),
    ]

    def create_user(self):
        user = self.User.objects.create(email=self.fake.email(),
                                        password='PaSwOrD123')
        access = AccessToken.for_user(user)
        client = self.login_user(access)
        return user, client

    def create_customer(self, email=fake.email(), password='PaSwOrD123'):
        user = self.User.objects.create_user(email=email, password=password, is_superuser=False)
        profile, _ = Customer.objects.get_or_create(user=user)
        user = self.User.objects.get(pk=user.pk)
        access = AccessToken.for_user(user)
        client = self.login_user(access)
        return user, profile, client

    def anon_client(self):
        client = APIClient()
        return client

    def create_super_user(self, email='adminasйцукйцукйцукq1234dfsadfas@test.ignore.net'):
        user = get_user_model().objects.get_or_create(email=email,
                                                      password='PaSwOrD123',
                                                      is_staff=True,
                                                      is_superuser=True)
        access = AccessToken.for_user(user[0])
        client = self.login_user(access)
        return user[0], client

    @staticmethod
    def login_user(token):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=SIMPLE_JWT['AUTH_HEADER_TYPES'][0] + ' ' + str(token))
        return client

    def login_user_model(self, user):
        access = AccessToken.for_user(user)
        return self.login_user(access)

    def create_product(self):
        category, _ = Category.objects.get_or_create(
            name=self.fake.name()
        )
        subcategory, _ = Subcategory.objects.get_or_create(
            name=self.fake.name(),
            category=category
        )
        product, _ = Product.objects.get_or_create(
            price=1000,
            description=self.fake.text(),
            name=self.fake.name(),
            subcategory=subcategory
        )
        return product

    def added_carts(self, customer):
        product = self.create_product()
        cart, _ = Cart.objects.get_or_create(
            customer=customer,
        )
        ProductQuantity.objects.get_or_create(
            product=product,
            quantity=2
        )
        position_product, _ = PositionProduct.objects.get_or_create(
            product_items=product.product_items,
            quantity=2,
            cart=cart
        )
        return cart, position_product
