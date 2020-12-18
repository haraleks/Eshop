from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models.profile_models import Customer
from users.serializers import CustomerSerializer, UpdateCustomerSerializer

User = get_user_model()


class CustomerRegistration(ModelViewSet):

    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Customer.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UpdateCustomerSerializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
        new_serializer = self.get_serializer(
            instance, context={'request': request}
        )
        return Response(new_serializer.data)
