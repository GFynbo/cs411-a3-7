from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from django.conf import settings

from .forms import RecipeSearchForm

import requests


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RecipeSearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            query = form.cleaned_data['query']
            response = requests.get('http://api.yummly.com/v1/api/recipes?&_app_id=09a314ee&_app_key=397b29968b12c73d65e17a07deff9f3e&q=' + query)
            pantrydata = response.json()
            return render(
                request,
                'index.html',
                {'query': pantrydata['criteria']['q'], 'matches': pantrydata['matches']}
            )
    # if a GET (or any other method) we'll create a blank form
    else:
        form = RecipeSearchForm()

    return render(request, 'index.html', {'form': form})
