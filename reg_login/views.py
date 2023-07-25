from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LoginUserForm
from .forms import RegisterUserForm
from send_mail.tasks import send_email_per
from userprofile.models import Profile


class Register(CreateView):
    """
    The get_context_data function is a method of the generic class-based view that allows you to add additional context
    variables to the template.
    The get_context_data function takes in **kwargs, which are keyword arguments passed from the view.
    In this case, we're adding a title variable with value Регистрация.

    :param self: Represent the instance of the object
    :param **kwargs: Pass keyworded, variable-length argument list
    :return: A dictionary with the context of the template
    """

    form_class = RegisterUserForm
    template_name = "registration/register.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("movie_list")

    def form_valid(self, form):
        user = form.save()
        if user.free_mailing_list == True:
            send_email_per.delay()
        if user is not None:
            Profile.objects.create(user=user)
            login(self.request, user)
        return redirect("movie_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация"
        return context


class LoginUser(LoginView):
    """
    The get_context_data function is a method of the generic class-based view that allows you to add additional context
    variables to the template.
    The get_context_data function takes in **kwargs, which are keyword arguments passed from the view.
    In this case, we're adding a title variable with value Войти.

    :param self: Represent the instance of the object
    :param **kwargs: Pass keyworded, variable-length argument list
    :return: A dictionary that contains the context for the template
    """

    from_class = LoginUserForm
    template_name = "login/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Войти"
        return context


def logout_user(request):
    """
    The logout_user function logs out the user and redirects them to the login page.

    :param request: Pass the request object to the view
    :return: A redirect to the django_login view
    """
    logout(request)
    return redirect("django_login")
