from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe


class PosterMixin:
    def get_poster(self, obj, item):
        return mark_safe(f'<img src={item.url} width="120", height="80"')


class LinkMixin:
    def get_link(self, obj, item, str_item: str, app_name: str):
        link = reverse("admin:" + app_name + "_" + str_item + "_change", args=[item.pk])
        return format_html("<a href='{}'>{}</a>", link, item)


def get_short_description(func_name, short_desc: str) -> str:
    func_name.short_description = short_desc
    return func_name.short_description
