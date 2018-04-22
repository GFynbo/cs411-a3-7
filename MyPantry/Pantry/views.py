from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from django.conf import settings

from .forms import RecipeSearchForm
from .models import IngredientManager

import requests

def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RecipeSearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            query = form.cleaned_data['query']
            query_string = 'http://api.yummly.com/v1/api/recipes?&_app_id=' + str(settings.APP_ID) + '&_app_key=' + str(settings.APP_KEY) + '&q=' + query
            response = requests.get(query_string)
            pantrydata = response.json()
            for recipe in pantrydata['matches']:
                for ingredient in recipe['ingredients']:
                    print(ingredient)
                    IngredientManager.add_ingredient(ingredient)

            print(IngredientManager.total_ingredients())
            return render(
                request,
                'index.html',
                {'query': pantrydata['criteria']['q'], 'matches': pantrydata['matches']}
            )
    # if a GET (or any other method) we'll create a blank form
    else:
        form = RecipeSearchForm()

    return render(request, 'index.html', {'form': form})
