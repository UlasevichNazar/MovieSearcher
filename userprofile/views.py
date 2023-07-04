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
    model = Profile
    template_name = "userprofile/user_profile.html"

    def get_object(self, queryset=None):
        user = get_object_or_404(User, id=self.kwargs.get("profile_pk"))
        profile = get_object_or_404(Profile, user=user)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_profile"] = self.object
        context["categories"] = Category.objects.all()

        return context


@login_required
def edit_profile(request):
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
