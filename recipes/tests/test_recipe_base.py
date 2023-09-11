from recipes.models import Category, Recipe, User
from django.test import TestCase

class RecipeTestBase(TestCase):
    def setUp(self) -> None:
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name = 'Jonas',
            last_name = 'Sousa',
            username = 'jonassousa',
            password = '123456',
            email = 'username@email.com'
        )
        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title = 'Recipe Title',
            description= 'Recipe Description',
            slug = 'Recipe Slug',
            preparation_time = '30',
            preparation_time_unit = 'Minutes',
            servings = '3',
            servings_unit = 'Persons',
            preparation_steps = 'Recipe Steps',
            preparation_steps_is_html = False,
            created_at = '2023-09-11 00:00:00',
            updated_at = '2023-09-11 00:00:00',
            is_published = True
        )
        return super().setUp()