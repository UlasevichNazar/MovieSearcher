import pytest
from django.urls import reverse

from movies.models import Category
from movies.views import edit_category


@pytest.mark.django_db
class TestEditCategory:
    def test_edit_category_valid_form(self, factory, category):
        # Given
        data = {
            "name": "Updated Category",
            "url": "updated-category",
            "description": "This is an updated category.",
        }
        request = factory.post(reverse("edit_category", args=[category.id]), data=data)
        # When
        response = edit_category(request, category.id)
        # Then
        assert response.status_code == 302
        assert response.url == reverse("category_list")
        assert Category.objects.get(id=category.id).name == "Updated Category"
        assert Category.objects.get(id=category.id).url == "updated-category"
        assert (
            Category.objects.get(id=category.id).description
            == "This is an updated category."
        )

    def test_edit_category_invalid_form(self, factory):
        # Given
        category = Category.objects.create(name="Test Category", url="test-category")
        data = {"name": "", "url": "", "description": "This is an updated category."}
        request = factory.post(reverse("edit_category", args=[category.id]), data=data)
        # When
        response = edit_category(request, category.id)
        # Then
        assert response.status_code == 302
        assert Category.objects.get(id=category.id).name == "Test Category"
        assert Category.objects.get(id=category.id).url == "test-category"
        assert Category.objects.get(id=category.id).description == ""

    def test_edit_category_category_does_not_exist(self, factory):
        # Given
        category_id = 999
        data = {
            "name": "Updated Category",
            "url": "updated-category",
            "description": "This is an updated category.",
        }
        request = factory.post(reverse("edit_category", args=[category_id]), data=data)
        # When
        with pytest.raises(Category.DoesNotExist):
            edit_category(request, category_id)
        # Then
        assert Category.objects.filter(name="Updated Category").count() == 0
        assert Category.objects.filter(url="updated-category").count() == 0

    def test_edit_category_duplicate_name_and_url(self, factory):
        # Given
        Category.objects.create(name="Test Category 1", url="test-category-1")
        category2 = Category.objects.create(
            name="Test Category 2", url="test-category-2"
        )
        data = {
            "name": "Test Category 2",
            "url": "test-category-1",
            "description": "This is an updated category.",
        }
        request = factory.post(reverse("edit_category", args=[category2.id]), data=data)
        # When
        response = edit_category(request, category2.id)
        # Then
        assert response.status_code == 302
        assert Category.objects.get(id=category2.id).name == "Test Category 2"
        assert Category.objects.get(id=category2.id).url == "test-category-1"
        assert (
            Category.objects.get(id=category2.id).description
            == "This is an updated category."
        )
