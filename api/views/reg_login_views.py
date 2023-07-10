from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from api.serializers.reg_login_serializers.login import UserLoginSerializer
from api.serializers.reg_login_serializers.registration import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer
