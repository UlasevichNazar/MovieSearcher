from django import forms
from django.contrib.auth.forms import UserChangeForm

from user.models import User


class UserProfileForm(UserChangeForm):
    username = forms.CharField(
        label="Логин", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.CharField(
        label="Eamil", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    birthday = forms.CharField(
        label="Дата рождения", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    bio = forms.CharField(
        label="О себе",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    profile_pic = forms.ImageField(label="Фото профиля", required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "birthday",
            "free_mailing_list",
            "bio",
            "profile_pic",
        )
