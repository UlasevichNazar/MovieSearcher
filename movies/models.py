from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class AbstractModel(models.Model):
    name = models.CharField('Имя', max_length=100)
    description = models.TextField('Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        abstract = True


# Модель кино
class Movie(models.Model):
    class Status(models.TextChoices):
        DRAFT = ('DF', 'Черновик')
        PUBLISHED = ('PB', 'Опубликовано')

    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание')
    poster = models.ImageField('Постер', upload_to='movie_posters/')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='movie_of_category',
                                 verbose_name='Категория')
    genre = models.ManyToManyField('Genre', related_name='movies_with_the_gener', verbose_name='Жанр')
    director = models.ForeignKey('Director', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='movies_directed_by',
                                 verbose_name='Режиссер')
    actors = models.ManyToManyField('Actor', related_name='movies_with_actor', verbose_name='Актер')
    country = models.CharField('Страна производства', max_length=60)
    year = models.PositiveSmallIntegerField('Год выпуска', default=2020)
    budget = models.PositiveIntegerField('Бюджет фильма', default=0, help_text='Сумма в долларах')
    fees_in_the_world = models.PositiveIntegerField('Сборы в мире', default=0, help_text='Сумма в долларах')
    slug = models.SlugField('URL', max_length=100, unique=True)
    publish = models.DateTimeField('Публикация', default=timezone.now)
    status = models.CharField('Статус', max_length=2, choices=Status.choices, default=Status.DRAFT)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]


# Модель категории
class Category(AbstractModel):
    url = models.SlugField('URL', max_length=100)

    class Meta(AbstractModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# Модель кадры из фильма
class Movie_image(models.Model):
    name = models.CharField('Название', max_length=100)
    image = models.ImageField('Изображение', upload_to='movie_images/')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_images', verbose_name='Фильм')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Изображение фильма'
        verbose_name_plural = 'Изображения фильмов'


# Модель Жанр
class Genre(AbstractModel):
    slug = models.SlugField(max_length=160, unique=True, verbose_name="URL")

    class Meta(AbstractModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


# Модель Режиссер
class Director(AbstractModel):
    image = models.ImageField('Изображение', upload_to='directors/')

    class Meta(AbstractModel.Meta):
        verbose_name = 'Режиссер'
        verbose_name_plural = 'Режиссеры'


# Модель Актер
class Actor(AbstractModel):
    image = models.ImageField('Изображение', upload_to='actors/')

    class Meta(AbstractModel.Meta):
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', verbose_name="Пользователь")
    text = models.TextField('Текст')
    created = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie', verbose_name='Фильм')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]


# Модель рейтинга
class Raiting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_of_rating', verbose_name='Пользователь')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_of_rating', verbose_name='Фильм')
    rating = models.PositiveSmallIntegerField('Оценка', validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        unique_together = ('user', 'movie')
