import traceback

from django.http import JsonResponse

# Create your views here.
from .tasks import run_script


def index(request):
	try:
		if request.method == "POST":
			job_id = request.POST.get('job_id', '')
			filename = request.POST.get('filename', '')
			result = run_script(job_id, filename)
	except Exception as e:
		result = traceback.format_exc()
	return JsonResponse({'status': result})


