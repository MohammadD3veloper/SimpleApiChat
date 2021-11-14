from django.urls import path, include
from .views import Authentication, email_activation, reset_password_confirm
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'auth', Authentication)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/activate_email/<uidb64>/<token>/', email_activation, name='activation'),
    path('auth/password/reset/<uidb64>/<token>/', reset_password_confirm, name='password-reset'),
] 