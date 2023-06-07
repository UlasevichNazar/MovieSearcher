from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class User(AbstractUser):
    username = models.CharField('Nickname', max_length=255, unique=True)
    email = models.EmailField('Email', unique=True)
    mailing_list_for_users = models.BooleanField('Mailing_list', )


