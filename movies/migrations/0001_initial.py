# Generated by Django 4.2.2 on 2023-06-29 23:54
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

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
            name="Category",
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
                ("url", models.SlugField(max_length=100, verbose_name="URL")),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
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
                (
                    "slug",
                    models.SlugField(max_length=160, unique=True, verbose_name="URL"),
                ),
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
                (
                    "publish",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Публикация"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("DF", "Черновик"), ("PB", "Опубликовано")],
                        default="DF",
                        max_length=2,
                        verbose_name="Статус",
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
            ],
            options={
                "verbose_name": "Изображение фильма",
                "verbose_name_plural": "Изображения фильмов",
            },
        ),
        migrations.CreateModel(
            name="Raiting",
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
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(5),
                        ],
                        verbose_name="Оценка",
                    ),
                ),
            ],
            options={
                "verbose_name": "Рейтинг",
                "verbose_name_plural": "Рейтинги",
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
            ],
            options={
                "verbose_name": "Отзыв",
                "verbose_name_plural": "Отзывы",
                "ordering": ["created"],
            },
        ),
    ]
