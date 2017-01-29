from django import forms
from .models import Album


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['image']