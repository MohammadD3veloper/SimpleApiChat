from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from blocker.models import Blocklist, IpAddress


class BlocklistMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        user_ip = request.META.get("REMOTE_ADDR")
        IpAddress.objects.get_or_create(ip_address=user_ip)

        try:
            Blocklist.objects.get(ip_address=user_ip)
            Response(status=status.HTTP_403_FORBIDDEN)                
        except Blocklist.DoesNotExist:
            pass

        if cache.get(user_ip):
            req_nums = cache.get(user_ip)
            if req_nums >= 30:
                Blocklist.objects.create(ip_address=user_ip)
            else:
                cache.incr(user_ip)
        else:
            cache.set(user_ip, 1, 5000)
  
        response = self.get_response(request)
        return response
