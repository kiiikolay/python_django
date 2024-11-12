from django.urls import path
from .views import process_det_view, user_form, handel_file_uploap

app_name = "requestdataapp"

urlpatterns = [
    path("get/", process_det_view, name="get-vew"),
    path("bio/", user_form, name="user-form"),
    path("upload/",handel_file_uploap , name="file-upload"),
]

