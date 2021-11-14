from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.core.cache import cache
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from .tasks import send_email
import random

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk',
            'first_name',
            'last_name',
            'username',
            'email',
            'profile_picture',
            'about',
            'is_staff',
            'is_active',
            'last_login',
            'liked_categories',
        ]


class UserRegistationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(max_length = 150, required=False)
    account_activation_token = serializers.CharField(max_length = 150, required=False)

    def validate(self, attrs):        
        if not attrs['password'] == attrs['password_confirm']:
            raise ValidationError('Passwords do not matches.')
        return attrs

    def create(self, validated_data):
        user, created = User.objects.get_or_create(
            email=validated_data['email'],
            is_active=False
        )

        username = user.create_random_username()
        user.username = username
        user.set_password(validated_data['password'])

        user.save()
        
        random_code = random.randrange(11111,99999)
        uid = user.get_user_uid()
        self.token = user.token(user)
        self.account_activation_token = user.account_token_activation(user)
        
        cache.set(validated_data['email'], random_code, 10000)
        send_email.delay(username=user.username, email=user.email, code=random_code, uid=uid, token=self.token)
        
        return user


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    new_password_confirm = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if self.context['request'].user.check_password(attrs['old_password']):
            if not attrs['new_password'] == attrs['new_password_confirm']:
                raise ValidationError('Passwords do not match')
            else:
                new_pass = attrs['new_password']
                self.context['request'].user.set_password(new_pass)
                self.context['request'].user.save()
        else:
            raise ValidationError('Your have entered wrong old password')
        
        return attrs


class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if not attrs['password'] == attrs['password2']:
            raise ValidationError('The passwords do not macth')

        return attrs


class UpdateUserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'about',
            'profile_picture',
        ]
