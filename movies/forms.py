from django import forms
from django.contrib.auth import get_user_model
from django_select2.forms import Select2MultipleWidget

from .models import Actor
from .models import Category
from .models import Director
from .models import Genre
from .models import Movie
from .models import Movie_image
from .models import Raiting
from .models import Review
from user.models import Role


class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["text"]


class RaitingForm(forms.ModelForm):
    class Meta:
        model = Raiting
        fields = ["rating"]


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
        fields = "__all__"


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
        fields = "__all__"


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
        fields = "__all__"


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
        fields = "__all__"


class MovieImageForm(forms.ModelForm):
    name = forms.CharField(
        label="Название", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    image = forms.ImageField(label="Фотография", required=False)
    movie = forms.ModelChoiceField(
        label="Фильм",
        queryset=Movie.objects.all(),
        empty_label="Фильм",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Movie_image
        fields = "__all__"


class MovieForm(forms.ModelForm):
    status = forms.ChoiceField(
        label="Статус",
        choices=Movie.Status.choices,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    publish = forms.DateTimeField(
        label="Публикация",
        widget=forms.DateTimeInput(attrs={"class": "form-control"}),
    )
    slug = forms.CharField(
        label="URL", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    fees_in_the_world = forms.IntegerField(
        label="Сборы в мире",
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    budget = forms.IntegerField(
        label="Бюджет фильма",
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    year = forms.IntegerField(
        label="Год выпуска",
        min_value=1900,
        max_value=2023,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    actors = forms.ModelMultipleChoiceField(
        queryset=Actor.objects.all(),
        widget=Select2MultipleWidget(attrs={"style": "width: 100%;height: 200px;"}),
        label="Актеры",
    )

    director = forms.ModelChoiceField(
        label="Режиссер",
        queryset=Director.objects.all(),
        empty_label="Режиссер",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    genre = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=Select2MultipleWidget(attrs={"style": "width: 100%;height: 200px;"}),
        label="Жанры",
    )

    category = forms.ModelChoiceField(
        label="Категория",
        queryset=Category.objects.all(),
        empty_label="Категория",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    description = forms.CharField(
        label="Описание", widget=forms.Textarea(attrs={"class": "form-control"})
    )

    title = forms.CharField(
        label="Название", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    country = forms.CharField(
        label="Страна производства",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Movie
        fields = "__all__"


class GetUserForm(forms.Form):
    username = forms.ModelChoiceField(
        label="Имя пользователя",
        queryset=get_user_model().objects.all(),
        empty_label="Имя пользователя",
        widget=forms.Select(attrs={"class": "form-control"}),
    )


# Форма для обновления статуса
class UpdateStatusForm(forms.ModelForm):
    status = forms.ChoiceField(
        label="Статус",
        choices=[
            (role.value, role.value) for role in Role
        ],  # Используем значение вместо имени
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = get_user_model()
        fields = ("status",)


class GetActorForm(forms.ModelForm):
    name = forms.CharField(
        label="Имя актера",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        model = Actor
        fields = ("name",)


class GetCategoryForm(forms.ModelForm):
    name = forms.CharField(
        label="Название категории",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        model = Category
        fields = ("name",)


class GetGenreForm(forms.ModelForm):
    name = forms.CharField(
        label="Название жанра",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        model = Genre
        fields = ("name",)


class GetDirectorForm(forms.ModelForm):
    name = forms.CharField(
        label="Имя режиссера",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        model = Director
        fields = ("name",)


class GetMovieForm(forms.ModelForm):
    title = forms.CharField(
        label="Название фильма",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        model = Movie
        fields = ("title",)


class DeleteUserForm(forms.Form):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = get_user_model()
        fields = ("username",)


class EditReviewForm(forms.ModelForm):
    text = forms.CharField(
        label="Комментарий",
        widget=forms.Textarea(attrs={"rows": 5, "cols": 40, "class": "form-control"}),
    )

    class Meta:
        model = Review
        fields = ("text",)
