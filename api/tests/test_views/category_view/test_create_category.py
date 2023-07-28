import pytest
from django.urls import reverse

from movies.models import Category


@pytest.mark.django_db
class TestCreateCategory:
    def test_create_category_successfully_by_admin(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        url = reverse("category_create")
        data = {
            "name": "Test Category",
            "description": "Test description",
            "url": "test-category",
        }
        response = api_client.post(url, data=data)

        new_category = Category.objects.filter(name="Test Category")
        assert response.status_code == 201
        assert new_category.exists()
        assert new_category[0].name == "Test Category"
        assert new_category[0].description == "Test description"
        assert new_category[0].url == "test-category"
        new_category.delete()

    def test_create_category_successfully_by_manager(self, api_client, manager):
        api_client.force_authenticate(manager)
        url = reverse("category_create")
        data = {
            "name": "Test Category",
            "description": "Test description",
            "url": "test-category",
        }
        response = api_client.post(url, data=data)

        new_category = Category.objects.filter(name="Test Category")
        assert response.status_code == 201
        assert new_category.exists()
        assert new_category[0].name == "Test Category"
        assert new_category[0].description == "Test description"
        assert new_category[0].url == "test-category"
        new_category.delete()

    def test_create_category_permission_false(self, api_client, user):
        api_client.force_authenticate(user)
        url = reverse("category_create")
        data = {
            "name": "Test Category",
            "description": "Test description",
            "url": "test-category",
        }
        response = api_client.post(url, data=data)
        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )

    def test_create_category_with_missing_required_fields(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        url = reverse("category_create")
        data = {
            "description": "Test description",
        }
        response = api_client.post(url, data=data)
        assert response.status_code == 400
        assert not Category.objects.filter(description="Test description").exists()
