from http.client import responses
from string import ascii_letters
from random import choices

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission
from django.urls import reverse
from django.conf import settings

from shopapp.models import Product, Order
from shopapp.utils import add_two_numbers


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)

class ProductCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client = Client()
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_create_product(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name" : self.product_name,
                "description" : "A good table",
                "price" : "123.45",
                "discount" : "10",
            },
            HTTP_USER_AGENT = "Chrome, etc",
        )
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )

    def tearDown(self):
        Product.objects.filter(created_by=self.user).delete()
        self.user.delete()

class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(username="testuser")
        cls.product = Product.objects.create(name="Best Prod", created_by=cls.user)

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()
        cls.user.delete()

    def test_get_product(self):
        response = self.client.get(reverse("shopapp:product_details", kwargs={"pk":self.product.pk}), HTTP_USER_AGENT = "Chrome, etc")
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(reverse("shopapp:product_details", kwargs={"pk":self.product.pk}), HTTP_USER_AGENT = "Chrome, etc")
        self.assertContains(response, self.product.name)

class ProductListViewTestCase(TestCase):
    fixtures = [
        'product-fixtures.json',
        'users-fixtures.json',
        'profile-fixtures.json',
        'groups-fixtures.json'
    ]

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)

    def test_products(self):
        response = self.client.get(reverse("shopapp:products_list"), HTTP_USER_AGENT = "Chrome, etc")
        self.assertQuerySetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk
        )
        self.assertTemplateUsed(response, "shopapp/products-list.html")

    def tearDown(self):
        self.user.delete()

class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="testclient", password="testpassword")

    def setUp(self):
        self.client.force_login(self.user)

    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:orders_list"), HTTP_USER_AGENT = "Chrome, etc")
        self.assertContains(response, "Orders")

    def test_order_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"), HTTP_USER_AGENT="Chrome, etc")
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'product-fixtures.json',
        'users-fixtures.json',
        'profile-fixtures.json',
        'groups-fixtures.json'
    ]

    def test_get_products_view(self):
        response = self.client.get(
            reverse("shopapp:products_export"),
            HTTP_USER_AGENT="Chrome, etc"
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived
            }
            for product in products
        ]
        products_data = response.json()

        self.assertEqual(
            products_data["products"],
            expected_data
        )

class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_superuser(username="testclient", password="testpassword")
        # content_type = ContentType.objects.get_for_model(Order)
        # view_order_permission = Permission.objects.get(codename='view_order', content_type=content_type)
        # cls.user.user_permissions.add(view_order_permission)

    def setUp(self):
        self.client.force_login(self.user)
        self.order = Order.objects.create(user=self.user, deliveri_address="Test Address", promocode="TESTPROMO")


    def test_order_details(self):
        response = self.client.get(reverse("shopapp:order_details", kwargs={"pk": self.order.pk}),
                                   HTTP_USER_AGENT="Chrome, etc")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Address")
        self.assertContains(response, "TESTPROMO")
        self.assertEqual(response.context_data['object'].pk, self.order.pk)

    def tearDown(self):
        self.order.delete()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()


class OrdersExportViewTestCase(TestCase):
    fixtures = [
        'product-fixtures.json',
        'users-fixtures.json',
        'profile-fixtures.json',
        'groups-fixtures.json',
        'order-fixtures.json'
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.staff_user = User.objects.create_user(
            username="test_staff_user",
            password="test_password",
            is_staff=True
        )

    @classmethod
    def tearDownClass(cls):
        cls.staff_user.delete()
        super().tearDownClass()

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.staff_user)

    def test_get_orders_view(self):
        response = self.client.get(
            reverse("shopapp:orders_export"),
            HTTP_USER_AGENT="Chrome, etc"
        )
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": order.pk,
                "deliveri_address": order.deliveri_address,
                "promocode": order.promocode,
                "user_id": order.user.id,
                "products": [product.id for product in order.products.all()]
            }
            for order in orders
        ]
        orders_data = response.json()

        self.assertEqual(
            orders_data["orders"],
            expected_data
        )

        def test_get_orders_view_unauthorised(self):
            self.client.logout()
            response = self.client.get(
                reverse("shopapp:orders_export"),
                HTTP_USER_AGENT="Chrome, etc"
            )
            self.assertEqual(response.status_code, 403)
