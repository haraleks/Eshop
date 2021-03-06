from django_filters import rest_framework as rest_filters
from rest_framework import permissions, filters, status, mixins
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from shop.models import (Product, Category, ProductsCompare, WishList, PositionProduct, Cart, Status)
from shop.serializers import (ProductSerializer, CategorySerializer, ProductDetailSerializer,
                              ProductsCompareSerializer, WishListSerializer, SubWishListSerializer,
                              AddedProductInCartsSerializer, PositionProductSerializer, CartsSerializer,
                              SendPayCartsSerializer)


class ProductView(mixins.ListModelMixin,
                  GenericViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()
    filter_backends = (rest_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ['price', 'subcategory', 'subcategory__category']
    search_fields = ['name', 'sku', 'id']
    ordering_fields = ['name', 'price', 'id']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductDetailSerializer(instance)
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class CategoryiesView(mixins.ListModelMixin,
                      GenericViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.all()
    filter_backends = (rest_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']


class ProductsCompareViewSet(ModelViewSet):
    serializer_class = ProductsCompareSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ProductsCompare.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(customer=request.user.customer_profile)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class WishListViewSet(ModelViewSet):
    serializer_class = WishListSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = WishList.objects.all()

    def list(self, request, *args, **kwargs):
        querysets = self.filter_queryset(self.get_queryset())
        querysets = querysets.filter(customer=request.user.customer_profile)
        sub_list = []
        for queryset in querysets:
            sub_list.append(queryset.product.subcategory)
        sub_list = set(sub_list)
        page = self.paginate_queryset(list(sub_list))
        context_dir = {
            'queryset': querysets
        }
        if page is not None:
            serializer = SubWishListSerializer(page, many=True, context=context_dir)
            return self.get_paginated_response(serializer.data)

        serializer = SubWishListSerializer(sub_list, many=True, context=context_dir)
        return Response(serializer.data)


class PositionProductsCreateDelete(mixins.CreateModelMixin,
                                   mixins.DestroyModelMixin,
                                   GenericViewSet):
    serializer_class = AddedProductInCartsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = PositionProduct.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        model = serializer.create(serializer.data)
        serializer = PositionProductSerializer(model)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CartsViewDelete(mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    serializer_class = CartsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Cart.objects.all()

    def list(self, request, *args, **kwargs):
        customer = request.user.customer_profile
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(customer=customer, status=Status.CREATED.value)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SendPayCarts(ModelViewSet):
    serializer_class = SendPayCartsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Cart.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
