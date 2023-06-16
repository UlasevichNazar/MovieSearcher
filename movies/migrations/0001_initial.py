# Generated by Django 4.2.2 on 2023-06-08 20:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Actor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Имя")),
                ("description", models.TextField(verbose_name="Описание")),
                (
                    "image",
                    models.ImageField(upload_to="actors/", verbose_name="Изображение"),
                ),
            ],
            options={
                "verbose_name": "Актер",
                "verbose_name_plural": "Актеры",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Director",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Имя")),
                ("description", models.TextField(verbose_name="Описание")),
                (
                    "image",
                    models.ImageField(
                        upload_to="directors/", verbose_name="Изображение"
                    ),
                ),
            ],
            options={
                "verbose_name": "Режиссер",
                "verbose_name_plural": "Режиссеры",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Имя")),
                ("description", models.TextField(verbose_name="Описание")),
                ("slug", models.SlugField(max_length=160, unique=True)),
            ],
            options={
                "verbose_name": "Жанр",
                "verbose_name_plural": "Жанры",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Movie",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Название")),
                ("description", models.TextField(verbose_name="Описание")),
                (
                    "poster",
                    models.ImageField(
                        upload_to="movie_posters/", verbose_name="Постер"
                    ),
                ),
                (
                    "country",
                    models.CharField(max_length=60, verbose_name="Страна производства"),
                ),
                (
                    "year",
                    models.PositiveSmallIntegerField(
                        default=2020, verbose_name="Год выпуска"
                    ),
                ),
                (
                    "budget",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Сумма в долларах",
                        verbose_name="Бюджет фильма",
                    ),
                ),
                (
                    "fees_in_the_world",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Сумма в долларах",
                        verbose_name="Сборы в мире",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(max_length=100, unique=True, verbose_name="URL"),
                ),
                ("publish", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "status",
                    models.CharField(
                        choices=[("DF", "Черновик"), ("PB", "Опубликовано")],
                        default="DF",
                        max_length=2,
                    ),
                ),
                (
                    "actors",
                    models.ManyToManyField(
                        related_name="actor", to="movies.actor", verbose_name="Актер"
                    ),
                ),
                (
                    "director",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="director",
                        to="movies.director",
                        verbose_name="Режиссер",
                    ),
                ),
                (
                    "genre",
                    models.ManyToManyField(
                        related_name="genre", to="movies.genre", verbose_name="Жанр"
                    ),
                ),
            ],
            options={
                "verbose_name": "Фильм",
                "verbose_name_plural": "Фильмы",
                "ordering": ["-publish"],
            },
        ),
        migrations.CreateModel(
            name="Movie_image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Название")),
                (
                    "image",
                    models.ImageField(
                        upload_to="movie_images/", verbose_name="Изображение"
                    ),
                ),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="movie_images",
                        to="movies.movie",
                        verbose_name="Фильм",
                    ),
                ),
            ],
            options={
                "verbose_name": "Изображение фильма",
                "verbose_name_plural": "Изображения фильмов",
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(verbose_name="Текст")),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="movie",
                        to="movies.movie",
                        verbose_name="Фильм",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Отзыв",
                "verbose_name_plural": "Отзывы",
                "ordering": ["created"],
                "indexes": [
                    models.Index(
                        fields=["created"], name="movies_revi_created_e621fb_idx"
                    )
                ],
            },
        ),
        migrations.AddIndex(
            model_name="movie",
            index=models.Index(
                fields=["-publish"], name="movies_movi_publish_50589d_idx"
            ),
        ),
    ]
