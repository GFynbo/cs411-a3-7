from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth import logout

from django.conf import settings

from .forms import AddIngredientForm, FavoriteMyRecipe, RecipeSearchForm, RecipeShowForm, UnfavoriteMyRecipe, UpdateMyIngredient
from .models import Ingredient, IngredientManager, MiniRecipe, MiniRecipeManager, MyRecipeManager, MyIngredient, MyIngredientManager


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
        form3 = UpdateMyIngredient()
        if form2.is_valid():
            name = form2.cleaned_data['name']
            user_pk = request.user.pk
            if IngredientManager.check_ingredient(name):
                print("Add myingredient: " + str(name))
                MyIngredientManager.add_myingredient(user_pk, name)
            else:
                print("No ingredient found.")
            return render(request, 'pantry.html', {'form': form, 'form2':form2, 'form3':form3, 'matches': MyIngredientManager.get_myingredients(user_pk)})
    form2 = AddIngredientForm()
    form = RecipeSearchForm()
    form3 = UpdateMyIngredient()
    user_pk = request.user.pk
    return render(request, 'pantry.html', {'form': form, 'form2':form2, 'form3':form3, 'matches': MyIngredientManager.get_myingredients(user_pk)})

@login_required
def update_ingredient(request):
    if request.method == 'POST':
        form = UpdateMyIngredient(request.POST)
        user_pk = request.user.pk
        if form.is_valid():
            amount = form.cleaned_data['amount']
            measurement = form.cleaned_data['measurement']
            id = form.cleaned_data['id']
            print(id)
            if MyIngredientManager.check_myingredient(user_pk, id):
                ing = MyIngredient.objects.get(user=request.user, ingredient=Ingredient.objects.get(name=id))
                ing.amount = amount
                ing.measurement = measurement
                ing.save()
                print(ing)
                return redirect("/pantry/my_pantry/")
        return redirect("/pantry/")
    else:
        return redirect("/pantry/")

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
    recipes = MyRecipeManager.get_myrecipes(user=request.user.pk)
    return render(request, 'myrecipes.html', {'form': form, 'myrecipes':recipes})

@login_required
def favorite(request):
    if request.method == 'POST':
        form = FavoriteMyRecipe(request.POST)
        user_pk = request.user.pk
        print(form.is_valid())
        if form.is_valid():
            id = form.cleaned_data['recipe_id']
            name = form.cleaned_data['recipe_name']
            if not MyRecipeManager.check_myrecipe(user=user_pk, recp_id=id):
                MyRecipeManager.add_myrecipe(user=user_pk, recp_id=id)
        return redirect("/pantry/my_recipes/")
    return redirect("/pantry/my_recipes/")

@login_required
def unfavorite(request):
    if request.method == 'POST':
        form = UnfavoriteMyRecipe(request.POST)
        user_pk = request.user.pk
        if form.is_valid():
            id = form.cleaned_data['recipe_id']
            print(id)
            name = form.cleaned_data['recipe_name']
            print(name)
            MyRecipeManager.delete_myrecipe(user=user_pk, recp_id=id)
        return redirect("/pantry/my_recipes/")
    return redirect("/pantry/my_recipes/")

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
            form_favorite = FavoriteMyRecipe()
            form_unfavorite = FavoriteMyRecipe()
            is_favorite = MyRecipeManager.check_myrecipe(user=request.user.pk, recp_id=recipe)
            # get yelp related restaurants (BOSTON ONLY)
            url = "https://api.yelp.com/v3/businesses/search"
            results = ""
            try:
                results = pantrydata['name']
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
                {'recipe': pantrydata, 'big_image_url':pantrydata['images'][0]['hostedLargeUrl'], 'businesses':businesses['businesses'], 'form': form, 'is_favorite':is_favorite, 'form_favorite':form_favorite, 'form_unfavorite':form_unfavorite}
            )
    # if a GET (or any other method) we'll create a blank form
    else:
        form = RecipeSearchForm()
    return render(request, 'show_recipe.html', {'form': form, 'recipeList': MiniRecipeManager.get_mini_recipes()})

@login_required
def logout_view(request):
    """ logout of the account """
    logout(request)
    return redirect("/pantry/")
