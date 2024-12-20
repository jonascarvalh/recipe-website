from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    def test_recipe_home_view_home_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func.view_class, views.RecipeListViewHome)
    
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

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test category is published False dont show"""
        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:recipe', 
                kwargs={'pk': recipe.category.id}
            )
        )
        # Check if one category exists
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_home_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1})
        )
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, content)

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
    
    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func.view_class, views.RecipeListViewSearch)
    
    def test_recipe_search_loads_correct_template(self):
        url = reverse('recipes:search') + '?q=teste'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)
    
    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=<Teste>'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8')
        )
