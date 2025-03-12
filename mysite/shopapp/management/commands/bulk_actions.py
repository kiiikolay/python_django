from collections.abc import Sequence
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo balk actions")

        result = Product.objects.filter(
            name__contains="Smartphone" # все объекты у которых в названии есть "Smartphone"
        ).update(discount=10)

        print(result)

        # info = [
        #   ('Smartphone1', 199),
        #   ('Smartphone2', 399),
        #   ('Smartphone3', 399),
        #]
        #products = [
        #    Product(name=name, price=price)
        #   for name, price in info
        #]
        #
        #result = Product.objects.bulk_create(products) #bulk_create - создать сразу пачку товаров, bulk_update - обновление пачки товаров
        #
        #for obj in result:
        #    print(obj)

        self.stdout.write("Done")