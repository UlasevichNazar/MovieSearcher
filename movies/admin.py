from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.contrib.admin import TabularInline
from django.utils.translation import gettext_lazy as _

from . import models
from .mixins import get_short_description
from .mixins import LinkMixin
from .mixins import PosterMixin
from .models import Movie


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = "__all__"


###################################################
# INLINES
###################################################
class Movie_imageInline(TabularInline):
    model = models.Movie_image
    fields = ("name", "image")
    extra = 1


###################################################
# MODELS
###################################################
@admin.register(models.Movie)
class MovieAdmin(LinkMixin, PosterMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "get_full_link",
        "get_image",
        "status",
    )
    list_display_links = (
        "id",
        "title",
    )
    list_editable = ("status",)
    search_fields = (
        "title",
        "category",
    )
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("publish", "get_image")
    autocomplete_fields = ("category",)
    form = MovieAdminForm
    inlines = (Movie_imageInline,)
    radio_fields = {
        "status": admin.VERTICAL,
    }
    fieldsets = (
        (None, {"fields": ("title", "description")}),
        (None, {"fields": ("slug",)}),
        (None, {"fields": (("category", "genre"),)}),
        (_("Постер"), {"fields": (("poster", "get_image"),)}),
        (_("Действующие лица"), {"fields": (("director", "actors"),)}),
        (_("Страна производства и дата выхода"), {"fields": (("country", "year"),)}),
        (_("Сборы"), {"fields": (("budget", "fees_in_the_world"),)}),
        (_("Публикация"), {"fields": ("publish",)}),
        (_("Статус"), {"fields": ("status",)}),
    )

    def get_image(self, obj):
        item = obj.poster
        return self.get_poster(obj, item)

    get_short_description(get_image, "Постер")

    def get_full_link(self, obj):
        item = obj.category
        app_name = "movies"
        str_item = "category"
        if item is not None:
            return self.get_link(obj, item, str_item, app_name)
        return None

    get_short_description(get_full_link, "Категория")


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "url",
    )
    list_display_links = (
        "id",
        "name",
    )
    search_fields = ("name",)
    prepopulated_fields = {"url": ("name",)}


@admin.register(models.Movie_image)
class Movie_imageAdmin(LinkMixin, PosterMixin, admin.ModelAdmin):
    list_display = ("id", "name", "get_image", "get_full_link")
    list_display_links = (
        "id",
        "name",
    )
    readonly_fields = ("get_image",)

    fieldsets = (
        (None, {"fields": ("name",)}),
        (None, {"fields": (("image", "get_image"),)}),
        (None, {"fields": ("movie",)}),
    )

    def get_image(self, obj):
        item = obj.image
        return self.get_poster(obj, item)

    get_short_description(get_image, "Изображение")

    def get_full_link(self, obj):
        item = obj.movie
        app_name = "movies"
        str_item = "movie"
        if item is not None:
            return self.get_link(obj, item, str_item, app_name)
        return None

    get_short_description(get_full_link, "Фильм")


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
    )
    list_display_links = (
        "id",
        "name",
    )
    prepopulated_fields = {"slug": ("name",)}


@admin.register(models.Director)
class DirectorAdmin(PosterMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "image",
    )
    list_display_links = (
        "id",
        "name",
    )
    # readonly_fields = ("get_image",)
    fieldsets = (
        (None, {"fields": ("name",)}),
        (None, {"fields": ("description",)}),
        (None, {"fields": (("image",),)}),
    )

    # def get_image(self, obj):
    #     item = obj.image
    #     return self.get_poster(obj, item)
    #
    # get_short_description(get_image, "Изображение")


@admin.register(models.Actor)
class ActorAdmin(PosterMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "image",
    )
    list_display_links = (
        "id",
        "name",
    )
    # readonly_fields = ("get_image",)
    fieldsets = (
        (None, {"fields": ("name",)}),
        (None, {"fields": ("description",)}),
        (None, {"fields": (("image",),)}),
    )

    # def get_image(self, obj):
    #     item = obj.image
    #     return self.get_poster(obj, item)
    #
    # get_short_description(get_image, "Изображение")


@admin.register(models.Review)
class ReviewAdmin(LinkMixin, admin.ModelAdmin):
    list_display = ("id", "get_full_user_link", "get_full_movie_link", "created")
    list_display_links = ("id",)

    def get_full_user_link(self, obj):
        item = obj.user
        app_name = "user"
        str_item = "user"
        if item is not None:
            return self.get_link(obj, item, str_item, app_name)
        return None

    get_short_description(get_full_user_link, "Пользователь")

    def get_full_movie_link(self, obj):
        item = obj.movie
        app_name = "movies"
        str_item = "movie"
        if item is not None:
            return self.get_link(obj, item, str_item, app_name)
        return None

    get_short_description(get_full_movie_link, "Фильм")


@admin.register(models.Raiting)
class RaitingAdmin(LinkMixin, admin.ModelAdmin):
    list_display = ("id", "get_full_user_link", "get_full_movie_link", "rating")
    list_display_links = ("id",)

    def get_full_user_link(self, obj):
        item = obj.user
        app_name = "user"
        str_item = "user"
        if item is not None:
            return self.get_link(obj, item, str_item, app_name)
        return None

    get_short_description(get_full_user_link, "Пользователь")

    def get_full_movie_link(self, obj):
        item = obj.movie
        app_name = "movies"
        str_item = "movie"
        if item is not None:
            return self.get_link(obj, item, str_item, app_name)
        return None

    get_short_description(get_full_movie_link, "Фильм")
