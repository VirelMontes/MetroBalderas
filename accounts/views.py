from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm

# from .forms import UserForm, AddressForm
# from .models import User, Address

# class SignupView(FormView):
#     form_class = UserForm
#     success_url = reverse_lazy('http://127.0.0.1:8000/accounts/login/')
#     template_name = 'signup.html'

#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.is_active = False
#         user.save()

#         return HttpResponseRedirect('/')

# class LoginView(LoginView):
#     template_name = 'login.html'

# def logout(request):
#     logout_url = reverse_lazy('login')
#     return LogoutView.as_view(next_page=logout_url)(request)

class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm


def sign_in(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('posts')
        
        form = LoginForm()
        return render(request,'login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Hi {username.title()}, welcome back!')
                return redirect('http://127.0.0.1:8000/accounts/profile/')
        
        # either form not valid or user is not authenticated
        messages.error(request,f'Invalid username or password')
        return render(request,'login.html',{'form': form})

def sign_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('login')     

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'signup.html', {'form': form})    
   
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'signup.html', {'form': form})
