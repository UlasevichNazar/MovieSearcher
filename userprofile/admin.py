from django.contrib import admin
from .models import Profile
from movies.mixins import LinkMixin, PosterMixin, get_short_description


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin, LinkMixin, PosterMixin):
    list_display = ["id", "get_full_link", "bio", "instagram", "get_image"]

    def get_image(self, obj):
        item = obj.profile_pic
        return self.get_poster(obj, item)

    get_short_description(get_image, "Постер")

    def get_full_link(self, obj):
        item = obj.user
        app_name = "user"
        str_item = "user"
        if item is not None:
            return self.get_link(obj, item, str_item, app_name)
        return None

    get_short_description(get_full_link, "Категория")
