from tempfile import template
from django.contrib.auth.views import LoginView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

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
    ProductsDataExportView,
    OrderUpdateView,
    OrderCreateView,
    OrderDeleteView,
    OrdersDataExportView,
    api_hello_view,
    ProductViewSet,
    OrderViewSet,
    LatestProductsFeed,

)

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    path("", ShopIndexView.as_view(), name='index'),
    path("groups/", GroupsListView.as_view(), name='groups_list'),
    path("products/", ProductsListView.as_view(), name='products_list'),
    path("products/feed", LatestProductsFeed(), name='products_feed'),
    path("products/export", ProductsDataExportView.as_view(), name='products_export'),
    path("products/create/", ProductCreateView.as_view(), name='product_create'),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name='product_details'),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name='product_update'),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name='product_archive'),
    path("orders/", OrdersListViev.as_view(), name='orders_list'),
    path("orders/export", OrdersDataExportView.as_view(), name='orders_export'),
    path("orders/create/", OrderCreateView.as_view(), name='create_order'),
    path("orders/<int:pk>/", OrdersDetailViev.as_view(), name='order_details'),
    path("orders/<int:pk>/update", OrderUpdateView.as_view(), name='order_update'),
    path("orders/<int:pk>/confirm_delete/", OrderDeleteView.as_view(), name='order_delete'),
    path("api/", include(routers.urls)),
]