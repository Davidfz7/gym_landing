from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
router = routers.DefaultRouter()

urlpatterns = [
    path("login/", views.TestView.as_view(), name = "login"),
    path("signup/", views.TestView.as_view(), name = "signup")
]
