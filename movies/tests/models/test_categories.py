import pytest
from django.db.utils import DataError

from movies.models import Category


@pytest.mark.django_db
class TestCategories:
    def test_create_category_with_valid_data(self, category):
        assert category.name == "Test Category"
        assert category.description == "Test description"
        assert category.url == "test-category"

    def test_save_category_with_valid_data(self, category):
        category.save()
        assert Category.objects.count() == 1

    def test_retrieve_category(self, category):
        category.save()
        retrieved_category = Category.objects.get(id=category.id)
        assert retrieved_category == category

    def test_create_category_with_name_longer_than_max_length(self):
        with pytest.raises(DataError):
            Category.objects.create(
                name="a" * 101, description="Test", url="test-category"
            )

    def test_create_category_with_url_longer_than_max_length(self):
        with pytest.raises(DataError):
            Category.objects.create(name="test", description="Test", url="a" * 101)

    def test_create_category_with_empty_name(self):
        with pytest.raises(ValueError):
            Category.objects.create(name="", description="test", url="test-category")

    def test_create_category_with_empty_url(self):
        with pytest.raises(ValueError):
            Category.objects.create(name="test", description="test", url="")

    def test_retrieve_category_invalid_id(self):
        with pytest.raises(Category.DoesNotExist):
            Category.objects.get(id=0)
