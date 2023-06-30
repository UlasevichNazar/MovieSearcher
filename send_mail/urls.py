from django.urls import path

from send_mail.views import send_mail_view
from send_mail.views import unsubscribe

urlpatterns = [
    path("", send_mail_view, name="send_mail"),
    path("ffff/", unsubscribe, name="unsubscribe"),
]
