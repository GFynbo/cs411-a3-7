from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from django.conf import settings

from .forms import RecipeSearchForm
from .models import IngredientManager, MiniRecipeManager

import requests

def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RecipeSearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            query = form.cleaned_data['query']
            query_string = 'http://api.yummly.com/v1/api/recipes?&_app_id=' + str(settings.APP_ID) + '&_app_key=' + str(settings.APP_KEY) + '&q=' + query + "&requirePictures=true"
            response = requests.get(query_string)
            pantrydata = response.json()
            for recipe in pantrydata['matches']:
                MiniRecipeManager.add_mini_recipe(recipe['recipeName'], recipe['id'], recipe['imageUrlsBySize']['90'])
                for ingredient in recipe['ingredients']:
                    IngredientManager.add_ingredient(ingredient)
            print(IngredientManager.total_ingredients())
            form = RecipeSearchForm()
            return render(
                request,
                'index.html',
                {'query': pantrydata['criteria']['q'], 'matches': pantrydata['matches'], 'form': form}
            )
    # if a GET (or any other method) we'll create a blank form
    else:
        form = RecipeSearchForm()

    return render(request, 'index.html', {'form': form})

def ingredients(request):
    return render(request, 'ingredients.html', {'ingredients': IngredientManager.get_ingredients(), 'total_ingredients': IngredientManager.total_ingredients()})

def login(request):
    return render(request, 'login.html', {'ingredients': IngredientManager.get_ingredients(), 'total_ingredients': IngredientManager.total_ingredients()})

def recipes(request):
    return render(request, 'recipes.html', {'recipeList': MiniRecipeManager.get_mini_recipes()})

def myrecipes(request):
    return render(request, 'myrecipes.html', {})
