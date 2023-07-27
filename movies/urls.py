from django.urls import path

from movies import views

urlpatterns = [
    path("", views.MovieList.as_view(), name="movie_list"),
    path("top", views.TopMoviesView.as_view(), name="top_movies"),
    path("search/", views.Search.as_view(), name="search"),
    path("filter/", views.FilterMovies.as_view(), name="filter"),
    path("add/buttons/", views.add_buttons, name="add_buttons"),
    path("about_us/", views.about_us, name="about_us"),
    path("category_buttons/", views.category_buttons, name="category_buttons"),
    path("categories/", views.category_list, name="category_list"),
    path("category/<int:category_id>/edit/", views.edit_category, name="edit_category"),
    path(
        "categories/<int:category_id>/delete/",
        views.delete_category,
        name="delete_category",
    ),
    path("add/movie/", views.add_movie, name="add_movie"),
    path("movies/", views.movie_list_admin, name="movie_list_admin"),
    path("movies/edit/<int:movie_id>/", views.edit_movie, name="edit_movie"),
    path("movies/delete/<int:movie_id>/", views.delete_movie, name="delete_movie"),
    path("add/category/", views.add_category, name="add_category"),
    path("add/genre/", views.add_genre, name="add_genre"),
    path("genres/", views.genre_list, name="genre_list"),
    path("genres/<int:genre_id>/", views.edit_genre, name="edit_genre"),
    path("genres/<int:genre_id>/delete/", views.delete_genre, name="delete_genre"),
    path("add/director/", views.add_director, name="add_director"),
    path("directors/", views.director_list, name="all_directors_list"),
    path(
        "directors/edit/<int:director_id>/", views.edit_director, name="edit_director"
    ),
    path(
        "directors/delete/<int:director_id>/",
        views.delete_director,
        name="delete_director",
    ),
    path("add/add_actor/", views.add_actor, name="add_actor"),
    path("actors/", views.actor_list, name="actor_list"),
    path("actors/edit/<int:actor_id>/", views.edit_actor, name="edit_actor"),
    path("actors/delete/<int:actor_id>/", views.delete_actor, name="delete_actor"),
    path("add/add_movie_image/", views.add_movie_images, name="add_image"),
    path("<slug:slug>/", views.MovieDetail.as_view(), name="movie_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("actor/<str:slug>/", views.ActorView.as_view(), name="actor_view"),
    path("director/<str:slug>/", views.DirectorView.as_view(), name="director_view"),
    path("review/<int:pk>/delete/", views.delete_review, name="delete_review"),
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path("add/get_user/", views.get_user, name="get_user"),
    path("add/update_status/", views.update_status, name="update_status"),
    path("add/delete-user/", views.delete_user, name="delete_user"),
]
