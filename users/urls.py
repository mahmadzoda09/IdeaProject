from django.urls import path
from .views import *


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path('users', all_users.as_view(), name='users'),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
]