from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(
            username="Olaffi1",
            password="P@ssword"
        )

        self.client.login(username="Olaffi1", password="P@ssword")
        response = self.client.get(
            reverse("authors:logout"),
            follow=True
        )

        self.assertIn(
            "Invalid logout request",
            response.content.decode("utf-8")
        )
    
    def test_user_tries_to_logout_using_another_user(self):
        User.objects.create_user(
            username="Olaffi1",
            password="P@ssword"
        )

        self.client.login(username="Olaffi1", password="P@ssword")
        response = self.client.post(
            reverse("authors:logout"),
            data={
                "username": "another_user",
            },
            follow=True
        )

        self.assertIn(
            "Invalid logout user",
            response.content.decode("utf-8")
        )
    
    def test_user_logout_successfully(self):
        User.objects.create_user(
            username="Olaffi1",
            password="P@ssword"
        )

        self.client.login(username="Olaffi1", password="P@ssword")
        response = self.client.post(
            reverse("authors:logout"),
            data={
                "username": "Olaffi1"
            },
            follow=True
        )

        self.assertIn(
            "Logged out successfully",
            response.content.decode("utf-8")
        )