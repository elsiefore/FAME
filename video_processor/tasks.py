import subprocess
import sys

from multiprocessing import Process, Queue
from time import sleep

from uploader.models import Result, Job
from video_processor.classify import analyze_one_image
from django.core.files.storage import FileSystemStorage

import json

from video_processor.convert_to_frame import convert_video_to_frame
from uploader.ibm_client import IBMCOSClient
import os


def run_script(job_id, filename):
	#subprocess.Popen([sys.executable, "/Users/lu.xia/fame/FAME/tester/video_processor/script.py", "argument"])
	queue = Queue()
	p = Process(target=new_function_call, args=(queue, job_id, filename))
	p.start()
	return 'ok'


def new_function_call(queue, job_id, filename):
	fs = FileSystemStorage()
	path = fs.base_location + filename
	if not os.path.isfile(path):
		cos_client = IBMCOSClient()
		cos_client.download(filename)

	# frame

	file_path_list = convert_video_to_frame(filename)
	result_json_list = []
	count = 0
	for file_path in file_path_list:
		result_json = analyze_one_image(img_path=file_path, time_stamp=count)
		count += 1
		result_json_list.append(result_json)

	print(result_json_list)
	result_json = {'result': result_json_list}
	try:
		job = Job.objects.get(pk=job_id)
		job.status = 'Success'
		job.save()
	except Job.DoesNotExist:
		job = None


	if job:
		new_result = Result(job_id=job, result=result_json)
	# result = Result.objects.create()
	# result.job_id = job_id
	# result.result = json.dumps(result_json_list)
	# result.save()
	return result_json
