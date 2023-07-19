from django.db import models

from config import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(
        null=True,
        blank=True,
        upload_to="profile/",
        default="profile/defaul_user_image.png",
    )


def __str__(self):
    return str(self.user)
