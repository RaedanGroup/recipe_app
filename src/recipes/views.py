from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView as AuthLogoutView
from .forms import RecipeSearchForm
import pandas as pd
from .utils import get_chart

# Create your views here.
def home(request):
    return render(request, 'recipes/recipes_home.html')

def search(request):
    form = RecipeSearchForm(request.POST or None)
    recipes_df = None
    chart = None

    if request.method == 'POST':
            recipe_name = request.POST.get('recipe_name')
            chart_type = request.POST.get('chart_type')

            qs = Recipe.objects.filter(name__icontains=recipe_name)
            if qs:
                recipes_df = pd.DataFrame(qs.values())
                chart = get_chart(chart_type, recipes_df, labels=recipes_df['name'].values)
                recipes_df = recipes_df.to_html()

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