from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import BlogSerializer
from .models import News
from rest_framework.permissions import AllowAny
from users.permissions import IsStaffOrReadOnly


# Create your views here.
class RetreiveDestroyUpdateNewsApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsStaffOrReadOnly,]
    serializer_class = BlogSerializer
    queryset = News.objects.filter(published=True)


class ListCreateNewsApiView(ListCreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = BlogSerializer
    queryset = News.objects.filter(published=True)
