import pytest
from selenium.webdriver.common.by import By
from .base import RecipeBaseFunctionalTest
from unittest.mock import patch

@pytest.mark.functional_test
class RecipeHomepageFunctionalTest(RecipeBaseFunctionalTest):
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here 😭', body.text)