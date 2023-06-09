# Generated by Django 4.2.2 on 2023-06-29 23:54
import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("movies", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AddField(
            model_name="raiting",
            name="movie",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="movie_of_rating",
                to="movies.movie",
                verbose_name="Фильм",
            ),
        ),
        migrations.AddField(
            model_name="raiting",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_of_rating",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AddField(
            model_name="movie_image",
            name="movie",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="movie_images",
                to="movies.movie",
                verbose_name="Фильм",
            ),
        ),
        migrations.AddField(
            model_name="movie",
            name="actors",
            field=models.ManyToManyField(
                related_name="movies_with_actor",
                to="movies.actor",
                verbose_name="Актер",
            ),
        ),
        migrations.AddField(
            model_name="movie",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="movie_of_category",
                to="movies.category",
                verbose_name="Категория",
            ),
        ),
        migrations.AddField(
            model_name="movie",
            name="director",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="movies_directed_by",
                to="movies.director",
                verbose_name="Режиссер",
            ),
        ),
        migrations.AddField(
            model_name="movie",
            name="genre",
            field=models.ManyToManyField(
                related_name="movies_with_the_gener",
                to="movies.genre",
                verbose_name="Жанр",
            ),
        ),
        migrations.AddIndex(
            model_name="review",
            index=models.Index(
                fields=["created"], name="movies_revi_created_e621fb_idx"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="raiting",
            unique_together={("user", "movie")},
        ),
        migrations.AddIndex(
            model_name="movie",
            index=models.Index(
                fields=["-publish"], name="movies_movi_publish_50589d_idx"
            ),
        ),
    ]
