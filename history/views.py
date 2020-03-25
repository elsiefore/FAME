from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from uploader.models import Job, Result
# Create your views here.


def list(request):
    job_list = Job.objects.all()
    return render(request, 'history.html', {'job_list': job_list})


def job_detail(request, job_id):
    result = Result.objects.get(job_id=job_id)
    return render(request, 'detail.html', {'result': result})
