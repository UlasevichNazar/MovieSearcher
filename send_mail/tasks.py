from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse

from config.celery import app
from movies.models import Movie

User = get_user_model()


@app.task
def send_email(user_id):
    user = User.objects.get(pk=user_id)
    random_movie = Movie.objects.order_by("?").first()
    movie_url = reverse("movie_detail", kwargs={"slug": random_movie.slug})
    send_mail(
        "KinoMan",
        f"B снова здравствуйте! {user.username}, Вас приветствует сайт KinoMan!!!\n"
        f"Вот ваш обещанный фильм, который мы рекомендуем посмотреть - {random_movie}\n"
        f"Ссылка на фильм: http://127.0.0.1:8000{movie_url}",
        "nazar@mail.ru",
        [user.email],
        fail_silently=False,
    )


@app.task
def send_email_per():
    for user in User.objects.filter(free_mailing_list=True):
        send_email(user.id)
