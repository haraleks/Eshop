from django.urls import path

from users.views import CustomerRegistration


as_view_common = {
    'get': 'list',
    'post': 'create',
}

as_view_with_pk = {
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
}

urlpatterns = [
    path('customer/', CustomerRegistration.as_view(as_view_common), name='customer'),
    path('customer/<int:pk>/', CustomerRegistration.as_view(as_view_with_pk), name='customer_pk')
]
