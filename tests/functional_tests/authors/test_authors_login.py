import pytest
from .base import AuthorsBaseTest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_succssfully(self):
        string_password = "P@ssw0rd"
        user = User.objects.create_user(
            username="Olaffi1",
            password=string_password
        )

        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse("authors:login"))

        # Usuário vê o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, "main-form")

        # Usuário insere os dados de login
        username = self.get_by_placeholder(form, "Type your username")
        password = self.get_by_placeholder(form, "Type your password")

        username.send_keys(user.username)
        password.send_keys(string_password)

        # Usuário envia o formulário
        form.submit()
        
        # Usuário vê a mensagem de login com sucesso e seu nome
        self.assertIn(
            f"You are logged in with {user.username}.",
            self.browser.find_element(By.TAG_NAME, "body").text
        )
    
    def test_login_create_raises_404_if_not_post_method(self):
        self.browser.get(self.live_server_url + reverse("authors:login_create"))
        self.assertIn(
            "Not Found",
            self.browser.find_element(By.TAG_NAME, "body").text
        )