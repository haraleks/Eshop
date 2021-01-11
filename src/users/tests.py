from django.urls import reverse
from rest_framework import status

from core.tests import InitClass


class TestCustomerRegistration(InitClass):
    def setUp(self) -> None:
        self.user, self.customer, self.customer_client = self.create_customer()
        self.path_pk = reverse('customer_id', args=[self.customer.pk])
        self.path_del = reverse('del_customer', args=[self.customer.pk])
        self.anon_client = self.anon_client()
        self.super_user, self.superuser_client = self.create_super_user()

    def test_get(self):
        response = self.customer_client.get(reverse('customer'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        data = {
            "email": "test@mail.do",
            "password": 'Aa#12312300',
            "password2": 'Aa#12312300',
            "first_name": "firstname",
            "last_name": "lastname",
            "sex": "F",
            "date_of_birth": "1980-01-01"

        }
        response = self.customer_client.post(reverse('customer'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], data['first_name'])

    def test_put(self):
        data = {
            "first_name": "Newfirstname",
            "last_name": "Newlastname",
            "sex": "M",
            "date_of_birth": "1999-01-01"
        }
        response = self.customer_client.put(self.path_pk, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], data['first_name'])

    def test_change_password(self):

        data = {
            "old_password": "PaSwOrD123",
            "new_password": "Newpassword123#",
            "new_password2": "Newpassword123#"
        }
        response = self.customer_client.put(reverse('customer_pass'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')

    def test_delete(self):
        response = self.customer_client.delete(self.path_pk)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_anonim(self):
        response = self.anon_client.delete(self.path_del)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_super_user(self):
        response = self.superuser_client.delete(self.path_del)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
