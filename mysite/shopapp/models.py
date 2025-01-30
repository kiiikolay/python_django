import os

from django.contrib.auth.models import User
from django.db import models
from django.utils.deconstruct import deconstructible

from myauth.models import Profile


@deconstructible
class ProductPreviewDirectoryPath:
    def __call__(self, instance, filename):
        return "product/product_{pk}/preview/{filename}".format(
            pk=instance.pk,
            filename=filename,
        )


product_preview_directory_path = ProductPreviewDirectoryPath()


class Product(models.Model):
    class Meta:
        ordering = ["name", "price"]

    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='products_created')
    preview = models.ImageField(null=True, blank=True, upload_to=None)  # Убираем upload_to
    _preview_pending = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._preview_pending = None

    def save(self, *args, **kwargs):
        is_new = not self.pk

        if is_new and self.preview:
            self._preview_pending = self.preview
            self.preview = None

        super().save(*args, **kwargs)
        if self._preview_pending:
            file_path = product_preview_directory_path(self, os.path.basename(self._preview_pending.name))

            self.preview.name = file_path
            super().save(*args, **kwargs)
            self._preview_pending = None

    def __str__(self) -> str:
        return f"Product(pk={self.pk}, name={self.name!r})"


def __str__(self) -> str:
    return f"Product(pk={self.pk}, name={self.name!r})"

    # @property
    # def description_short(self) -> str:
    #     if len(self.description) < 48:
    #         return self.description
    #     return self.description[:48] + "..."

    def __str__(self) -> str:
        return f"Product(pk={self.pk}, name={self.name!r})"

class Order(models.Model):
    deliveri_address = models.TextField(null=True, blank=False)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")
    receipt = models.FileField(null=True, upload_to='orders/receipts/')
