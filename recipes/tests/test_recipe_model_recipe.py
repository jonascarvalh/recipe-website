from django.core.exceptions import ValidationError
from .test_recipe_base import Recipe, RecipeTestBase, Category
from parameterized import parameterized

class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()
    
    def make_recipe_no_defaults(self):
        return Recipe(
            category=self.make_category(name='Default Category'),
            author=self.make_author(username='newuser'),
            title = 'Recipe Title',
            description= 'Recipe Description',
            slug = 'recipe-slug',
            preparation_time = '30',
            preparation_time_unit = 'Minutes',
            servings = '3',
            servings_unit = 'Persons',
            preparation_steps = 'Recipe Steps',
        )

    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ])
    
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'a' * (max_length+1))

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
    
    def test_recipe_preparation_time_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        recipe.full_clean()
        recipe.save()
        self.assertFalse(
            recipe.preparation_steps_is_html, 
            msg='Recipe preparation_steps_is_html is not false'
        )
    
    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        recipe.full_clean()
        recipe.save()
        self.assertFalse(
            recipe.is_published, 
            msg='Recipe is_published is not false'
        )
    
    def test_recipe_string_representation(self):
        needed = 'Testing Representation'
        self.recipe.title = 'Testing Representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe), 
            needed,
            msg=f'Recipe string representation need must be recipe {needed}'
        )