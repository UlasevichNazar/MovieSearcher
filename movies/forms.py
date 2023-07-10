from django import forms
from django.forms import SelectMultiple

from .models import Review, Raiting, Movie, Category, Genre, Director, Actor


class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["text"]


class RaitingForm(forms.ModelForm):
    class Meta:
        model = Raiting
        fields = ['rating']


class MovieForm(forms.ModelForm):
    # category = forms.ModelMultipleChoiceField(
    #     label="Категории",
    #     queryset=Category.objects.all(),
    #     widget=SelectMultiple(attrs={"class": "form-control"}),
    #     required=False,
    # )
    #
    # genre = forms.ModelMultipleChoiceField(
    #     label="Жанры",
    #     queryset=Genre.objects.all(),
    #     widget=SelectMultiple(attrs={"class": "form-control"}),
    #     required=False,
    # )
    # director = forms.ModelMultipleChoiceField(
    #     label="Режиссеры",
    #     queryset=Director.objects.all(),
    #     widget=SelectMultiple(attrs={"class": "form-control"}),
    #     required=False,
    # )
    #
    # actors = forms.ModelMultipleChoiceField(
    #     label="Актеры",
    #     queryset=Actor.objects.all(),
    #     widget=SelectMultiple(attrs={"class": "form-control"}),
    #     required=False,
    # )

    description = forms.CharField(
        label="Описание", widget=forms.Textarea(attrs={"class": "form-control"})
    )

    title = forms.CharField(
        label="Название", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    country = forms.CharField(
        label="Страна производства", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Movie
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    description = forms.CharField(
        label="Описание", widget=forms.Textarea(attrs={"class": "form-control"})
    )
    name = forms.CharField(
        label="Название", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    url = forms.CharField(
        label="Ссылка", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Category
        fields = '__all__'


class GenreForm(forms.ModelForm):
    description = forms.CharField(
        label="Описание", widget=forms.Textarea(attrs={"class": "form-control"})
    )
    name = forms.CharField(
        label="Название", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    slug = forms.CharField(
        label="Ссылка", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Genre
        fields = '__all__'


class DirectorForm(forms.ModelForm):
    description = forms.CharField(
        label="Описание", widget=forms.Textarea(attrs={"class": "form-control"})
    )
    name = forms.CharField(
        label="Имя", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    image = forms.ImageField(label="Фотография", required=False)

    class Meta:
        model = Director
        fields = '__all__'


class ActorForm(forms.ModelForm):
    description = forms.CharField(
        label="Описание", widget=forms.Textarea(attrs={"class": "form-control"})
    )
    name = forms.CharField(
        label="Имя", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    image = forms.ImageField(label="Фотография", required=False)

    class Meta:
        model = Actor
        fields = '__all__'
