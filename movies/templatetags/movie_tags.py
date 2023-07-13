from django import template

from movies.models import Movie

register = template.Library()


@register.inclusion_tag("movies/soon_on_site/movies.html")
def get_movie(count):
    movies = Movie.objects.filter(status="DF")[:count]
    return {"soon_movies": movies}
