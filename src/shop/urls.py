from django.urls import path

from shop.views import (ProductView, CategoryiesView, ProductsCompareViewSet,
                        WishListViewSet, CartsViewDelete, PositionProductsCreateDelete, SendPayCarts)

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
    path('products/', ProductView.as_view({'get': 'list'}), name='products'),

    path('categories/', CategoryiesView.as_view({'get': 'list'}), name='category'),

    path('products-for-compare/', ProductsCompareViewSet.as_view(as_view_common), name='compare'),
    path('products-for-compare/<int:pk>/', ProductsCompareViewSet.as_view({'delete': 'destroy'}), name='compare_pk'),

    path('wish_list/', WishListViewSet.as_view(as_view_common), name='wish_list'),
    path('wish_list/<int:pk>/', WishListViewSet.as_view({'delete': 'destroy'}), name='wish_list_pk'),

    path('carts/', CartsViewDelete.as_view({'get': 'list'}), name='carts'),
    path('carts/<int:pk>/', CartsViewDelete.as_view({'delete': 'destroy'}), name='carts_pk'),
    path('change_status_carts/<int:pk>/', SendPayCarts.as_view({'put': 'update'}), name='change_status_carts'),

    path('cart_products/', PositionProductsCreateDelete.as_view({'post': 'create'}), name='position_products'),
    path('cart_products/<int:pk>/',
         PositionProductsCreateDelete.as_view({'delete': 'destroy'}), name='position_products_pk'),
]
