from django.urls import path

from movies import views

urlpatterns = [
    path("", views.MovieList.as_view(), name="movie_list"),
    path("search/", views.Search.as_view(), name="search"),
    path("filter/", views.FilterMovies.as_view(), name="filter"),
    path('add/buttons/', views.add_buttons, name='add_buttons'),
    path("add/movie/", views.add_movie, name='add_movie'),
    path("add/category/", views.add_category, name='add_category'),
    path("add/genre/", views.add_genre, name='add_genre'),
    path("add/director/", views.add_director, name='add_director'),
    path("add/add_actor/", views.add_actor, name='add_actor'),
    path("<slug:slug>/", views.MovieDetail.as_view(), name="movie_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
]
