
from django.shortcuts import render
from django.http import JsonResponse

from video_processor.tasks import analyze_video
from .forms import VideoForm
from .models import Job, StatusChoice
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
                if cos_client.is_key_unique(filename):
                    cos_client.upload(uploaded_file_path, filename)
                    new_job = Job.objects.create(
                        display_name=filename, s3_obejct_key=filename, status=StatusChoice.Processing.value)
                    analyze_video(new_job.id, filename)
                    return JsonResponse(
                        {
                            'success': True,
                            'message': "Upload Successful!"
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'success': False,
                            'message': "Duplicate file key found. Please rename your file."
                        }
                    )
            except Exception as ex:
                Job.objects.create(
                    display_name=filename, s3_obejct_key=filename, status=StatusChoice.Failed.value)
                return JsonResponse(
                    {
                        'success': False,
                        'message': "Upload failed."
                    }
                )
    else:
        form = VideoForm()
    return render(request, 'index.html', {'form': form})


def health(request):
    state = {"status": "UP"}
    return JsonResponse(state)
