from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView as AuthLogoutView
from .forms import RecipeSearchForm


# Create your views here.
def home(request):
    return render(request, 'recipes/recipes_home.html')

def search(request):
    form = RecipeSearchForm(request.POST or None)

    if request.method == 'POST':
            recipe_name = request.POST.get('recipe_name')
            chart_type = request.POST.get('chart_type')
            print (recipe_name, chart_type)

            qs = Recipe.objects.all()
            print(qs)

            qs = qs.filter(name__icontains=recipe_name)
            print(qs)

            print(qs.values())

    context = {
        'form': form,
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