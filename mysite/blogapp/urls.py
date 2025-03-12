from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    OrdersListViev
)

app_name = "blog"

urlpatterns = (
    path("", OrdersListViev.as_view(), name="articles"),
)