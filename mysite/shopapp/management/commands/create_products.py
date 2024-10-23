from django.core.management import BaseCommand
from shopapp.models import Product

class Command(BaseCommand):
    '''
    Создаёт новые продукты
    '''

    def handle(self, *args, **options):
        self.stdout.write('Создание продукта')

        products_names = [
            "Laptop",
            "Desktop",
            "Smartphone"
        ]

        for products_name in products_names:
            product, created = Product.objects.get_or_create(name=products_name)
            self.stdout.write(f"Создание продукта {product.name}")

        self.stdout.write(self.style.SUCCESS("Продукты созданы"))