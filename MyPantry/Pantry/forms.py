from django import forms

class RecipeSearchForm(forms.Form):
    query = forms.CharField(label='Your search', max_length=100)
