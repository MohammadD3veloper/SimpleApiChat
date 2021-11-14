from django.urls import path, include
from rest_framework import routers
from .views import (
    BlockedIpAddressList,
    IpAddressList,
    IpAddressRetrieveUpdateDestroyApiView,
    BlockedIpAddressRetrieveUpdateDestroyApiView,
)



urlpatterns = [
    path('ips/', IpAddressList.as_view()),
    path('ips/blocked/', BlockedIpAddressList.as_view()),
    path('ip/<int:pk>/', IpAddressRetrieveUpdateDestroyApiView.as_view()),
    path('ip/blocked/<int:pk>/', BlockedIpAddressRetrieveUpdateDestroyApiView.as_view()),
] 