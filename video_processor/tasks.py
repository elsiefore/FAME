import subprocess
import sys

from multiprocessing import Process, Queue
from time import sleep

from uploader.models import Result, Job, StatusChoice
from video_processor.classify import analyze_one_image
from django.core.files.storage import FileSystemStorage

import json

from video_processor.convert_to_frame import convert_video_to_frame
from uploader.ibm_client import IBMCOSClient
import os


def run_script(job_id, filename):
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
	# file_path_list = convert_video_to_frame(filename)
	# result_json_list = []
	# count = 0
	# for file_path in file_path_list:
	# 	result_json = analyze_one_image(img_path=file_path, time_stamp=count)
	# 	count += 1
	# 	result_json_list.append(result_json)

	result_json_list = [
		{
			"expressions": {
				"HAPPY": 2,
				"SURPRISE": 3,
				"NEUTRAL": 1
			},
			"timestamp": 0
		},
		{
			"expressions": {
				"HAPPY": 1,
				"SURPRISE": 2,
				"NEUTRAL": 3
			},
			"timestamp": 1
		},
		{
			"expressions": {
				"HAPPY": 1,
				"SURPRISE": 3,
				"NEUTRAL": 2
			},
			"timestamp": 2
		},
		{
			"expressions": {
				"HAPPY": 1,
				"SURPRISE": 1,
				"NEUTRAL": 4
			},
			"timestamp": 3
		},
		{
			"expressions": {
				"SURPRISE": 1,
				"NEUTRAL": 5
			},
			"timestamp": 4
		},
		{
			"expressions": {
				"SURPRISE": 2,
				"NEUTRAL": 4
			},
			"timestamp": 5
		},
		{
			"expressions": {
				"SURPRISE": 6
			},
			"timestamp": 6
		},
		{
			"expressions": {
				"SURPRISE": 6
			},
			"timestamp": 7
		},
		{
			"expressions": {
				"HAPPY": 1,
				"SURPRISE": 5
			},
			"timestamp": 8
		},
		{
			"expressions": {
				"HAPPY": 1,
				"SURPRISE": 5
			},
			"timestamp": 9
		},
		{
			"expressions": {
				"HAPPY": 1,
				"SURPRISE": 5
			},
			"timestamp": 10
		},
		{
			"expressions": {
				"HAPPY": 1,
				"SURPRISE": 5
			},
			"timestamp": 11
		},
		{
			"expressions": {
				"HAPPY": 1,
				"SURPRISE": 5
			},
			"timestamp": 12
		},
		{
			"expressions": {
				"HAPPY": 2,
				"SURPRISE": 4
			},
			"timestamp": 13
		},
		{
			"expressions": {
				"HAPPY": 3,
				"SURPRISE": 3
			},
			"timestamp": 14
		},
		{
			"expressions": {
				"HAPPY": 4,
				"SURPRISE": 2
			},
			"timestamp": 15
		},
		{
			"expressions": {
				"HAPPY": 3,
				"SURPRISE": 3
			},
			"timestamp": 16
		},
		{
			"expressions": {
				"HAPPY": 3,
				"SURPRISE": 3
			},
			"timestamp": 17
		},
		{
			"expressions": {
				"HAPPY": 3,
				"SURPRISE": 2,
				"NEUTRAL": 1
			},
			"timestamp": 18
		},
		{
			"expressions": {
				"HAPPY": 4,
				"SURPRISE": 2
			},
			"timestamp": 19
		},
		{
			"expressions": {
				"HAPPY": 3,
				"SURPRISE": 3
			},
			"timestamp": 20
		},
		{
			"expressions": {
				"HAPPY": 2,
				"SURPRISE": 4
			},
			"timestamp": 21
		},
		{
			"expressions": {
				"HAPPY": 3,
				"SURPRISE": 3
			},
			"timestamp": 22
		},
		{
			"expressions": {
				"HAPPY": 4,
				"SURPRISE": 2
			},
			"timestamp": 23
		},
		{
			"expressions": {
				"HAPPY": 4,
				"SURPRISE": 2
			},
			"timestamp": 24
		},
		{
			"expressions": {
				"HAPPY": 3,
				"SURPRISE": 3
			},
			"timestamp": 25
		},
		{
			"expressions": {
				"HAPPY": 4,
				"SURPRISE": 2
			},
			"timestamp": 26
		},
		{
			"expressions": {
				"HAPPY": 3,
				"SURPRISE": 3
			},
			"timestamp": 27
		},
		{
			"expressions": {
				"HAPPY": 5,
				"SURPRISE": 1
			},
			"timestamp": 28
		},
		{
			"expressions": {
				"HAPPY": 4,
				"SURPRISE": 1,
				"NEUTRAL": 1
			},
			"timestamp": 29
		}
	]
	print(result_json_list)
	result_json = {'result': result_json_list}
	try:
		job = Job.objects.get(pk=job_id)
		job.status = StatusChoice.Complete.value
		job.save()
	except Job.DoesNotExist:
		job = None

	if job:
		Result(job=job, result=result_json)
	return result_json
