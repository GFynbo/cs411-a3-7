from django import forms

class RecipeSearchForm(forms.Form):
    query = forms.CharField(label='Your search', max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control form-control-dark w-100', 'placeholder' : 'Search'}))

class RecipeShowForm(forms.Form):
    recipe_id = forms.CharField()

class AddIngredientForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'avocado, etc'}))

class UpdateMyIngredient(forms.Form):
    id = forms.CharField()
    measurement = forms.CharField()
    amount = forms.DecimalField()

class FavoriteMyRecipe(forms.Form):
    recipe_id = forms.CharField()
    recipe_name = forms.CharField()

class UnfavoriteMyRecipe(forms.Form):
    recipe_id = forms.CharField()
    recipe_name = forms.CharField()
