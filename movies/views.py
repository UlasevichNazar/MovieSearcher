from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import FormView

from . import models
from .forms import ActorForm
from .forms import AddReviewForm
from .forms import CategoryForm
from .forms import DirectorForm
from .forms import GenreForm
from .forms import GetUserForm
from .forms import MovieForm
from .forms import MovieImageForm
from .forms import RaitingForm
from .forms import UpdateStatusForm
from .models import Actor
from .models import Category
from .models import Director
from .models import Genre
from .models import Movie
from .models import Raiting
from .models import Review


class PoiskList:
    def get_genres(self):
        return Genre.objects.all()

    def get_category(self):
        return Category.objects.all()

    def get_years(self):
        return list(
            sorted(
                Movie.objects.filter(status=Movie.Status.PUBLISHED)
                .values_list("year", flat=True)
                .distinct()
            )
        )


# Список фильмов
class MovieList(PoiskList, generic.ListView):
    model = models.Movie
    queryset = model.objects.filter(status=model.Status.PUBLISHED)
    paginate_by = 4
    context_object_name = "movies"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.all()
        context["title"] = "Главная страница"
        return context

    def get_queryset(self):
        return self.queryset


class MovieDetail(PoiskList, generic.DetailView):
    model = Movie
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.object
        average_rating = Raiting.objects.filter(movie=movie).aggregate(
            avg_rating=Avg("rating")
        )["avg_rating"]
        rating_count = Raiting.objects.filter(movie=movie).count()
        context["rating_count"] = rating_count
        context["average_rating"] = average_rating
        context["movies"] = self.get_queryset().distinct()
        context["categories"] = Category.objects.all()

        user = self.request.user
        if not user.is_anonymous:
            rating = Raiting.objects.filter(user=user, movie=movie).first()
            if rating:
                context["rating_form"] = RaitingForm(instance=rating)
                context["can_edit_rating"] = True
                context["rating"] = rating.rating
                context["rating_id"] = rating.id
            else:
                context["rating_form"] = RaitingForm()

        return context

    def post(self, request, *args, **kwargs):
        movie = self.get_object()
        user = request.user
        print(user)
        rating = Raiting.objects.filter(user=user, movie=movie).first()

        if rating:
            rating.delete()
            return redirect("movie_detail", slug=movie.slug)
        form = RaitingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = user
            rating.movie = movie
            print(rating)
            rating.save()

        return redirect("movie_detail", slug=movie.slug)


class ActorView(PoiskList, DetailView):
    model = Actor
    template_name = "persons/actors.html"
    slug_field = "name"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.all()
        return context


class DirectorView(PoiskList, DetailView):
    model = Director
    template_name = "persons/directors.html"
    slug_field = "name"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.all()
        context["director_name"] = self.object.name
        return context


class AddReview(FormView):
    template_name = "movies/movie_detail.html"
    form_class = AddReviewForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.movie = Movie.objects.get(id=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        review = form.save(commit=False)
        review.user = self.request.user
        review.movie = self.movie
        review.save()
        return redirect(self.movie.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movie"] = self.movie
        return context


@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review_movie = review.movie
    if review.user == request.user:
        review.delete()
    return redirect(review_movie.get_absolute_url())


class FilterMovies(PoiskList, generic.ListView):
    def get_queryset(self):
        queryset = Movie.objects.filter(status=Movie.Status.PUBLISHED)
        if "category" in self.request.GET:
            queryset = queryset.filter(
                category__in=self.request.GET.getlist("category")
            )
        if "genre" in self.request.GET and self.request.GET.getlist("genre"):
            queryset = queryset.filter(genre__in=self.request.GET.getlist("genre"))
        if "year" in self.request.GET:
            queryset = queryset.filter(year__in=self.request.GET.getlist("year"))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["movies"] = self.get_queryset().distinct()
        context["categories"] = Category.objects.all()
        context["year"] = "".join([x for x in self.request.GET.getlist("year")])
        context["genre"] = "".join([x for x in self.request.GET.getlist("genre")])
        context["category"] = "".join([x for x in self.request.GET.getlist("category")])
        context["title"] = "Поиск фильма"
        return context


class Search(PoiskList, generic.ListView):
    def get_queryset(self):
        return Movie.objects.filter(title__iregex=self.request.GET.get("s"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        movies = self.get_queryset().distinct()
        context["s"] = f'q={self.request.GET.get("s")}&'
        context["movies"] = movies
        context["no_results"] = (
                len(movies) == 0
        )  # Добавляем переменную для проверки наличия результатов
        context["categories"] = Category.objects.all()

        return context


def add_movie(request):
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()  # Сохраняем фильм
            return redirect(
                "movie_detail", slug=movie.slug
            )  # Перенаправляем на страницу деталей фильма

    else:
        form = MovieForm()
    return render(
        request,
        "movies/add_movie.html",
        {"form": form, "categories": Category.objects.all(), "title": "Добавить фильм"},
    )


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "movies/add_buttons.html")
    else:
        form = CategoryForm()

    return render(
        request,
        "movies/add_category.html",
        {
            "form": form,
            "categories": Category.objects.all(),
            "title": "Добавить категорию",
        },
    )


def add_genre(request):
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "movies/add_buttons.html")
    else:
        form = GenreForm()

    return render(
        request,
        "movies/add_genre.html",
        {"form": form, "categories": Category.objects.all(), "title": "Добавить жанр"},
    )


def add_director(request):
    if request.method == "POST":

        form = DirectorForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return render(request, "movies/add_buttons.html")
        else:
            form = DirectorForm()

        return render(
            request,
            "movies/add_director.html",
            {
                "form": form,
                "categories": Category.objects.all(),
                "title": "Добавить режиссера",
            },
        )


def add_actor(request):
    if request.method == "POST":
        form = ActorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "movies/add_buttons.html")
    else:
        form = ActorForm()

    return render(
        request,
        "movies/add_actor.html",
        {
            "form": form,
            "categories": Category.objects.all(),
            "title": "Добавить актера",
        },
    )


def category_buttons(request):
    categories = Category.objects.all()
    return render(request, "movies/category_buttons.html", {"categories": categories, "title": "Категории"})


def add_movie_images(request):
    if request.method == "POST":
        form = MovieImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "movies/add_buttons.html")
    else:
        form = MovieImageForm()
    return render(
        request,
        "movies/add_movie_images.html",
        {
            "form": form,
            "categories": Category.objects.all(),
            "title": "Добавить изображение",
        },
    )


def add_buttons(request):
    return render(
        request,
        "movies/add_buttons.html",
        {"categories": Category.objects.all(), "title": "Добавить"},
    )


def about_us(request):
    return render(
        request,
        "about_us/about_us.html"
    )


class TopMoviesView(PoiskList, ListView):
    model = Movie
    template_name = "movies/top_movies.html"
    context_object_name = "top_movies"
    paginate_by = 5

    def get_queryset(self):
        return (
            Movie.objects.filter(status=Movie.Status.PUBLISHED)
            .exclude(
                Q(movie_of_rating__isnull=True)
                | Q(movie_of_rating__rating__isnull=True)
            )
            .annotate(average_rating=Avg("movie_of_rating__rating"))
            .order_by("-average_rating")
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.all()
        context["title"] = "Лучшие фильмы"
        return context


# Первый шаг: получение пользователя
def get_user(request):
    if request.method == "POST":
        form = GetUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            request.session["selected_username"] = username
            return redirect("update_status")
    else:
        form = GetUserForm()

    return render(
        request,
        "movies/get_user.html",
        {
            "form": form,
            "categories": Category.objects.all(),
            "title": "Выбрать пользователя",
        },
    )


# Второй шаг: обновление статуса пользователя


def update_status(request):
    username = request.session.get("selected_username")
    user = get_object_or_404(get_user_model(), username=username)

    if request.method == "POST":
        form = UpdateStatusForm(request.POST)
        if form.is_valid():
            new_status = form.cleaned_data["status"]
            if new_status == "администратор":
                user.is_superuser = True
                user.is_staff = True
            if new_status == "менеджер":
                user.is_superuser = False
                user.is_staff = True
            else:
                user.is_superuser = False
                user.is_staff = False

            user.status = new_status
            user.save(update_fields=["status", "is_superuser", "is_staff"])
            return redirect("add_buttons")
    else:
        initial_data = {"username": user}
        form = UpdateStatusForm(initial=initial_data)

    return render(
        request,
        "movies/update_status.html",
        {
            "form": form,
            "categories": Category.objects.all(),
            "title": "Обновить статус",
        },
    )
