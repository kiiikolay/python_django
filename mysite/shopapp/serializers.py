from rest_framework import serializers

from .models import Product, Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "pk",
            "name",
            "description",
            "price",
            "discount",
            "create_at",
            "archived",
            "preview",
        ]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "deliveri_address",
            "promocode",
            "create_at",
            "user",
            "products",
        ]