import pytest

from user.models import User
from userprofile.models import Profile


@pytest.mark.django_db
class TestUserProfile:
    def test_create_profile_with_all_fields_valid(self, profile, user):
        assert profile.user == user
        assert profile.bio == "test bio"
        assert profile.profile_pic == "test_profile_pic.jpg"

    def test_update_profile_with_valid_data(self, profile):
        new_user = User.objects.create_user(
            username="new user",
            email="newuseremail@email.com",
            password="newuserpassword123",
        )
        profile.user = new_user
        profile.bio = "New bio from new user"
        profile.profile_pic = "new_profile_pic.jpg"
        profile.save()
        new_profile = Profile.objects.filter(user=new_user)
        assert new_profile.exists()
        assert new_profile[0].user == new_user
        assert new_profile[0].bio == "New bio from new user"
        assert new_profile[0].profile_pic == "new_profile_pic.jpg"

    def test_delete_profile_successfully(self, profile, user):
        profile.delete()
        with pytest.raises(Profile.DoesNotExist):
            Profile.objects.get(user=user)
