from django.urls import path
from .views import home, RecipeListView, RecipeDetailView

app_name = 'recipes'

urlpatterns = [
    path('', home, name='home'),
    path('recipes/', RecipeListView.as_view(), name='recipe_list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
]