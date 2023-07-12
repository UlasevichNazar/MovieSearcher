from django.urls import path

from movies import views

urlpatterns = [
    path("", views.MovieList.as_view(), name="movie_list"),
    path("top", views.TopMoviesView.as_view(), name="top_movies"),
    path("search/", views.Search.as_view(), name="search"),
    path("filter/", views.FilterMovies.as_view(), name="filter"),
    path("add/buttons/", views.add_buttons, name="add_buttons"),
    path("category_buttons", views.category_buttons, name="category_buttons"),
    path("add/movie/", views.add_movie, name="add_movie"),
    path("add/category/", views.add_category, name="add_category"),
    path("add/genre/", views.add_genre, name="add_genre"),
    path("add/director/", views.add_director, name="add_director"),
    path("add/add_actor/", views.add_actor, name="add_actor"),
    path("add/add_movie_image/", views.add_movie_images, name="add_image"),
    path("<slug:slug>/", views.MovieDetail.as_view(), name="movie_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("actor/<str:slug>/", views.ActorView.as_view(), name="actor_view"),
    path("director/<str:slug>/", views.DirectorView.as_view(), name="director_view"),
    path("review/<int:pk>/delete/", views.delete_review, name="delete_review"),
    path("add/get_user/", views.get_user, name="get_user"),
    path("add/update_status/", views.update_status, name="update_status"),
]
