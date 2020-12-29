from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models.profile_models import Customer
from users.utils import vaildation_password

User = get_user_model()


class CustomerRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    sex = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)

    def validate_password(self, data):
        errors_dct = vaildation_password(data)
        if errors_dct:
            raise serializers.ValidationError(errors_dct)
        return data

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": ["Password doesn't match"]})
        return super().validate(attrs)

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = User.objects.create_user(
            email=email, password=password)
        validated_data['user'] = user
        customer = Customer.objects.create(**validated_data)
        return customer


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


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class UpdateCustomerSerializer(CustomerSerializer):

    first_name = serializers.CharField(required=False)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)


class ChangePasswordUserSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    new_password2 = serializers.CharField()

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError("Old password is not the same")
        if attrs['new_password'] == attrs['old_password']:
            raise serializers.ValidationError("You entered your old password")
        else:
            errors_dct = vaildation_password(attrs['new_password'])
            if errors_dct:
                raise serializers.ValidationError(errors_dct)
            return attrs

    def update(self, instance, validated_data):
        user = self.context['request'].user
        user.set_password(validated_data['new_password'])
        user.save()
        res = {'status': 'success',
               'message': 'Password updated successfully'}
        return res
