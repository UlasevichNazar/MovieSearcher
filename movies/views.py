from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import generic
from django.views import View

from . import models
from .forms import AddReviewForm
from .models import Category
from .models import Genre
from .models import Movie
from .models import Raiting


class PoiskList:
    def get_genres(self):
        return Genre.objects.all()

    def get_category(self):
        return Category.objects.all()

    def get_years(self):
        return Movie.objects.values_list("year", flat=True).distinct()


# Список фильмов
class MovieList(PoiskList, generic.ListView):
    model = models.Movie
    queryset = model.objects.filter(status=model.Status.PUBLISHED)
    context_object_name = "movies"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.all()
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
        context["categories"] = Category.objects.all()
        return context


class AddReview(View):
    @method_decorator(login_required)
    def post(self, request, pk):
        form = AddReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
        return redirect(movie.get_absolute_url())


# Фильтр фильмов
class FilterMovies(PoiskList, generic.ListView):
    def get_queryset(self):
        queryset = Movie.objects.all()
        if "category" in self.request.GET:
            queryset = queryset.filter(
                category__in=self.request.GET.getlist("category")
            )
        if "genre" in self.request.GET:
            queryset = queryset.filter(genre__in=self.request.GET.getlist("genre"))
        if "year" in self.request.GET:
            queryset = queryset.filter(year__in=self.request.GET.getlist("year"))
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movies"] = self.get_queryset()
        context["categories"] = Category.objects.all()
        return context
