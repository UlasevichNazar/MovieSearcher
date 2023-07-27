from django_filters import rest_framework as filters

from movies.models import Movie


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class MovieFilter(filters.FilterSet):
    genre = CharFilterInFilter(field_name="genre__name", lookup_expr="in")
    category = CharFilterInFilter(field_name="category__name", lookup_expr="in")
    year = filters.RangeFilter()

    class Meta:
        model = Movie
        fields = ("genre", "category", "year")
