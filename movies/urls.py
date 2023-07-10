from django.urls import path

from movies import views

urlpatterns = [
    path("", views.MovieList.as_view(), name="movie_list"),
    path("search/", views.Search.as_view(), name="search"),
    path("filter/", views.FilterMovies.as_view(), name="filter"),
    path("<slug:slug>/", views.MovieDetail.as_view(), name="movie_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("actor/<str:slug>/", views.ActorView.as_view(), name="actor_view"),
    path("review/<int:pk>/delete/", views.delete_review, name="delete_review"),
]
