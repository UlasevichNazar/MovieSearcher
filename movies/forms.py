from django import forms
from .models import Review, Raiting


class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["text"]


class RaitingForm(forms.ModelForm):
    class Meta:
        model = Raiting
        fields = ['rating']
