from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from django.conf import settings

import requests


def index(request):
    response = requests.get('http://api.yummly.com/v1/api/recipes?&_app_id=09a314ee&_app_key=397b29968b12c73d65e17a07deff9f3e&q=salt&excludedIngredient=pepper')
    pantrydata = response.json()
    return render(
        request,
        'index.html',
        {
        'matches': pantrydata['matches']
    })
