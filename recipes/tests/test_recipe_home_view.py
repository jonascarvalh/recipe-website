from django.urls import resolve, reverse
from recipes import views
from unittest.mock import patch
from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_home_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)
    
    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')
    
    def test_recipe_home_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipes found',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        # Need a recipe for this test
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn('Recipe Title', content)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe is published False dont show"""
        # Need a recipe for this test
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        # Check if one recipe exists
        self.assertIn(
            'No recipes found',
            response.content.decode('utf-8')
        )

    # @patch('recipes.views.PER_PAGE', new=3) # It can be done like this
    def test_recipes_in_home_is_paginated(self):
        for i in range(8):
            kwargs = {
                'author_data': {'username': f'u{i}'}, 
                'slug': f's{i}'
            }
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 3)
        self.assertEqual(len(paginator.get_page(1)), 3) # page 1 with 3 recipes
        self.assertEqual(len(paginator.get_page(2)), 3) # page 2 with 3 recipes
        self.assertEqual(len(paginator.get_page(3)), 2) # page 3 with 3 recipes
    
    def test_invalid_page_query_uses_page_one(self):
        for i in range(8):
            kwargs = {
                'author_data': {'username': f'u{i}'}, 
                'slug': f's{i}'
            }
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home') + '?page=1A')
            self.assertEqual(
                response.context['recipes'].number, 
                1
            )

            response = self.client.get(reverse('recipes:home') + '?page=2')
            self.assertEqual(
                response.context['recipes'].number, 
                2
            )

            response = self.client.get(reverse('recipes:home') + '?page=3')
            self.assertEqual(
                response.context['recipes'].number, 
                3
            )