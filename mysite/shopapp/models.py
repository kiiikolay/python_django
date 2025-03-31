import os
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.deconstruct import deconstructible
from myauth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.core.files import File
from django.utils.translation import gettext_lazy as _, gettext as __

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
    """
    Модель Product представляет товар,
    который можно продавать в интернет-магазине.

    Заказы тут: :model:`shopapp.Order`
    """
    class Meta:
        ordering = ["name", "price"]
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=False, blank=True, db_index=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='products_created')
    preview = models.ImageField(
        null=True,
        blank=True,
        upload_to=product_preview_directory_path
    )
    _preview_pending = None

    def get_absolute_url(self):
        return reverse("shopapp:product_details", kwargs={"pk": self.pk})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._preview_pending = None
        self.old_preview = None

    def save(self, *args, **kwargs):
        is_new = not self.pk
        if is_new:
            super().save(*args, **kwargs)

        if self.preview and self._preview_pending is None:
            self._preview_pending = self.preview
            self.preview = None

        if self._preview_pending:
            file_path = product_preview_directory_path(self, os.path.basename(self._preview_pending.name))

            if isinstance(self._preview_pending, File):
                file_content = self._preview_pending.read()
            elif isinstance(self._preview_pending, str) and default_storage.exists(self._preview_pending):
                file_content = default_storage.open(self._preview_pending, 'rb').read()
            else:
                self._preview_pending = None
                return

            if isinstance(self._preview_pending, File):
                new_file_path = default_storage.save(file_path, self._preview_pending)
            else:
                new_file_path = default_storage.save(file_path, default_storage.open(self._preview_pending, 'rb'))

            self.preview = new_file_path
            self._preview_pending = None

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Product(pk={self.pk}, name={self.name!r})"

def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    return "product/product_{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="image")
    image = models.ImageField(upload_to=product_images_directory_path)
    descriptions = models.CharField(max_length=200, null=False, blank=True)


def __str__(self) -> str:
    return f"Product(pk={self.pk}, name={self.name!r})"

    # @property
    # def description_short(self) -> str:
    #     if len(self.description) < 48:
    #         return self.description
    #     return self.description[:48] + "..."



class Order(models.Model):
    class Meta():
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
    deliveri_address = models.TextField(null=True, blank=False)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")
    receipt = models.FileField(null=True, upload_to='orders/receipts/')
