from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views.movie_views import MovieCreateView
from api.views.movie_views import MovieListView
from api.views.movie_views import MovieRetrieveView
from api.views.movie_views import MovieUpdateDestroyView
from api.views.rating_view import CreateRatingView
from api.views.review_view import CreateReviewView
from api.views.review_view import DestroyReviewView
from api.views.review_view import ReviewView

router = DefaultRouter()
router.register("rating/create", CreateRatingView, basename="create_rating")


movie_urlpatterns = [
    path("movie/", MovieListView.as_view(), name="movie_view"),
    path("movie/create/", MovieCreateView.as_view(), name="movie_create_view"),
    path("movie/<slug:slug>/", MovieRetrieveView.as_view(), name="movie_retrieve_view"),
    path(
        "movie/admin/<slug:slug>/",
        MovieUpdateDestroyView.as_view(),
        name="movie_update_destroy_view",
    ),
]

review_urlpatterns = [
    path("reviews/", ReviewView.as_view(), name="reviews"),
    path("reviews/create/", CreateReviewView.as_view(), name="create_reviews"),
    path(
        "reviews/delete/<int:pk>/", DestroyReviewView.as_view(), name="destroy_reviews"
    ),
]

router_urlpatterns = [path("movie/", include(router.urls))]

reg_login_urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("auth/", include("djoser.urls.jwt")),
]

urlpatterns = (
    movie_urlpatterns + review_urlpatterns + reg_login_urlpatterns + router_urlpatterns
)
