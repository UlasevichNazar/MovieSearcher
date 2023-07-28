from unittest.mock import Mock

import pytest
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse

from userprofile.forms import UserProfileForm
from userprofile.models import Profile
from userprofile.views import edit_profile
from userprofile.views import User


@pytest.mark.django_db
class TestEditProfile:
    def test_valid_form_submission(
        self,
        user,
        profile,
        factory,
    ):
        url = reverse("edit_profile")
        data = {
            "username": "newusername",
            "email": "newuseremail@email.com",
            "birthday": "01.01.2023",
            "bio": "new bio",
        }
        UserProfileForm(data, instance=user)
        UserProfileForm(data, instance=profile)
        request = factory.post(url, data=data)
        request.user = user
        messages.success = Mock()

        response = edit_profile(request)
        updating_user = User.objects.get(id=user.id)
        assert response.status_code == 302
        assert response.url == f"/user/user_profile/{user.id}/"
        assert updating_user.username == "newusername"
        assert updating_user.email == "newuseremail@email.com"
        assert updating_user.profile.bio == "new bio"
        messages.success.assert_called_once_with(
            request, "Your profile has been updated."
        )

    def test_invalid_form_submission(self, user, profile, factory):
        url = reverse("edit_profile")
        data = {"username": "", "email": "", "birthday": "", "bio": ""}
        UserProfileForm(data, instance=user)
        UserProfileForm(data, instance=profile)
        request = factory.post(url, data=data)
        request.user = user
        messages.success = Mock()

        response = edit_profile(request)

        assert response.status_code == 200
        assert User.objects.get(id=user.id).username == "testuser"
        assert User.objects.get(id=user.id).email == "test@test.com"
        assert User.objects.get(id=user.id).profile.bio == "test bio"
        messages.success.assert_not_called()

    def test_user_not_logged_in(self, factory):
        response_url = "/accounts/login/?next=/user/edit_profile/"
        url = reverse("edit_profile")
        request = factory.get(url)
        request.user = AnonymousUser()

        response = edit_profile(request)

        assert response.status_code == 302
        assert response.url == response_url

    def test_edit_another_user_profile(self, user, profile, factory):
        user2 = User.objects.create(
            username="anotheruser",
            email="anotheruseremail@email.com",
            password="anotheruserpassword123",
        )
        url = reverse("edit_profile")
        data = {
            "username": "newusername",
            "email": "newemail@test.com",
            "birthday": "01.01.2000",
            "bio": "new bio",
        }
        UserProfileForm(data, instance=user)
        UserProfileForm(data, instance=profile)
        request = factory.post(url, data=data)
        request.user = user2
        messages.success = Mock()
        with pytest.raises(Profile.DoesNotExist):
            edit_profile(request)
