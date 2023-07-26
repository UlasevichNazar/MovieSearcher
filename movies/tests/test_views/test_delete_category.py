import pytest

from movies.models import Category
from movies.views import delete_category


@pytest.mark.django_db
class TestDeleteCategory:
    def test_delete_category_success(self, factory, category):
        request = factory.post(f"/delete_category/{category.id}/")
        response = delete_category(request, category.id)
        assert response.status_code == 302
        assert response.url == "/categories/"
        assert not Category.objects.filter(id=category.id).exists()

    def test_delete_category_does_not_exist(self, factory):
        request = factory.post("/delete_category/999/")
        with pytest.raises(Category.DoesNotExist):
            delete_category(request, 999)

    def test_delete_category_not_post(self, factory, category):
        request = factory.post(f"/delete_category/{category.id}/")
        response = delete_category(request, category.id)
        assert response.status_code == 302

    def test_delete_category_success_redirect(self, factory, category):
        request = factory.post(f"/delete_category/{category.id}/")
        response = delete_category(request, category.id)
        assert response.status_code == 302
        assert response.url == "/categories/"
        assert not Category.objects.filter(id=category.id).exists()
