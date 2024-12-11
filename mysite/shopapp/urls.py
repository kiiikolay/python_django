from tempfile import template

from django.contrib.auth.views import LoginView
from django.urls import path
from .views import (
    ShopIndexView,
    GroupsListView,
    ProductDetailsView,
    ProductsListView,
    OrdersListViev,
    OrdersDetailViev,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrderUpdateView,
    OrderCreateView,
    OrderDeleteView,
    get_cookie_view,
    set_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutView,
)

app_name = "shopapp"

urlpatterns = [
    path("", ShopIndexView.as_view(), name='index'),
    path("groups/", GroupsListView.as_view(), name='groups_list'),
    path("products/", ProductsListView.as_view(), name='products_list'),
    path("products/create/", ProductCreateView.as_view(), name='product_create'),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name='product_details'),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name='product_update'),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name='product_archive'),
    path("orders/", OrdersListViev.as_view(), name='orders_list'),
    path("orders/create/", OrderCreateView.as_view(), name='create_order'),
    path("orders/<int:pk>/", OrdersDetailViev.as_view(), name='order_details'),
    path("orders/<int:pk>/update", OrderUpdateView.as_view(), name='order_update'),
    path("orders/<int:pk>/confirm_delete/", OrderDeleteView.as_view(), name='order_delete'),
    # path("login/", login_view, name="login"),
    path(
        "login/",
        LoginView.as_view(
            template_name="shopapp/login.html",
            redirect_authenticated_user=True
        ),
        name="login"),
    path("logout/", MyLogoutView.as_view(), name='logout'),
    path("cookie/get/", get_cookie_view, name='cookie-get'),
    path("cookie/set/", set_cookie_view, name='cookie-set'),
    path("session/set/", set_session_view, name='session-set'),
    path("session/get/", get_session_view, name='session-get'),



]