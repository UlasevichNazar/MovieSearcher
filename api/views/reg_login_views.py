from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from api.serializers.reg_login.login import UserLoginSerializer
from api.serializers.reg_login.registration import RegisterSerializer


@extend_schema_view(
    create=extend_schema(
        summary="registration", tags=["Registration and Authentication"]
    ),
    post=extend_schema(
        summary="authentication", tags=["Registration and Authentication"]
    ),
)
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer
