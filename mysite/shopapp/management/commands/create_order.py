from django.contrib.auth.models import User
from django.core.management import BaseCommand
from shopapp.models import Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Создание заказа")
        user = User.objects.get(username="kikolas")
        order = Order.objects.get_or_create(
            deliveri_address="Пожилой переулок 23, дом 2",
            promocode="SALE123",
            user=user,
        )
        self.stdout.write(f"Заказы созданы {order}")