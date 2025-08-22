from django import forms
from .models import JobPost,Application

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        #fields = '__all__'
        exclude = ['author','status']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        #fields = '__all__'
        exclude = ['author','JobPost','status']