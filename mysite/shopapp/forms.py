from django.contrib.auth.models import Group
from django.forms import ModelForm
from django.core import validators
from .models import Product, Order

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount"

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "deliveri_address", "promocode", "user", "products"

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ["name"]

