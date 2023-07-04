from django.urls import include
from django.urls import path


urlpatterns = [path("v1/doc/", include("api.spectacular.urls"))]
