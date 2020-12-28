from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models.profile_models import Customer
from users.serializers import (CustomerSerializer, UpdateCustomerSerializer, ChangePasswordUserSerializer,
                               CustomerRegistrationSerializer)

User = get_user_model()


class CustomerRegistration(ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Customer.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = CustomerRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        model = serializer.create(serializer.data)
        serializer = self.get_serializer(model)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UpdateCustomerSerializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
        new_serializer = self.get_serializer(instance)
        return Response(new_serializer.data)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class ChangePasswordUser(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        instance = request.user
        serializer = ChangePasswordUserSerializer(instance, data=request.data,
                                                  context={"request": self.request})
        if serializer.is_valid(raise_exception=True):
            response = serializer.save()

        return Response(response)


class DeletedCustomer(ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Customer.objects.all()
