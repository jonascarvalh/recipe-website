from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_home_is_correct(self):
        view = resolve(
            reverse('recipes:recipe', kwargs={'pk': 1})
        )
    
    def test_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)
    
    def test_recipe_detail_template_loads_the_correct_recipes(self):
        needed_title = 'This is a detail page - It load one recipe'
        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(
            reverse(
                'recipes:recipe', 
                kwargs={'pk': 1}
            )
        )
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """Test detail is published False dont show"""
        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:recipe', 
                kwargs={'pk': recipe.id}
            )
        )
        # Check if one category exists
        self.assertEqual(response.status_code, 404)