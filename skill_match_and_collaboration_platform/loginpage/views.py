from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import RegisterForm
from django.contrib import messages
from django.urls import reverse_lazy

class SignupView(FormView):
    template_name = 'signup.html'
    form_class = RegisterForm
    success_url = reverse_lazy('homepage')  # Redirect after successful signup

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Account created successfully')
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)

    

#for longin logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView

class LoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('homepage')  # Redirect after login

    def form_valid(self, form):
        name = form.cleaned_data['username']
        userpass = form.cleaned_data['password']
        user = authenticate(username=name, password=userpass)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        return self.form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)

    
from django.views.generic import TemplateView

class ProfileView(TemplateView):
    template_name = 'profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


from django.contrib.auth import logout
def Logout(request):
    logout(request)
    return redirect('homepage')

#for changing passwoard
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from django.contrib.auth import update_session_auth_hash

def changePass(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form = PasswordChangeForm(user=request.user, data = request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('profile')
        else:
            form = PasswordChangeForm(user=request.user)
        return render(request,'changePass.html', {'form':form})
    else:
        return redirect('homepage')
    
def changePass2(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form = SetPasswordForm(user=request.user, data = request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('profile')
        else:
            form = SetPasswordForm(user=request.user)
        return render(request,'changePass2.html', {'form':form})
    else:
        return redirect('loginpage')

#for showing frofile impormation
from django.views.generic.edit import UpdateView
from .forms import show_profile

class ShowProfileView(UpdateView):
    form_class = show_profile
    template_name = 'profileImpo.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user  # Show profile of the logged-in user

    
# For Editing your profile
from .forms import EditProfile

class EditProfileView(UpdateView):
    form_class = EditProfile
    template_name = 'editprofile.html'
    success_url = reverse_lazy('showProfile')

    def get_object(self, queryset=None):
        return self.request.user  # Edit profile of the logged-in user


from django.views.generic.list import ListView
from jobPost.models import JobPost

class UserPostView(ListView):
    model = JobPost
    template_name = 'userpost.html'
    context_object_name = 'data'

    def get_queryset(self):
        return JobPost.objects.filter(author=self.request.user)
 

from django.contrib.auth.decorators import login_required 

@login_required
def delete_profile(request):
    if request.method == "POST":
        user = request.user
        user.delete()  # Delete the user instance
        # messages.success(request, "Your profile has been deleted successfully.")
        return redirect('homepage')  # Redirect to the homepage or another appropriate page

    return render(request, 'delete_profile.html')