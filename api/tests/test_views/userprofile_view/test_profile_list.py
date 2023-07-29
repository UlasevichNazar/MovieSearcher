import pytest
from django.urls import reverse

from userprofile.models import Profile


@pytest.mark.django_db
class TestProfileList:
    def test_returns_profile_list(self, user, api_client, profile):
        api_client.force_authenticate(user)
        url = reverse("user_profiles")
        response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == Profile.objects.count()

    def test_returns_correct_serializer_class(self, api_client, user, profile):
        api_client.force_authenticate(user)
        url = reverse("user_profiles")
        response = api_client.get(url)

        assert response.status_code == 200
        assert list(response.data[0].keys()) == ["user", "bio", "profile_pic"]

    def test_returns_404_error_when_profile_not_found(self, api_client, user):
        api_client.force_authenticate(user)
        response = api_client.get("/user_profile/999/")

        assert response.status_code == 404
