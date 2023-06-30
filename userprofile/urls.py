from django.urls import path

from . import views
from .views import ShowProfilePageView

urlpatterns = [
    path(
        "user_profile/<int:profile_pk>/",
        ShowProfilePageView.as_view(),
        name="user_profile",
    ),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
]
