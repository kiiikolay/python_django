from django import forms
from django.core import validators
from .models import Product, Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount"

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "deliveri_address", "promocode", "user", "products"

