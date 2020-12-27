from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models.profile_models import Customer
from users.serializers import CustomerSerializer, UpdateCustomerSerializer, ChangePasswordUserSerializer

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
