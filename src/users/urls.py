from django.urls import path

from users.views import (CustomerRegistration, ChangePasswordUser)

as_view_common = {
    'get': 'list',
    'post': 'create'
}

as_view_with_pk = {
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
}

urlpatterns = [
    path('customers/', CustomerRegistration.as_view(as_view_common), name='customer'),
    path('customers/<int:pk>/', CustomerRegistration.as_view(as_view_with_pk), name='customer_id'),
    path('change_password/', ChangePasswordUser.as_view({'put': 'update'}), name='customer_pass')
]
