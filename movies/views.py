from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Avg
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic.edit import FormView

from . import models
from .forms import AddReviewForm, CategoryForm, GenreForm, DirectorForm, ActorForm
from .forms import RaitingForm
from .forms import MovieForm
from .models import Category, Director, Actor
from .models import Genre
from .models import Movie
from .models import Raiting


class PoiskList:
    def get_genres(self):
        return Genre.objects.all()

    def get_category(self):
        return Category.objects.all()

    def get_years(self):
        return list(
            set(
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
        context["average_rating"] = average_rating
        context["movies"] = self.get_queryset().distinct()

        context["categories"] = Category.objects.all()
        if self.request.user.is_authenticated:
            # Проверяем, выставил ли пользователь уже оценку для данного фильма
            raiting = Raiting.objects.filter(
                user=self.request.user, movie=movie
            ).first()
            if raiting:
                # Если оценка уже выставлена, скрываем форму
                context["rating_form"] = None
            else:
                # Если оценка еще не выставлена, отображаем форму
                context["rating_form"] = RaitingForm()
        else:
            context["rating_form"] = None

        return context

    def post(self, request, *args, **kwargs):
        movie = self.get_object()
        user = request.user

        # Проверяем, выставил ли пользователь уже оценку для данного фильма
        raiting = Raiting.objects.filter(user=user, movie=movie).first()

        if raiting:
            # Если оценка уже выставлена, перенаправляем пользователя обратно на страницу фильма
            return redirect("movie_detail", slug=movie.slug)

        form = RaitingForm(request.POST)
        if form.is_valid():
            # Сохраняем оценку фильма
            rating = form.save(commit=False)
            rating.user = user
            rating.movie = movie
            rating.save()

        return redirect("movie_detail", slug=movie.slug)


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


class FilterMovies(PoiskList, generic.ListView):
    def get_queryset(self):
        queryset = Movie.objects.all()
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
        context["s"] = f'q={self.request.GET.get("s")}&'
        context["movies"] = self.get_queryset().distinct()
        context["categories"] = Category.objects.all()

        return context


def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()  # Сохраняем фильм
            return redirect('movie_detail', slug=movie.slug)  # Перенаправляем на страницу деталей фильма
    else:
        form = MovieForm()
    return render(request, 'movies/add_movie.html', {'form': form})


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'movies/add_buttons.html')
    else:
        form = CategoryForm()
    return render(request, 'movies/add_category.html', {'form': form})


def add_genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'movies/add_buttons.html')
    else:
        form = GenreForm()
    return render(request, 'movies/add_genre.html', {'form': form})


def add_director(request):
    if request.method == 'POST':
        form = DirectorForm(request.POST, request.FILES)  # Включаем файлы запроса
        if form.is_valid():
            form.save()
            return render(request, 'movies/add_buttons.html')
    else:
        form = DirectorForm()
    return render(request, 'movies/add_director.html', {'form': form})


def add_actor(request):
    if request.method == 'POST':
        form = ActorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'movies/add_buttons.html')
    else:
        form = ActorForm()
    return render(request, 'movies/add_actor.html', {'form': form})


def add_buttons(request):
    return render(request, 'movies/add_buttons.html')
