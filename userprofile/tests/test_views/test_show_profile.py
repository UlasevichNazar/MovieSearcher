import pytest
from django.http import Http404

from userprofile.models import Profile
from userprofile.views import ShowProfilePageView


@pytest.mark.django_db
class TestShowProfile:
    def test_retrieve_profile_successfully(self, user, profile):
        # Arrange
        profile.save()
        view = ShowProfilePageView()
        view.kwargs = {"profile_pk": user.id}

        # Act
        result = view.get_object()

        # Assert
        assert result == profile

    def test_profile_object_does_not_exist(self):
        # Arrange
        view = ShowProfilePageView()
        view.kwargs = {"profile_pk": 1}

        # Act & Assert
        with pytest.raises(Http404):
            view.get_object()

    def test_user_object_does_not_exist(self):
        # Arrange
        profile = Profile.objects.create()
        view = ShowProfilePageView()
        view.kwargs = {"profile_pk": profile.id}

        # Act & Assert
        with pytest.raises(Http404):
            view.get_object()
