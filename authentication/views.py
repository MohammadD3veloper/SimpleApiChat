from django.shortcuts import render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework.views import Response
from rest_framework.permissions import AllowAny
from authentication.forms import CodeVerificationForm, PasswordResetForm
from authentication.mixins import MultipleSerializerMixin
from .tasks import send_any_email, send_email
from .tokens import account_activation_token
from rest_framework.response import responses
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.core.cache import cache
from django.contrib.auth import authenticate, login, logout
from .models import User
from .serializers import (
    LoginSerializer, 
    PasswordChangeSerializer, 
    PasswordResetConfirmSerializer, 
    PasswordResetEmailSerializer, 
    UpdateUserAccountSerializer, 
    UserSerializer, 
    UserRegistationSerializer
)
from django.http.response import (
    HttpResponse, 
    HttpResponseForbidden, 
    HttpResponseNotFound,
)


# Create your views here.
class Authentication(MultipleSerializerMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_classes = {
        'register': UserRegistationSerializer,
        'login': LoginSerializer,
        'password_reset': PasswordResetEmailSerializer,
        'password_reset_confirm': PasswordResetConfirmSerializer,
        'password_change': PasswordChangeSerializer,
        'update_user_account': UpdateUserAccountSerializer,
        'get_account_info': UserSerializer,
    }

    @action(methods=['POST'], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        email=serializer.validated_data.get('email')
        queryset = User.objects.get(email=email)
        user = UserSerializer(queryset)
        data = {
            'result': {
                'user': user.data,
                'token': serializer.token,
                'verification': 'We have sent the verification link to your email.',
            }
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return Response({
                'result': {
                    'success': 'You have been logged in successfully.'
                }
            })
        return Response({'result':{
            'error': 'Username or password is wrong.'
        }})
        
    @action(methods=['GET'], detail=False)
    def logout(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['POST'], detail=False)
    def password_reset(self, request): 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        user = User.objects.get(email=email)
        uid = user.get_user_uid()
        token = user.account_token_activation()
        send_any_email(subject="Password reset",
        text=f"""
        This email sent for change your password in our website
        if you want to change your password you should done it with
        the following link:
        here is the password reset link:
        {f'http://127.0.0.1:8000/auth/password/reset/{uid}/{token}'}
        Thanks for choosing us
        """,
        email=email,
        )
        return Response({
            'result': {
                'success': 'we have sent an password reset mail to your email address'
            }
        })

    @action(methods=['PUT'], detail=False)
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            'result': {
                'success': 'Your password has been changed. if you have been logged out, please re-login with your new password'
            }
        })

    @action(methods=['PUT'], detail=False)
    def update_user_account(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            'results':
            {
                'success': serializer.data
            }
        })

    @action(methods=['GET'], detail=False)
    def get_account_info(self, request):
        queryset = User.objects.get(pk=request.user.pk)
        serializer = self.get_serializer(queryset)
        return Response({
            'result':{
                'success': serializer.data
            }
        })

    @action(methods=['DELETE'], detail=False)
    def delete_account(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action == 'login':
            self.permission_classes = [AllowAny,]
        
        if self.action == 'logout':
            self.permission_classes = [AllowAny,]

        if self.action == 'register':
            self.permission_classes = [AllowAny,]

        if self.action == 'password_reset':
            self.permission_classes = [AllowAny,]

        return super().get_permissions()


def email_activation(request, uidb64, token):
    if request.method == "POST":
        form = CodeVerificationForm(request.POST)
        try:
            uid = urlsafe_base64_decode(force_text(uidb64))
            user = User.objects.get(pk=uid)
            if form.is_valid():
                code = cache.get(user.email)
                user_code = form.cleaned_data.get('code')
        except(
            TypeError,
            ValueError, 
            OverflowError, 
            User.DoesNotExist
            ):
            user = None
        if code:
            if code == user_code:
                if user is not None and not user.is_active:
                    user.is_active = True
                    user.save()
                    login(request, user)
                    return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
                return HttpResponseNotFound("User Does not exist or your account is already activated.")
            return HttpResponseForbidden('Code is invalid.')
        return HttpResponseForbidden('Code has been expired, please sign up again.') 

    if request.method == "GET":
        form = CodeVerificationForm()
        return render(request, 'activation.html', {'form': form})


def reset_password_confirm(request, uidb64, token):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        try:
            uid = urlsafe_base64_decode(force_text(uidb64))
            user = User.objects.get(pk=uid)
        except(
            TypeError,
            ValueError, 
            OverflowError, 
            User.DoesNotExist
            ):
            user = None
        if user and account_activation_token.check_token(user, token):
            if form.is_valid():
                if form.cleaned_data.get('new_password') == form.cleaned_data.get('new_password_confirm'):
                    user.set_password(form.cleaned_data.get('new_password'))
                    user.save()
                    return HttpResponse("Your password has been reset successfully.")
                else:
                    return HttpResponse("Password do not match.")
            else:
                return form.errors()
        else:
            return HttpResponseForbidden("User does not exist or this page is already checked.")
        
    if request.method == "GET":
        form = PasswordResetForm()
        return render(request, 'reset_password_confirm.html', {'form': form})
