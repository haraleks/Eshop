from django.urls import path

from shop.views import (ProductViewSet, CategoryViewSet, ProductsCompareViewSet,
                        WishListViewSet, BasketViewSet, PositionProductsViewSet, SendPayBasket)

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
    path('product/', ProductViewSet.as_view({'get': 'list'}), name='product'),
    path('product/<int:pk>/', ProductViewSet.as_view(as_view_with_pk), name='product_pk'),

    path('category/', CategoryViewSet.as_view(as_view_common), name='customer'),
    path('category/<int:pk>/', CategoryViewSet.as_view(as_view_with_pk), name='customer_pk'),

    path('compare/', ProductsCompareViewSet.as_view(as_view_common), name='compare'),
    path('compare/<int:pk>/', ProductsCompareViewSet.as_view({'delete': 'destroy'}), name='compare_pk'),

    path('wish_list/', WishListViewSet.as_view(as_view_common), name='wish_list'),
    path('wish_list/<int:pk>/', WishListViewSet.as_view({'delete': 'destroy'}), name='wish_list_pk'),

    path('basket/', BasketViewSet.as_view({'get': 'list'}), name='basket'),
    path('basket/<int:pk>/', BasketViewSet.as_view({'delete': 'destroy'}), name='basket_pk'),
    path('change_status_baskets/<int:pk>/', SendPayBasket.as_view({'put': 'update'}), name='basket_pk'),

    path('position_products/', PositionProductsViewSet.as_view({'post': 'create'}), name='position_products'),
    path('position_products/<int:pk>/',
         PositionProductsViewSet.as_view({'delete': 'destroy'}), name='position_products_pk'),
]
