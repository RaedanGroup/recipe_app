from django.test import TestCase
from django.contrib.auth.models import User
from .models import Recipe

# Create your tests here.

class RecipeModelTests(TestCase):
    def setUp(self):
        # Create a user for the tests
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_create_recipe(self):
        # Test creating a recipe
        recipe = Recipe.objects.create(
            name="Test Recipe",
            cooking_time=15,
            ingredients="flour, sugar, eggs",
            created_by=self.user
        )
        self.assertEqual(recipe.name, "Test Recipe")
        self.assertEqual(recipe.cooking_time, 15)
        self.assertEqual(recipe.ingredients, "flour, sugar, eggs")
        self.assertEqual(recipe.created_by, self.user)

    def test_return_ingredients_as_list(self):
        # Test the return_ingredients_as_list method
        recipe = Recipe.objects.create(
            name="Test Recipe",
            cooking_time=15,
            ingredients="flour, sugar, eggs",
            created_by=self.user
        )
        ingredients_list = recipe.return_ingredients_as_list()
        self.assertEqual(ingredients_list, ["flour", "sugar", "eggs"])

    def test_calculate_difficulty_easy(self):
        # Test the calculate_difficulty method for 'Easy' difficulty
        recipe = Recipe.objects.create(
            name="Easy Recipe",
            cooking_time=5,
            ingredients="flour, sugar",
            created_by=self.user
        )
        recipe.calculate_difficulty()
        self.assertEqual(recipe.difficulty, "Easy")

    def test_calculate_difficulty_medium(self):
        # Test the calculate_difficulty method for 'Medium' difficulty
        recipe = Recipe.objects.create(
            name="Medium Recipe",
            cooking_time=5,
            ingredients="flour, sugar, eggs, milk",
            created_by=self.user
        )
        recipe.calculate_difficulty()
        self.assertEqual(recipe.difficulty, "Medium")

    def test_calculate_difficulty_intermediate(self):
        # Test the calculate_difficulty method for 'Intermediate' difficulty
        recipe = Recipe.objects.create(
            name="Intermediate Recipe",
            cooking_time=15,
            ingredients="flour, sugar",
            created_by=self.user
        )
        recipe.calculate_difficulty()
        self.assertEqual(recipe.difficulty, "Intermediate")

    def test_calculate_difficulty_hard(self):
        # Test the calculate_difficulty method for 'Hard' difficulty
        recipe = Recipe.objects.create(
            name="Hard Recipe",
            cooking_time=15,
            ingredients="flour, sugar, eggs, milk",
            created_by=self.user
        )
        recipe.calculate_difficulty()
        self.assertEqual(recipe.difficulty, "Hard")
