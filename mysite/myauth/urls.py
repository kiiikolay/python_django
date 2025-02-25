from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    get_cookie_view,
    set_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutView,
    AboutMeView,
    RegisterView,
    start_auth_view,
    FooBarView,
    ProfileListView,
    AboutMeDetailView,
    ProfileAvatarUpdateView,
)

app_name = "myauth"

urlpatterns = (
    path("", start_auth_view, name="start"),
    # path("login/", login_view, name="login"),
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True
        ),
        name="login"),
    path("reg/", RegisterView.as_view(), name='register'),
    path("profiles-list/", ProfileListView.as_view(), name='profiles-list'),
    path("about-me/", AboutMeView.as_view(), name='about-me'),
    path("about-me-details/<int:pk>/", AboutMeDetailView.as_view(), name='about-me-details'),
    path("about-me-details/<int:pk>/update", ProfileAvatarUpdateView.as_view(), name='update-avatar'),
    # path("logout/", MyLogoutView.as_view(), name='logout'),
    path("logout/", LogoutView.as_view(), name='logout'),

    path("cookie/get/", get_cookie_view, name='cookie-get'),
    path("cookie/set/", set_cookie_view, name='cookie-set'),

    path("session/set/", set_session_view, name='session-set'),
    path("session/get/", get_session_view, name='session-get'),

    path("foo-bar", FooBarView.as_view(), name='foo-bar'),
)