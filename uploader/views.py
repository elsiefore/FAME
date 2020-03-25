
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import render

from .forms import VideoForm
from .models import Job, StatusChoice
from django.urls import reverse
from uploader.ibm_client import IBMCOSClient
from django.core.files.storage import FileSystemStorage


def home(request):
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            uploaded_file_path = fs.path(filename)
            cos_client = IBMCOSClient()
            try:
                cos_client.upload(uploaded_file_path, filename)
                Job.objects.create(
                    display_name=filename, s3_obejct_key=uploaded_file_path, status=StatusChoice.Processing.value)
            except:
                Job.objects.create(
                    display_name=filename, s3_obejct_key=uploaded_file_path, status=StatusChoice.Failed.value)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = VideoForm()
    return render(request, 'index.html', {'form': form})


def health(request):
    state = {"status": "UP"}
    return JsonResponse(state)
