# tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe
from django.core.exceptions import ValidationError

class RecipeModelTests(TestCase):
    def setUp(self):
        # Create a user for the tests
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Create recipes for testing
        self.recipe1 = Recipe.objects.create(
            name="Recipe One",
            cooking_time=10,
            ingredients="flour, sugar, eggs",
            created_by=self.user
        )
        self.recipe2 = Recipe.objects.create(
            name="Recipe Two",
            cooking_time=20,
            ingredients="flour, sugar, eggs, milk",
            created_by=self.user
        )

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

    def test_recipe_list_view(self):
        # Test the recipe list view
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('recipes:recipe_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_list.html')
        self.assertContains(response, self.recipe1.name)
        self.assertContains(response, self.recipe2.name)

    def test_recipe_detail_view(self):
        # Test the recipe 1 detail view
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('recipes:recipe_detail', kwargs={'pk': self.recipe1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')
        self.assertContains(response, self.recipe1.name)
        self.assertContains(response, self.recipe1.cooking_time)
        self.assertContains(response, self.recipe1.difficulty)
        
        # Check individual Rec1 ingredients
        ingredients_list = self.recipe1.return_ingredients_as_list()
        for ingredient in ingredients_list:
            self.assertContains(response, ingredient)

        # Test the recipe 2 detail view
        response = self.client.get(reverse('recipes:recipe_detail', kwargs={'pk': self.recipe2.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')
        self.assertContains(response, self.recipe2.name)
        self.assertContains(response, self.recipe2.cooking_time)
        self.assertContains(response, self.recipe2.difficulty)
        
        # Check individual Rec2 ingredients
        ingredients_list = self.recipe2.return_ingredients_as_list()
        for ingredient in ingredients_list:
            self.assertContains(response, ingredient)

    def test_field_lengths(self):
        recipe = Recipe(
            name="A" * 51,  # This should be 50 characters or less
            cooking_time=15,
            ingredients="flour, sugar, eggs",
            created_by=self.user
        )
        with self.assertRaises(ValidationError):
            recipe.full_clean()  # This will validate the model

        recipe.name = "A" * 50  # Adjust to valid length
        try:
            recipe.full_clean()  # Validate again
        except ValidationError:
            self.fail("ValidationError raised with valid name length")


    def test_pagination(self):
        # Ensure the test user is logged in
        self.client.login(username='testuser', password='12345')

        # Create more recipes if necessary to test pagination
        for i in range(1, 11):  # Adjust the range as needed
            Recipe.objects.create(
                name=f"Recipe {i}",
                cooking_time=10,
                ingredients="flour, sugar, eggs",
                created_by=self.user
            )

        response = self.client.get(reverse('recipes:recipe_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recipe 1')
        self.assertContains(response, 'Recipe 10')
        self.assertTemplateUsed(response, 'recipes/recipe_list.html')


    def test_login_protection(self):
        # Test login protection for list view
        response = self.client.get(reverse('recipes:recipe_list'))
        self.assertNotEqual(response.status_code, 200)  # Should redirect to login page
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('recipes:recipe_list')}")
        
        # Test login protection for detail view
        response = self.client.get(reverse('recipes:recipe_detail', kwargs={'pk': self.recipe1.pk}))
        self.assertNotEqual(response.status_code, 200)  # Should redirect to login page
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('recipes:recipe_detail', kwargs={'pk': self.recipe1.pk})}")
