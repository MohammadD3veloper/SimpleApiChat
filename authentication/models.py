from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from rest_framework_simplejwt.tokens import RefreshToken
from base64 import b64decode, b64encode, urlsafe_b64decode
from hashlib import md5


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    profile_picture = models.ImageField(upload_to='images/profiles/')
    about = models.TextField(max_length=300)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_profile_image(self):
        return self.profile_picture.url

    def create_random_username(self):
        hashed = md5(str(self.pk).encode()).digest()
        encoded = b64encode(hashed).decode()
        limited = encoded[0:10]
        return limited

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def account_token_activation(self):
        return account_activation_token.make_token(self)

    def get_user_uid(self):
        return urlsafe_base64_encode(force_bytes(self.pk))
