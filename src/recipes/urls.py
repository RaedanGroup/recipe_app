from django.urls import path
from .views import home, RecipeListView, RecipeDetailView, LogoutView, search, submit_recipe

app_name = 'recipes'

urlpatterns = [
    path('', home, name='home'),
    path('recipes/', RecipeListView.as_view(), name='recipe_list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('search/', search, name='search'),
    path('submit-recipe/', submit_recipe, name='submit_recipe'),
]