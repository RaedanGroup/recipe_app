# views.py
from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, DetailView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView as AuthLogoutView
from .forms import RecipeSearchForm
import pandas as pd
from .utils import get_chart, rename_columns

def home(request):
    return render(request, 'recipes/recipes_home.html')

def search(request):
    form = RecipeSearchForm(request.POST or None)
    recipes_df = None
    chart = None

    if 'show_all' in request.GET:
        recipe_name = ''
        chart_type = 'pie-chart'
        # Redirect to remove 'show_all' from the URL
        return redirect(request.path)
    else:
        recipe_name = request.POST.get('recipe_name', '')
        chart_type = request.POST.get('chart_type', 'pie-chart')

    qs = Recipe.objects.filter(name__icontains=recipe_name)
    if qs.exists():
        recipes_df = pd.DataFrame(qs.values('id', 'name', 'cooking_time', 'ingredients', 'difficulty'))
        chart = get_chart(chart_type, recipes_df, labels=recipes_df['name'].values)
        recipes_df['link'] = recipes_df['id'].apply(lambda x: f'<a href="{reverse("recipes:recipe_detail", kwargs={"pk": x})}">Details</a>')

        # Drop the 'id' column from the DataFrame
        recipes_df = recipes_df.drop(columns=['id'])

        # Rename the columns
        recipes_df = rename_columns(recipes_df)

        recipes_df = recipes_df.to_html(classes='table table-striped', escape=False, index=False)

    context = {
        'form': form,
        'recipes_df': recipes_df,
        'chart': chart
    }

    return render(request, 'recipes/recipes_search.html', context)

class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'
    context_object_name = 'recipes'

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

class LogoutView(AuthLogoutView):
    template_name = 'recipes/success.html'
