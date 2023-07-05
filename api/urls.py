from django.urls import include
from django.urls import path
from rest_framework import routers

from api.views import MovieView

router = routers.DefaultRouter()
router.register(r"movie", MovieView, basename="movies")
urlpatterns = [
    path("v1/", include(router.urls)),
]
