import pytest
from django.urls import reverse

from reg_login.views import logout_user


@pytest.mark.django_db
class TestLogout:
    def test_logout_success(self, client, user):
        url = reverse("django_logout")
        client.force_login(user)
        response = client.get(url)

        assert response.status_code == 302
        assert not user.is_anonymous

    def test_redirect_to_login(self, client, user):
        url = reverse("django_logout")
        client.force_login(user)
        response = client.get(url)

        assert response.status_code == 302
        assert response.url == "/accounts/login/"

    def test_request_object_none(self):
        with pytest.raises(AttributeError):
            logout_user(None)
