# models.py
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

class Recipe(models.Model):
    name = models.CharField(max_length=50)
    cooking_time = models.IntegerField()
    ingredients = models.TextField()
    pic = models.ImageField(upload_to='recipe_pics', default='no_picture.jpg')
    difficulty = models.CharField(max_length=20, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # ingredients as list
    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        return self.ingredients.split(", ")

    # calculate difficulty level
    def calculate_difficulty(self):
        num_ingredients = len(self.return_ingredients_as_list())
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"

    # Override the save method to calculate difficulty before saving a new recipe via the form
    def save(self, *args, **kwargs):
        self.calculate_difficulty()
        super().save(*args, **kwargs)

    # string representation of the model
    def __str__(self):
        return self.name
    
