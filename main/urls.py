from django.urls import path, include
from .views import ChatApiView, ListCreateChatApiView
from rest_framework import routers


urlpatterns = [
    path('chat/', ChatApiView.as_view()),
    path('chat/create/', ListCreateChatApiView.as_view())
] 
