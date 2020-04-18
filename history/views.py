from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from uploader.models import Job, Result
# Create your views here.


def list(request):
    job_list = Job.objects.all()
    return render(request, 'history.html', {'job_list': job_list})


def job_detail(request, job_id):
    job = Job.objects.get(id=job_id)

    # below are for dev only
    json_result = {"result": [{"timestamp": 1, "expressions": {"ANGRY": 1, "FEAR": 1, "SURPRISE": 2}}, {
        "timestamp": 2, "expressions": {"ANGRY": 2, "FEAR": 1, "SURPRISE": 1}}]}
    result,_ = Result.objects.get_or_create(
        job_id=job_id, result=json_result)

    return render(request, 'detail.html', {'result': result})
