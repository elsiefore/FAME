from django import forms
from uploader.models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model= Video
        fields= ["name", "videofile"]