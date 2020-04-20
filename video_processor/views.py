import traceback

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from .tasks import run_script

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pythondjangoapp.settings")
django.setup()


@csrf_exempt
def index(request):
    try:
        if request.method == "POST":
            job_id = request.POST.get('job_id', '')
            filename = request.POST.get('filename', '')
            result = run_script(job_id, filename)
    except Exception as e:
        result = traceback.format_exc()
    return JsonResponse({'status': result})
