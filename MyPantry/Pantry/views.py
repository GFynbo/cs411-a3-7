from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from django.conf import settings

from .forms import AddIngredientForm, RecipeSearchForm, RecipeShowForm, UpdateMyIngredient
from .models import IngredientManager, MiniRecipeManager, MyIngredientManager


from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import requests


@login_required
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

@login_required
def pantry(request):
    if request.method == 'POST':
        form2 = AddIngredientForm(request.POST)
        form = RecipeSearchForm()
        if form2.is_valid():
            name = form2.cleaned_data['name']
            user_pk = request.user.pk
            if IngredientManager.check_ingredient(name):
                print("Add myingredient: " + str(name))
                MyIngredientManager.add_myingredient(user_pk, name)
            else:
                print("No ingredient found.")
            return render(request, 'pantry.html', {'form': form, 'form2':form2, 'matches': MyIngredientManager.get_myingredients(user_pk)})
    else:
        form2 = AddIngredientForm()
    form = RecipeSearchForm()
    form3 = UpdateMyIngredient()
    user_pk = request.user.pk
    return render(request, 'pantry.html', {'form': form, 'form2':form2, 'form3':form3, 'matches': MyIngredientManager.get_myingredients(user_pk)})

@login_required
def ingredients(request):
    form = RecipeSearchForm()
    return render(request, 'ingredients.html', {'form': form, 'ingredients': IngredientManager.get_ingredients(), 'total_ingredients': IngredientManager.total_ingredients()})

def login(request):
    form = RecipeSearchForm()
    return render(request, 'login.html', {'form': form, 'ingredients': IngredientManager.get_ingredients(), 'total_ingredients': IngredientManager.total_ingredients()})

@login_required
def recipes(request):
    form = RecipeSearchForm()
    return render(request, 'recipes.html', {'form': form, 'recipeList': MiniRecipeManager.get_mini_recipes()})

@login_required
def myrecipes(request):
    form = RecipeSearchForm()
    return render(request, 'myrecipes.html', {'form': form, })

@login_required
def show_recipe(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RecipeShowForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            recipe = form.cleaned_data['recipe_id']
            # get yummly recipe
            query_string = 'http://api.yummly.com/v1/api/recipe/' + recipe + '?&_app_id=' + str(settings.APP_ID) + '&_app_key=' + str(settings.APP_KEY)
            response = requests.get(query_string)
            pantrydata = response.json()
            form = RecipeSearchForm()

            # get yelp related restaurants (BOSTON ONLY)
            url = "https://api.yelp.com/v3/businesses/search"
            results = ""
            try:
                results = pantrydata['name']
                print(results)
            except:
                results = ""

            querystring = {"term":results,"latitude":"42.3605","longitude":"-71.057083"}

            headers = {
                'Authorization': "Bearer P8-sXpWc-rQuZzafffsT9-0aHs99DWGfjAuSNutjp05fqnVbPTdUNoYp9MhWSqQucma9S3qaa3jRaT6AjASBujMoU5wEW6JqqCTeh834slXvwMxffjE97bG1jHXmWnYx",
                'Cache-Control': "no-cache",
                'Postman-Token': "0b8dfcdd-851d-7243-07c9-f755f8fd7896"
                }

            response = requests.request("GET", url, headers=headers, params=querystring)
            businesses = response.json()

            return render(
                request,
                'show_recipe.html',
                {'recipe': pantrydata, 'big_image_url':pantrydata['images'][0]['hostedLargeUrl'], 'businesses':businesses['businesses'], 'form': form}
            )
    # if a GET (or any other method) we'll create a blank form
    else:
        form = RecipeSearchForm()
    return render(request, 'show_recipe.html', {'form': form, 'recipeList': MiniRecipeManager.get_mini_recipes()})
