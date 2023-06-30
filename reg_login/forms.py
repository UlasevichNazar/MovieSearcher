from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label="Логин", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    free_mailing_list = forms.CharField(
        label="Рассылка",
        required=False,
        widget=forms.CheckboxInput(attrs={"class:": "form-controlt"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "free_mailing_list")


class LoginUserForm(AuthenticationForm):
    username = (
        forms.CharField(
            label="Логин", widget=forms.TextInput(attrs={"class": "form-control"})
        ),
    )
    password = (
        forms.CharField(
            label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"})
        ),
    )
