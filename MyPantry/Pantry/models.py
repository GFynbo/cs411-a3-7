from django.db import models

# Create your models here.
class IngredientManager(models.Manager):
    """ Ingredient Manager is just a manager model to add, delete, and search
        for ingredients in the database.
    """
    def total_ingredients():
        ingredients = Ingredient.objects.all()
        return len(ingredients)

    def get_ingredients():
        # gets all ingredients
        ingredients = Ingredient.objects.all()
        return ingredients

    def check_ingredient(ingredient):
        return Ingredient.objects.get(name=ingredient)

    def add_ingredient(ingredient_name):
        if check_ingredient(ingredient_name):
            new_ingredient = Ingredient(name=ingredient_name, category=ingredient_name)
            new_ingredient.save()
        else:
            print("Ingredient already exists")

class Ingredient(models.Model):
    """ Ingredient is a unique model to describe and define ingredients """
    name = models.CharField(max_length=100, help_text="Enter the ingredient name (e.g. Salt or Onion)")
    category = models.CharField(max_length=100, default="None", help_text="Enter the ingredient category (e.g. Spice or Meat)")
