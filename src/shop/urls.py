from django.urls import path

from shop.views import ProductViewSet

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
    path('product/', ProductViewSet.as_view(as_view_common), name='product'),
    path('product/<int:pk>/', ProductViewSet.as_view(as_view_with_pk), name='product_pk')
]
