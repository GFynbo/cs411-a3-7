from django.db import models
from django.contrib.auth.models import User

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
        return Ingredient.objects.filter(name=ingredient).exists()

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

class MiniRecipeManager(models.Manager):
    """ Manager for the MiniRecipe class """
    def total_mini_recipes():
        recipes = MiniRecipe.objects.all()
        return len(recipes)

    def get_mini_recipes():
        # gets all ingredients
        recipes = MiniRecipe.objects.all().order_by('name')
        return recipes

    def get_mini_recipe(recipe_id_name):
        # gets all ingredients
        if MiniRecipeManager.check_mini_recipe(recipe_id_name):
            return MiniRecipe.objects.get(recipe_id=recipe_id_name)
        else:
            return False

    def check_mini_recipe(recipe_id_name):
        return MiniRecipe.objects.filter(recipe_id=recipe_id_name).exists()

    def add_mini_recipe(recipe_name, recipe_id_name, recipe_img_url):
        if MiniRecipeManager.check_mini_recipe(recipe_id_name):
            print("MiniRecipe already exists: " + (recipe_id_name))
        else:
            new_recipe = MiniRecipe(name=recipe_name, recipe_id=recipe_id_name, img_url=recipe_img_url)
            new_recipe.save()

class MiniRecipe(models.Model):
    """ A class containing a recipe name, ID and URL for picture """
    name = models.CharField(max_length=100)
    recipe_id = models.CharField(max_length=200)
    img_url = models.CharField(max_length=350)

class MyIngredientManager(models.Manager):
    """ manager for the myingredient model """
    def total_myingredients():
        recipes = MyIngredient.objects.all()
        return len(recipes)

    def get_myingredients(user):
        # gets all ingredients
        try:
            curr_user = User.objects.get(pk=user)
            recipes = MyIngredient.objects.filter(user=curr_user)
            return recipes
        except:
            return []

    def check_myingredient(user, recipe_id_name):
        try:
            curr_user = User.objects.get(pk=user)
            curr_recp = Ingredient.objects.get(name=ingredient_name)
            return MyIngredient.objects.filter(user=curr_user, ingredient=curr_recp).exists()
        except:
            return False

    def add_myingredient(user, ingredient_name):
        try:
            if not MyIngredientManager.check_myingredient(user, ingredient_name):
                curr_user = User.objects.get(pk=user)
                print(curr_user)
                curr_ing = Ingredient.objects.get(name=ingredient_name)
                print(curr_ing)
                new_mying = MyIngredient(user=curr_user, ingredient=curr_ing)
                new_mying.save()
        except:
            print("failed adding ingredient")

class MyIngredient(models.Model):
    """ model to represent the ingredients for an individual """
    user = models.ForeignKey(User, related_name="myingredient_user")
    ingredient = models.ForeignKey(Ingredient, related_name="myingredient_ing")
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    measurement = models.CharField(max_length=20, default="cups")
