from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import include, path
from rest_framework.test import (APIClient, APITestCase,
                                 URLPatternsTestCase)
from rest_framework_simplejwt.tokens import AccessToken

from users.models.profile_models import Customer

SIMPLE_JWT = settings.SIMPLE_JWT


class InitClass(APITestCase, URLPatternsTestCase):
    User = get_user_model()

    urlpatterns = [
        path('api/v1/', include('shop.urls')),
        path('api/v1/', include('users.urls')),
    ]

    def create_user(self):
        user = self.User.objects.create(email='testuser@gmail.com',
                                        password='PaSwOrD123')
        access = AccessToken.for_user(user)
        client = self.login_user(access)
        return user, client

    def create_customer(self, email='testcustom@gmail.com', password='PaSwOrD123'):
        user, _ = self.User.objects.get_or_create(email=email, password=password, is_superuser=False)
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
