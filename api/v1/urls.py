from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views.actors_view import ActorCreateView
from api.views.actors_view import ActorListView
from api.views.actors_view import ActorRetrieveView
from api.views.actors_view import ActorUpdateDestroyView
from api.views.category_view import CreateCategoryView
from api.views.category_view import UpdateDeleteCategory
from api.views.director_view import DirectorCreateView
from api.views.director_view import DirectorListView
from api.views.director_view import DirectorRetrieveView
from api.views.director_view import DirectorUpdateDestroyView
from api.views.genre_view import CreateGenreView
from api.views.genre_view import UpdateDeleteGenre
from api.views.movie_image_view import MovieImageCreateView
from api.views.movie_image_view import MovieImageListView
from api.views.movie_image_view import MovieImageUpdateDeleteView
from api.views.movie_views import BestMoviesView
from api.views.movie_views import MovieCreateView
from api.views.movie_views import MovieListView
from api.views.movie_views import MovieRetrieveView
from api.views.movie_views import MovieUpdateDestroyView
from api.views.rating_view import RatingView
from api.views.review_view import CreateReviewView
from api.views.review_view import DestroyReviewView
from api.views.review_view import ReviewView
from api.views.user_profile import UserProfileUpdateView
from api.views.user_profile import UserProfileView
from api.views.user_view import DeleteUserView
from api.views.user_view import GetUserView

router = DefaultRouter()
router.register("rating", RatingView, basename="rating")

movie_urlpatterns = [
    path("movie/", MovieListView.as_view(), name="movie_view"),
    path("movie/create/", MovieCreateView.as_view(), name="movie_create_view"),
    path("movie/<slug:slug>/", MovieRetrieveView.as_view(), name="movie_retrieve_view"),
    path(
        "movie/admin/<slug:slug>/",
        MovieUpdateDestroyView.as_view(),
        name="movie_update_destroy_view",
    ),
    path("best-movies/", BestMoviesView.as_view(), name="best_movie_view"),
]

review_urlpatterns = [
    path("reviews/", ReviewView.as_view(), name="reviews"),
    path("reviews/create/", CreateReviewView.as_view(), name="create_reviews"),
    path(
        "reviews/delete/<int:pk>/", DestroyReviewView.as_view(), name="destroy_reviews"
    ),
]

router_urlpatterns = [path("movie/", include(router.urls))]

actors_urlpatterns = [
    path("actors/", ActorListView.as_view(), name="actors_list"),
    path("actors/<int:pk>/", ActorRetrieveView.as_view(), name="actors_retrieve"),
    path("actors/create/", ActorCreateView.as_view(), name="actors_create"),
    path(
        "actors/admin/<int:pk>/",
        ActorUpdateDestroyView.as_view(),
        name="actors_delete_update",
    ),
]

director_urlpatterns = [
    path("director/", DirectorListView.as_view(), name="directors_list"),
    path(
        "director/<int:pk>/", DirectorRetrieveView.as_view(), name="director_retrieve"
    ),
    path("director/create/", DirectorCreateView.as_view(), name="director_create"),
    path(
        "director/admin/<int:pk>/",
        DirectorUpdateDestroyView.as_view(),
        name="director_delete_update",
    ),
]

category_urlpatterns = [
    path("category/create/", CreateCategoryView.as_view(), name="category_create"),
    path(
        "category/admin/<int:pk>/",
        UpdateDeleteCategory.as_view(),
        name="category_delete_update",
    ),
]

genre_urlpatterns = [
    path("genre/create/", CreateGenreView.as_view(), name="genre_create"),
    path(
        "genre/admin/<int:pk>/",
        UpdateDeleteGenre.as_view(),
        name="category_delete_update",
    ),
]

movie_image_urlpatterns = [
    path("movie_image/", MovieImageListView.as_view(), name="movie_images_list"),
    path(
        "movie_image/create/",
        MovieImageCreateView.as_view(),
        name="movie_images_create",
    ),
    path(
        "movie_image/admin/<int:pk>",
        MovieImageUpdateDeleteView.as_view(),
        name="movie_images_list",
    ),
]

reg_login_urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("auth/", include("djoser.urls.jwt")),
]

user_profile_urlpatterns = [
    path("user_profile/", UserProfileView.as_view(), name="user_profiles"),
    path(
        "user_profile/<int:pk>/",
        UserProfileUpdateView.as_view(),
        name="update_user_profile",
    ),
]
user_urlpatterns = [
    path("user/", GetUserView.as_view(), name="all_users"),
    path("user/delete/<int:pk>/", DeleteUserView.as_view(), name="delete_user_view"),
]

select2_urlpatterns = [
    path("select2/", include("django_select2.urls")),
]
urlpatterns = (
    movie_urlpatterns
    + review_urlpatterns
    + reg_login_urlpatterns
    + router_urlpatterns
    + actors_urlpatterns
    + director_urlpatterns
    + category_urlpatterns
    + genre_urlpatterns
    + movie_image_urlpatterns
    + user_profile_urlpatterns
    + user_urlpatterns
    + select2_urlpatterns
)
