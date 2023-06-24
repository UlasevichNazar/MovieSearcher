from django.contrib.auth import logout, login
from django.shortcuts import render, redirect


from .forms import RegisterUserForm, LoginUserForm
from django.views.generic import ListView, DetailView, CreateView

from django.contrib.auth.views import LoginView







class register(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')




class LoginUser(LoginView):
    from_class = LoginUserForm
    template_name = 'login/login.html'



def logout_user(request):
    logout(request)
    return redirect('login')








