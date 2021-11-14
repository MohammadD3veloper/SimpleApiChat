from django.shortcuts import render
from authentication.serializers import UserSerializer, User
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .permissions import IsStaffOrReadOnly, ReadOnly
# Create your views here.


class RetrieveUpdateDestroyUsersApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsStaffOrReadOnly,]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ListCreateUsersApiView(ListCreateAPIView):
    permission_classes = [IsStaffOrReadOnly,]
    serializer_class = UserSerializer
    queryset = User.objects.all()
