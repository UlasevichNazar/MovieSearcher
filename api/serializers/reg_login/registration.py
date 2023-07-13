from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from send_mail.tasks import send_email_per
from userprofile.models import Profile

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    email = serializers.CharField(required=True)
    username = serializers.CharField(required=True, max_length=150)
    free_mailing_list = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password", "free_mailing_list")

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("This email address is already registered.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        free_mailing_list = validated_data.pop("free_mailing_list", False)
        user = User.objects.create_user(password=password, **validated_data)
        user.free_mailing_list = free_mailing_list
        if user.free_mailing_list == True:
            send_email_per.delay()
        if user is not None:
            Profile.objects.create(user=user)
        user.save()
        return user
