from django.urls import path, include
from rest_framework import routers
from .views import (
    RetreiveDestroyUpdateNewsApiView,
    ListCreateNewsApiView,
)



urlpatterns = [
    path('blog/<int:pk>', RetreiveDestroyUpdateNewsApiView.as_view()),
    path('blog/', ListCreateNewsApiView.as_view())
] 