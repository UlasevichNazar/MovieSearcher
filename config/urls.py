from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("movies.urls")),
    path("user/", include("userprofile.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("accounts/", include("reg_login.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
