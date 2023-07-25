from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic.detail import DetailView

from .forms import UserProfileForm
from .models import Profile
from movies.models import Category

User = get_user_model()


class ShowProfilePageView(DetailView):
    """
    View to display the profile page of a user.

    This view extends Django's built-in `DetailView` class and is responsible
    for displaying the user profile page based on the given `profile_pk`.

    Attributes:
        model (Profile): The Django model to use for retrieving the profile information.
        template_name (str): The name of the template used to render the profile page.

    Methods:
        get_object(self, queryset=None): Retrieves the profile object for the given `profile_pk`.
        get_context_data(self, **kwargs): Adds additional context data to be used in the template.
    """

    model = Profile
    template_name = "userprofile/user_profile.html"

    def get_object(self, queryset=None):
        """Retrieves the profile object for the given `profile_pk`"""
        user = get_object_or_404(User, id=self.kwargs.get("profile_pk"))
        profile = get_object_or_404(Profile, user=user)
        return profile

    def get_context_data(self, **kwargs):
        """Adds additional context data to be used in the template"""
        context = super().get_context_data(**kwargs)
        context["page_profile"] = self.object
        context["categories"] = Category.objects.all()

        return context


@login_required
def edit_profile(request):
    """
    The edit_profile function allows a user to edit their profile.
    It takes the request as an argument and returns a rendered template.
    If the request method is POST, it creates two forms: one for editing the User model and
     one for editing the Profile model.
    The form instances are passed in with instance=request.user or instance=request.userprofile
    so that they can be populated with data from those models when they're rendered on screen
    (i.e., so that users don't have to re-enter all of their information).
    If both forms are valid, then we save them using form_instance

    :param request: Get the user information
    :return: A render function
    """
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("user_profile", request.user.id)
        else:
            form = UserProfileForm(instance=request.user)
            profile_form = UserProfileForm(instance=request.user.profile)
    return render(
        request,
        "userprofile/edit_profile.html",
        {
            "form": form,
            "profile_form": profile_form,
            "categories": Category.objects.all(),
        },
    )
