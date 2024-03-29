from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from config import settings


class AbstractModel(models.Model):
    name = models.CharField("Имя", max_length=100, blank=False, null=False)
    description = models.TextField("Описание")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        abstract = True


# Модель кино
class Movie(models.Model):
    class Status(models.TextChoices):
        DRAFT = ("draft", "Черновик")
        PUBLISHED = ("publish", "Опубликовано")

    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movie_posters/")
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        related_name="movie_of_category",
        verbose_name="Категория",
    )
    genre = models.ManyToManyField(
        "Genre", related_name="movies_with_the_gener", verbose_name="Жанр"
    )
    director = models.ForeignKey(
        "Director",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="movies_directed_by",
        verbose_name="Режиссер",
    )
    actors = models.ManyToManyField(
        "Actor", related_name="movies_with_actor", verbose_name="Актер"
    )
    country = models.CharField("Страна производства", max_length=60)
    year = models.PositiveSmallIntegerField("Год выпуска", default=2020)
    budget = models.PositiveIntegerField(
        "Бюджет фильма", default=0, help_text="Сумма в долларах"
    )
    fees_in_the_world = models.PositiveIntegerField(
        "Сборы в мире", default=0, help_text="Сумма в долларах"
    )
    slug = models.SlugField("URL", max_length=100, unique=True)
    publish = models.DateTimeField("Публикация", default=timezone.now)
    status = models.CharField(
        "Статус", max_length=7, choices=Status.choices, default=Status.DRAFT
    )

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.title or not self.slug:
            raise ValueError("Название фильма или url фильма не может быть пустым.")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        ordering = ["-publish"]
        indexes = [models.Index(fields=["-publish"])]


@receiver(pre_delete, sender=Movie)
def movie_pre_delete(sender, instance, **kwargs):
    if instance.poster:
        default_storage.delete(instance.poster.path)


# Модель категории
class Category(AbstractModel):
    url = models.SlugField("URL", max_length=100, blank=False)

    class Meta(AbstractModel.Meta):
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def save(self, *args, **kwargs):
        if not self.name or not self.url:
            raise ValueError("Имя или url категории не может быть пустым.")
        super().save(*args, **kwargs)


# Модель кадры из фильма
class Movie_image(models.Model):
    name = models.CharField("Название", max_length=100)
    image = models.ImageField("Изображение", upload_to="movie_images/")
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="movie_images",
        verbose_name="Фильм",
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Изображение фильма"
        verbose_name_plural = "Изображения фильмов"

    def save(self, *args, **kwargs):
        if not self.name or not self.image:
            raise ValueError(
                "Имя или картинка в постерах к  фильму не может быть пустым."
            )
        super().save(*args, **kwargs)


@receiver(pre_delete, sender=Movie_image)
def movie_image_pre_delete(sender, instance, **kwargs):
    # Удаление файла изображения
    if instance.image:
        default_storage.delete(instance.image.path)


# Модель Жанр
class Genre(AbstractModel):
    slug = models.SlugField(max_length=160, unique=True, verbose_name="URL")

    class Meta(AbstractModel.Meta):
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def save(self, *args, **kwargs):
        if not self.name or not self.slug:
            raise ValueError("Имя или url жанра не может быть пустым.")
        super().save(*args, **kwargs)


# Модель Режиссер
class Director(AbstractModel):
    image = models.ImageField("Изображение", upload_to="directors/")

    class Meta(AbstractModel.Meta):
        verbose_name = "Режиссер"
        verbose_name_plural = "Режиссеры"

    def save(self, *args, **kwargs):
        if not self.name:
            raise ValueError("Имя режисера не может быть пустым.")
        super().save(*args, **kwargs)


# Модель Актер
class Actor(AbstractModel):
    image = models.ImageField("Изображение", upload_to="actors/")

    class Meta(AbstractModel.Meta):
        verbose_name = "Актер"
        verbose_name_plural = "Актеры"

    def save(self, *args, **kwargs):
        if not self.name:
            raise ValueError("Имя актера не может быть пустым.")
        super().save(*args, **kwargs)


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user",
        verbose_name="Пользователь",
    )
    text = models.TextField("Текст")
    created = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="reviews", verbose_name="Фильм"
    )

    def save(self, *args, **kwargs):
        if not self.text:
            raise ValueError("Комментарий не может быть пустым.")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["created"]
        indexes = [models.Index(fields=["created"])]


# Модель рейтинга
class Raiting(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_of_rating",
        verbose_name="Пользователь",
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="movie_of_rating",
        verbose_name="Фильм",
    )
    rating = models.PositiveSmallIntegerField(
        "Оценка", validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    def save(self, *args, **kwargs):
        if not (0 <= self.rating <= 10):
            raise ValidationError("Оценка должна быть в диапазоне от 0 до 10.")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
        unique_together = ("user", "movie")
