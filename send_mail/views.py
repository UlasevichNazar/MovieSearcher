from django.shortcuts import redirect

from send_mail.tasks import send_email_per


def send_mail_view(request):
    user = request.user
    user.free_mailing_list = True
    user.save()
    send_email_per.delay()
    return redirect("user_profile")


def unsubscribe(request):
    user = request.user
    user.free_mailing_list = False
    user.save()
    return redirect("user_profile")
