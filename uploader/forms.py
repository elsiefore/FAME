from django import forms
from uploader.models import Video

class VideoForm(forms.Form):
    file = forms.FileField()