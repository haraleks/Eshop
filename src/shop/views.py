from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from shop.models import Product
from shop.serializers import ProductSerializer


class ProductViewSet(ModelViewSet):

    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
