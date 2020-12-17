from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.utils import vaildation_password

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']

    def save(self, *args, **kwargs):
        user = User.objects.create_user(email=self.validated_data['email'], password=self.validated_data['password'])
        return user

    def validate_password(self, data):
        errors_dct = vaildation_password(data)
        if errors_dct:
            raise serializers.ValidationError(errors_dct)
        return data

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": ["Password doesn't match"]})
        return super().validate(attrs)
