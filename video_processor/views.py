from django.http import JsonResponse

# Create your views here.
from .tasks import run_script


def index(request):
	run_script(123, '123.mp4')
	return JsonResponse({'status': 'ok'})
