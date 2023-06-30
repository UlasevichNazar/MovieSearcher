from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from .models import Profile
from django.contrib import messages
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required

#poverka commita
class ShowProfilePageView(DetailView):
    model = Profile
    template_name = "userprofile/user_profile.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs["pk"])
        context["page_user"] = page_user
        return context


class CreateProfilePageView(CreateView):
    model = Profile

    template_name = "userprofile/create_profile.html"
    fields = ["profile_pic", "bio", "facebook", "twitter", "instagram"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy("movie_list")


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('/')
    else:
        form = UserProfileForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    return render(request, 'userprofile/edit_profile.html', {'form': form, 'profile_form': profile_form})
