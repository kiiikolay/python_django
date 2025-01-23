from django.test import TestCase, Client
from myauth.views import get_cookie_view
from django.urls import reverse
import json

class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        response = self.client.get(reverse("myauth:cookie-get"), HTTP_USER_AGENT = "Chrome, etc")
        self.assertContains(response, "Cookie value")

class FooBarViewTest(TestCase):
    def setUp(self):
        self.client = Client()
    def test_foo_bar_view(self):
        response = self.client.get(reverse("myauth:foo-bar"), HTTP_USER_AGENT = "Chrome, etc")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["content-type"], "application/json",
        )
        expected_data = {
            "foo": "bar", "spam": "eggs"}
        # resived_data = json.loads(response.content)
        #
        # self.assertEqual(resived_data, expected_data)
        self.assertJSONEqual(response.content, expected_data)