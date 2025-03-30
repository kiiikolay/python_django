from django.contrib.auth.models import Group
from django import forms
from django.forms import ModelForm
from django.core import validators
from .models import Product, Order

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount", "preview"

    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}),
    )

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "deliveri_address", "promocode", "user", "products"

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ["name"]

class CSVImportForm(forms.Form):
    csv_file = forms.FileField()

