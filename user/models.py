import datetime
from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from user.managers import MyCustomManager


class Role(Enum):
    USER = "пользователь"
    MANAGER = "менеджер"
    ADMIN = "администратор"


class User(AbstractUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)
    username = models.CharField("Никнейм", max_length=50, unique=True)
    email = models.EmailField("Email", max_length=100, unique=True)
    birthday = models.DateField("Дата рождения", default=datetime.date.today, null=True)
    free_mailing_list = models.BooleanField(
        "Бесплатная рассылка", blank=True, null=True, default=False
    )
    USERNAME_FIELD = "username"
    objects = MyCustomManager()
    status = models.CharField(
        "Статус",
        max_length=15,
        choices=[(role.value, role.name) for role in Role],
        default=Role.USER.value,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.username}"
