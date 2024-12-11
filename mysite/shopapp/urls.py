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


]