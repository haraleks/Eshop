from django.urls import reverse
from faker import Faker
from rest_framework import status

from core.tests import InitClass
from shop.models import (Product, Category, Subcategory, ProductsCompare, WishList)

fake = Faker()


class TestProduct(InitClass):
    def setUp(self) -> None:
        Product.objects.get_or_create(
            price=1000,
            description='TEsts descriptions',
            name='Iphone 13'
        )
        self.anon_client = self.anon_client()

    def test_get(self):
        response = self.anon_client.get(reverse('products'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCategory(InitClass):
    def setUp(self) -> None:
        category, _ = Category.objects.get_or_create(
            name='First category'
        )
        Subcategory.objects.get_or_create(
            name='First subcategory',
            category=category
        )
        self.anon_client = self.anon_client()

    def test_get(self):
        response = self.anon_client.get(reverse('category'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCompare(InitClass):
    def setUp(self) -> None:
        self.product = self.create_product()
        self.user, self.customer, self.customer_client = self.create_customer()
        compare, _ = ProductsCompare.objects.get_or_create(
            products=self.product,
            customer=self.customer
        )
        self.path_pk = reverse('compare_pk', args=[compare.pk])
        self.anon_client = self.anon_client()

    def test_get(self):
        response = self.customer_client.get(reverse('compare'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_anonim(self):
        response = self.anon_client.get(reverse('compare'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post(self):
        product = self.create_product()
        data = {
            "products": product.pk
        }
        response = self.customer_client.post(reverse('compare'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['products'], data['products'])

    def test_put(self):
        data = {
            "products": self.product.pk
        }
        response = self.customer_client.put(self.path_pk, data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete(self):
        response = self.customer_client.delete(self.path_pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_anonim(self):
        response = self.anon_client.delete(self.path_pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestWishList(InitClass):
    def setUp(self) -> None:
        self.product = self.create_product()
        self.user, self.customer, self.customer_client = self.create_customer()
        wish_list, _ = WishList.objects.get_or_create(
            product=self.product,
            customer=self.customer
        )
        self.path_pk = reverse('wish_list_pk', args=[wish_list.pk])
        self.anon_client = self.anon_client()

    def test_get(self):
        response = self.customer_client.get(reverse('wish_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_anonim(self):
        response = self.anon_client.get(reverse('wish_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post(self):
        product = self.create_product()
        data = {
            "product": product.pk
        }
        response = self.customer_client.post(reverse('wish_list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['product'], data['product'])

    def test_put(self):
        data = {
            "product": self.product.pk
        }
        response = self.customer_client.put(self.path_pk, data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete(self):
        response = self.customer_client.delete(self.path_pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_anonim(self):
        response = self.anon_client.delete(self.path_pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestCarts(InitClass):
    def setUp(self) -> None:
        self.user, self.customer, self.customer_client = self.create_customer()
        self.cart, position_product = self.added_carts(self.customer)

        self.path_pk = reverse('carts_pk', args=[self.cart.pk])
        self.anon_client = self.anon_client()

    def test_get(self):
        response = self.customer_client.get(reverse('carts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_anonim(self):
        response = self.anon_client.get(reverse('carts'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post(self):
        data = {
            "customer": self.customer.pk
        }
        response = self.customer_client.post(reverse('carts'), data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put(self):
        self.user2, self.customer2, self.customer_client2 = self.create_customer(
            email=fake.email()
        )
        data = {
            "customer": self.customer2.pk
        }
        response = self.customer_client.put(self.path_pk, data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete(self):
        response = self.customer_client.delete(self.path_pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_anonim(self):
        response = self.anon_client.delete(self.path_pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_status_carts(self):
        self.path_pk = reverse('change_status_carts', args=[self.cart.pk])

        data = {
            "status": 'created'
        }
        response = self.customer_client.put(self.path_pk, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PositionProducts(InitClass):
    def setUp(self) -> None:
        self.user, self.customer, self.customer_client = self.create_customer()
        self.carts, self.position_product = self.added_carts(self.customer)

        self.path_pk = reverse('position_products_pk', args=[self.position_product.pk])
        self.anon_client = self.anon_client()

    def test_get(self):
        response = self.customer_client.get(reverse('position_products'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_anonim(self):
        response = self.anon_client.get(reverse('position_products'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post(self):
        data = {
            "customer": self.customer.pk
        }
        response = self.customer_client.post(reverse('carts'), data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put(self):
        self.user2, self.customer2, self.customer_client2 = self.create_customer(
            email=fake.email()
        )
        data = {
            "customer": self.customer2.pk
        }
        response = self.customer_client.put(self.path_pk, data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete(self):
        response = self.customer_client.delete(self.path_pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_anonim(self):
        response = self.anon_client.delete(self.path_pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
