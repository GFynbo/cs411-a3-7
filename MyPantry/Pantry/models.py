from django.db import models

# Create your models here.
class IngredientManager(models.Manager):
    """ Ingredient Manager is just a manager model to add, delete, and search
        for ingredients in the database.
    """
    def total_ingredients():
        ingredients = Ingredient.objects.all()
        return len(ingredients)

    def get_matches(user, deny=False):
        # get matches for the match page
        matches = Match.objects.filter(user=user, deny=deny)
        return matches

    def check_ingredient(ingredient):
        return Match.objects.filter(user=user, restaurant=restaurant)

    def add_ingredient(ingredient, restaurant, deny=False):
        new_match = Match(user=user, restaurant=restaurant, deny=deny)
        new_match.save()

class Ingredient(models.Model):
    """ Ingredient is a unique model to describe and define ingredients """
    name = models.CharField(max_length=100, help_text="Enter the ingredient name (e.g. Salt or Onion)")
    category = models.CharField(max_length=100, default="None", help_text="Enter the ingredient category (e.g. Spice or Meat)")
