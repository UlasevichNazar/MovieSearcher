import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from userprofile.models import Profile


@pytest.mark.django_db
class TestUpdateUserProfile:
    def test_update_user_profile_successfully_by_owner(self, api_client, user, profile):
        api_client.force_authenticate(user)
        url = f"/api/v1/user_profile/{profile.pk}/"
        image_path = "/app/media/test_updating_image.png"
        with open(image_path, "rb") as image_file:
            data = {
                "bio": "Updating Test bio",
                "image": SimpleUploadedFile(
                    "test_updating_image.png",
                    image_file.read(),
                    content_type="image/jpeg",
                ),
            }
        response = api_client.patch(url, data=data)
        print(response, data)
        updating_profile = Profile.objects.filter(user=user)

        assert response.status_code == 200
        assert updating_profile.exists()
        assert updating_profile[0].bio == "Updating Test bio"
