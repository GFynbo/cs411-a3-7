from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('my_pantry', views.pantry, name='pantry'),
    url('show_recipe', views.show_recipe, name='show_recipe'),
    url('login', views.login, name='login'),
    url('ingredients', views.ingredients, name='ingredients'),
    url('my_recipes', views.myrecipes, name='myrecipes'),
    url('recipes', views.recipes, name='recipes'),
]
