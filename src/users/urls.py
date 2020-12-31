from django.urls import path

from users.views import CustomerRegistration, ChangePasswordUser, DeletedCustomer

as_view_common = {
    'get': 'list',
    'post': 'create'
}

as_view_with_pk = {
    'get': 'retrieve',
    'put': 'update',
}

urlpatterns = [
    path('customer/', CustomerRegistration.as_view(as_view_common), name='customer'),
    path('customer/<int:pk>/', CustomerRegistration.as_view(as_view_with_pk), name='customer_id'),
    path('change_password/', ChangePasswordUser.as_view({'put': 'update'}), name='customer_pass'),
    path('deleted_customer/<int:pk>/', DeletedCustomer.as_view({'delete': 'destroy'}), name='del_customer'),
]
