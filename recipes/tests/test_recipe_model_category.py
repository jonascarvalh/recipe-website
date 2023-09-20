from django.core.exceptions import ValidationError
from .test_recipe_base import Recipe, RecipeTestBase, Category
from parameterized import parameterized

class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category()
        return super().setUp()
    
    def test_recipe_category_string(self):
        needed = 'Category Test Representation'
        self.category.name = 'Category Test Representation'
        self.category.full_clean()
        self.category.save()
        self.assertEqual(
            str(self.category),
            needed
        )
    
    def test_category_model_max_length(self):
        self.category.name = 'a'*70

        with self.assertRaises(ValidationError):
            self.category.full_clean()