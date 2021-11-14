from django.urls import path
from .views import (
    ListCreateUsersApiView,
    RetrieveUpdateDestroyUsersApiView,
)


urlpatterns = [
    path('user/<int:pk>/', RetrieveUpdateDestroyUsersApiView.as_view()),
    path('users/', ListCreateUsersApiView.as_view())
]