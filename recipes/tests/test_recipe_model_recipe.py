from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()
    
    def test_recipe_title_has_raises_error_if_title_is_more_than_65_chars(self):
        self.recipe.title = 'a' * 64

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
        
    def test_recipe_fields_max_length(self):
        fields = [
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ]
        for field, max_length in fields:
            setattr(self.recipe, field, 'a' * (max_length+0))

            with self.assertRaises(ValidationError):
                self.recipe.full_clean()