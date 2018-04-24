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
        ingredients = Ingredient.objects.all().order_by('name')
        return ingredients

    def check_ingredient(ingredient):
        return Ingredient.objects.get(name=ingredient)

    def add_ingredient(ingredient_name):
        try:
            Ingredient.objects.get(name=ingredient_name)
            print("Ingredient already exists: " + str(ingredient_name))
        except:
            new_ingredient = Ingredient(name=ingredient_name, category=ingredient_name)
            new_ingredient.save()

class Ingredient(models.Model):
    """ Ingredient is a unique model to describe and define ingredients """
    name = models.CharField(max_length=100, help_text="Enter the ingredient name (e.g. Salt or Onion)")
    category = models.CharField(max_length=100, default="None", help_text="Enter the ingredient category (e.g. Spice or Meat)")


# Create your models here.
class RecipeManager(models.Manager):
    """ Ingredient Manager is just a manager model to add, delete, and search
        for ingredients in the database.
    """
    def total_recipes():
        recipes = Recipe.objects.all()
        return len(recipes)

    def get_recipes():
        # gets all ingredients
        recipes = Recipe.objects.all().order_by('name')
        return recipes

    def check_recipe(recipe_name):
        return Recipe.objects.get(name=recipe_name)

    def add_recipe(recipe_name):
        try:
            Recipe.objects.get(name=recipe_name)
            print("Ingredient already exists: " + (recipe_name).encode('utf-8'))
        except:
            new_recipe = Recipe(name=recipe_name, category="None")
            new_recipe.save()

class Recipe(models.Model):
    """ Ingredient is a unique model to describe and define ingredients """
    name = models.CharField(max_length=100, help_text="Enter the ingredient name (e.g. Salt or Onion)")
    category = models.CharField(max_length=100, default="None", help_text="Enter the ingredient category (e.g. Spice or Meat)")
