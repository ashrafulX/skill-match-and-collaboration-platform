from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm ,UserChangeForm
from django import forms

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
    

class show_profile(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
    def __init__(self, *args, **kwargs):
        super(show_profile, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True  
            
class EditProfile(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id':'required', 'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id':'required', 'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'id':'required', 'class': 'form-control'}))
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    