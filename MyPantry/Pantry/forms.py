from django import forms

class RecipeSearchForm(forms.Form):
    query = forms.CharField(label='Your search', max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control form-control-dark w-100', 'placeholder' : 'Search'}))
