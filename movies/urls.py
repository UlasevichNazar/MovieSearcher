from django.urls import path
from movies import views

urlpatterns = [
    path("", views.MovieList.as_view(), name="movie_list"),
    path("<slug:slug>/", views.MovieDetail.as_view(), name="movie_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
]
