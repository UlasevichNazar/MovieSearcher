from django.urls import path

from .views import LoginUser
from .views import logout_user
from .views import Register


urlpatterns = [
    path("registration/", Register.as_view(), name="register"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
]
