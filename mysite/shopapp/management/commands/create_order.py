from collections.abc import Sequence
from django.db import transaction

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from shopapp.models import Order, Product


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Создание заказа с товарами")
        user = User.objects.get(username="admin")
        products: Sequence[Product] = Product.objects.only("id").all() # .defer -> перечисление полей, которые не нужны. .only - только те, которые нужны
        order, created = Order.objects.get_or_create(
            deliveri_address="Пожилой переулок 23, дом 24",
            promocode="SALE1234",
            user=user,
        )
        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(f"Заказы созданы {order}")