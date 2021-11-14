from rest_framework import serializers
from .models import Blocklist, IpAddress


class IpAdressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IpAddress
        fields = ['__all__']


class BlockedIpsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blocklist
        fields = ['__all__']
