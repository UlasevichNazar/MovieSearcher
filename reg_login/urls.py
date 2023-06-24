from django.urls import path
from .views import register, LoginUser, logout_user



urlpatterns = [
    path('registration/', register.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),

]