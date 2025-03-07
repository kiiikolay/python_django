from tempfile import template
from django.contrib.auth.views import LoginView
from django.urls import path
from .views import (
    api_hello_view,
    GroupsListView
)

app_name = "myapiapp"

urlpatterns = [
    path("hello/", api_hello_view, name='hello'),
    path("groups/", GroupsListView.as_view(), name='groups'),
]