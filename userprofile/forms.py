from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User, Profile


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    birthday = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # free_mailing_list = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'form-check-label'}))
    # paid_mailing_list = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(label='О себе', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_pic = forms.ImageField(label='Фото профиля', required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'birthday', 'free_mailing_list', 'paid_mailing_list', 'bio', 'profile_pic')
