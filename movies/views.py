from django.db.models import Q
from django.shortcuts import render
from django.views import generic
from . import models
from .models import Genre, Raiting, Actor, Category, Movie


class PoiskList:
    def get_genres(self):
        return Genre.objects.all()

    def get_raiting(self):
        return Raiting.objects.all()

    def get_actor(self):
        return Actor.objects.all()

    def get_category(self):
        return Category.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year')


# Список фильмов
class MovieList(generic.ListView):
    model = models.Movie
    queryset = model.objects.filter(status=model.Status.PUBLISHED)
    context_object_name = 'movies'


# Фильтр фильмов
class FilterMovies(PoiskList, generic.ListView):
    def get_queryset(self):
        queryset = Movie.objects.filter(Q(year__in=self.request.GET.getlist('year')) |
                                        Q(genre__in=self.request.GET.getlist('genre')) |
                                        Q(raiting__in=self.request.GET.getlist('raiting')) |
                                        Q(actor__in=self.request.GET.getlist('actor')) |
                                        Q(category__in=self.request.GET.getlist('category'))
                                        )

        return queryset
