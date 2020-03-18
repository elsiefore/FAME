from __future__ import unicode_literals

from django.http import JsonResponse
from django.http import Http404
from django.shortcuts import render

from .models import Video
from .forms import VideoForm


def index(request):
    return render(request, 'index.html')


def health(request):
    state = {"status": "UP"}
    return JsonResponse(state)

# http://www.learningaboutelectronics.com/Articles/How-to-create-a-video-uploader-with-Python-in-Django.php
def showvideo(request):
    # form= VideoForm(request.POST or None, request.FILES or None)
    # if form.is_valid():
    # form.save()    
      
    return 'Upload Successful'