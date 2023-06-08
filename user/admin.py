from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'free_mailing_list', 'paid_mailing_list', ]
    list_filter = ['username', 'email', 'free_mailing_list', 'paid_mailing_list', ]
    list_display_links = ['id', 'username', ]
    search_fields = ['username', 'id', 'email', 'free_mailing_list', 'paid_mailing_list', ]
    ordering = ['-id']
    filter_horizontal = ['groups', 'user_permissions', ]
    readonly_fields = ['last_login', ]
    fieldsets = (
        ('Основная информация о пользователе', {
            'fields': (('username',), ('first_name', 'last_name'), ('birthday',))}),
        (_('Email и пароль'), {
            'fields': (('email', 'password'),)}),
        (_('Permissions'),
         {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'), }),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('Рассылка'), {'fields': (('free_mailing_list', 'paid_mailing_list'),)})
    )
