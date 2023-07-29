import pytest

from movies.models import Category
from movies.views import category_list


@pytest.mark.django_db
class TestCategoryList:
    def test_render_all_categories(self, factory, category):
        Category.objects.create(name="Action", url="action")
        request = factory.get("category_list/")
        response = category_list(request)
        assert response.status_code == 200
        assert "Action" in str(response.content)
        assert "Test Category" in str(response.content)

    def test_render_filtered_categories(self, factory, category):
        Category.objects.create(name="Action", url="action")
        request = factory.get("/category_list/", {"search": "act"})
        response = category_list(request)
        assert response.status_code == 200
        assert "Action" in str(response.content)
        assert "Test Category" not in str(response.content)

    def test_render_no_categories(self, factory):
        request = factory.get("/category_list/")
        response = category_list(request)
        assert response.status_code == 200

    def test_render_no_categories_found(self, factory, category):
        Category.objects.create(name="Action", url="action")
        request = factory.get("/category_list/", {"search": "drama"})
        response = category_list(request)
        assert response.status_code == 200
