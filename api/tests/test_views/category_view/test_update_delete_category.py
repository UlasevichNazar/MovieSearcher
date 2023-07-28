import pytest

from movies.models import Category


@pytest.mark.django_db
class TestUpdateDeleteCategory:
    def test_update_category_successfully_by_admin(
        self, api_client, superuser, category
    ):
        api_client.force_authenticate(superuser)
        url = f"/api/v1/category/admin/{category.pk}/"
        data = {
            "name": "Update Test Category",
            "description": "Update Test description",
            "url": "update-test-category",
        }
        response = api_client.put(url, data=data)
        updating_category = Category.objects.filter(name="Update Test Category")
        assert response.status_code == 200
        assert updating_category.exists()
        assert updating_category[0].name == "Update Test Category"
        assert updating_category[0].description == "Update Test description"
        assert updating_category[0].url == "update-test-category"

    def test_update_category_successfully_by_manager(
        self, api_client, manager, category
    ):
        api_client.force_authenticate(manager)
        url = f"/api/v1/category/admin/{category.pk}/"
        data = {
            "name": "Update Test Category",
            "description": "Update Test description",
            "url": "update-test-category",
        }
        response = api_client.put(url, data=data)
        updating_category = Category.objects.filter(name="Update Test Category")
        assert response.status_code == 200
        assert updating_category.exists()
        assert updating_category[0].name == "Update Test Category"
        assert updating_category[0].description == "Update Test description"
        assert updating_category[0].url == "update-test-category"

    def test_update_category_permissions_false(self, api_client, user, category):
        api_client.force_authenticate(user)
        url = f"/api/v1/category/admin/{category.pk}/"
        data = {
            "name": "Update Test Category",
            "description": "Update Test description",
            "url": "update-test-category",
        }
        response = api_client.put(url, data=data)
        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )

    def test_update_non_exiting_category(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        url = "/api/v1/category/admin/999/"
        data = {
            "name": "Update Test Category",
            "description": "Update Test description",
            "url": "update-test-category",
        }
        response = api_client.put(url, data=data)
        assert response.status_code == 404

    def test_delete_category_successfully_by_admin(
        self, api_client, category, superuser
    ):
        api_client.force_authenticate(superuser)
        url = f"/api/v1/category/admin/{category.pk}/"
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not Category.objects.filter(name="Test Category").exists()

    def test_delete_category_successfully_by_manager(
        self, api_client, category, manager
    ):
        api_client.force_authenticate(manager)
        url = f"/api/v1/category/admin/{category.pk}/"
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not Category.objects.filter(name="Test Category").exists()

    def test_delete_category_permissions_false(self, api_client, category, user):
        api_client.force_authenticate(user)
        url = f"/api/v1/category/admin/{category.pk}/"
        response = api_client.delete(url)
        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )
        assert Category.objects.filter(name="Test Category").exists()

    def test_delete_non_exiting_category(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        url = "/api/v1/category/admin/999/"
        response = api_client.delete(url)
        assert response.status_code == 404
