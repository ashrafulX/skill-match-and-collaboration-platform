from django import forms
from .models import Categories

class CatForm(forms.ModelForm):
    class Meta:
        model = Categories
        exclude = ['slug']
        