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
    birthday = forms.DateField(
        label="Дата рождения",
        widget=forms.DateInput(
            attrs={"class": "form-control", "placeholder": "дд.мм.гггг"}
        ),
        input_formats=["%d.%m.%Y"],
    )
    bio = forms.CharField(
        label="О себе",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5, "cols": 50}),
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
