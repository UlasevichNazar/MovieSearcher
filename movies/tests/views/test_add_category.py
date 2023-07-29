import pytest

from movies.models import Category
from movies.views import add_category


@pytest.mark.django_db
class TestAddCategory:
    def test_valid_form(self, factory):
        # Arrange
        request = factory.post(
            "/add/category/",
            data={
                "name": "Test Category",
                "url": "test-category",
                "description": "This is a test category.",
            },
        )
        # Act
        response = add_category(request)
        # Assert
        assert response.status_code == 200
        assert Category.objects.filter(name="Test Category").exists()

    def test_invalid_form(self, factory):
        # Arrange
        request = factory.post(
            "/add/category/",
            data={"name": "", "url": "", "description": "This is a test category."},
        )
        # Act
        response = add_category(request)
        # Assert
        assert response.status_code == 200
        assert not Category.objects.filter(
            description="This is a test category."
        ).exists()

    def test_empty_form(self, factory):
        # Arrange
        request = factory.get("/add/category/")
        # Act
        response = add_category(request)
        # Assert
        assert response.status_code == 200

    #  Tests that category name and URL cannot be empty
    def test_empty_fields(self, factory):
        # Arrange
        request = factory.post(
            "/add/category/",
            data={"name": "", "url": "", "description": "This is a test category."},
        )
        # Act
        response = add_category(request)
        # Assert
        assert response.status_code == 200
        assert not Category.objects.filter(
            description="This is a test category."
        ).exists()
