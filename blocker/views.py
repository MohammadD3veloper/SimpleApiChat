from django.shortcuts import render
from rest_framework import generics
from .serializers import BlockedIpsSerializer, IpAdressesSerializer
from .models import IpAddress, Blocklist
from rest_framework.permissions import IsAdminUser


# Create your views here.
class IpAddressRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser,]
    serializer_class = IpAdressesSerializer
    queryset = IpAddress.objects.all()


class IpAddressList(generics.ListAPIView):
    permission_classes = [IsAdminUser,]
    serializer_class = IpAdressesSerializer
    queryset = IpAddress.objects.all()


class BlockedIpAddressRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser,]
    serializer_class = BlockedIpsSerializer
    queryset = Blocklist.objects.all()


class BlockedIpAddressList(generics.ListAPIView):
    permission_classes = [IsAdminUser,]
    serializer_class = BlockedIpsSerializer
    queryset = Blocklist.objects.all()
