
from django.http import JsonResponse,Http404,HttpResponseRedirect
from django.shortcuts import render

from .forms import VideoForm
from django.urls import reverse
from uploader.ibm_client import IBMCOSClient
from django.core.files.storage import FileSystemStorage

def home(request):
    if request.method=="POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            uploaded_file_path = fs.path(filename)
            cos_client = IBMCOSClient()
            cos_client.upload(uploaded_file_path,filename)
            return HttpResponseRedirect(reverse('home'))
    else:
        form=VideoForm()
    return render(request,'index.html',{'form':form})

def health(request):
    state = {"status": "UP"}
    return JsonResponse(state)

# http://www.learningaboutelectronics.com/Articles/How-to-create-a-video-uploader-with-Python-in-Django.php
def showvideo(request):
    # form= VideoForm(request.POST or None, request.FILES or None)
    # if form.is_valid():
    # form.save()

    return 'Upload Successful'