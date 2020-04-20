
import os
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

from .forms import VideoForm
from .models import Job, StatusChoice
from django.urls import reverse
from uploader.ibm_client import IBMCOSClient
from django.core.files.storage import FileSystemStorage


def home(request):
    if request.method == "POST":
        print("upload")
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            uploaded_file_path = fs.path(filename)
            cos_client = IBMCOSClient()
            try:
                if cos_client.is_key_unique(filename):
                    cos_client.upload(uploaded_file_path, filename)
                    Job.objects.create(
                        display_name=filename, s3_obejct_key=filename, status=StatusChoice.Processing.value)
                    messages.success(request, 'Upload successfully!')
                else:
                    messages.error(
                        request, 'Duplicate file key found. Please rename your file.')
                    print('DUp')
            except Exception as ex:
                Job.objects.create(
                    display_name=filename, s3_obejct_key=filename, status=StatusChoice.Failed.value)
                messages.error(request, 'Upload failed.')

            # remove the file in media folder
            # os.remove(uploaded_file_path)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = VideoForm()
    return render(request, 'index.html', {'form': form})


def health(request):
    state = {"status": "UP"}
    return JsonResponse(state)
