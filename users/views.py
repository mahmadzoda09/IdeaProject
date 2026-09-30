from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView , ListView ,DetailView

from .forms import RegisterForm
from .models import User


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")

class UserLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True
    next_page = reverse_lazy("users")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")

class all_users(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'

class UserDetailView(DetailView):
    model = User
    template_name = "users/user_detail.html"
    context_object_name = "user"