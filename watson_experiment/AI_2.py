import json, os
from ibm_watson import VisualRecognitionV3, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

"""
    System parameters
"""
Watson_API_key = 'UNj_AQojzpzeg5q5FvmaMu2a3jathuqDB79_DjpAGJb_'
version_name = '2020-03-20'
# Different Collection ID for each Watson service_v4:

authenticator = IAMAuthenticator(Watson_API_key)
service_v3 = VisualRecognitionV3(version_name, authenticator=authenticator)

classifier_id = "FaceClassification_746624536"

# test file path
happy_face_path = "/Users/dqin/Documents/FAME/watson_experiment/sample_face_and_result/face_happy.jpg"
face_0_path = "/Users/dqin/Documents/FAME/watson_experiment/sample_face_and_result/face_0.jpg"
face_1_path = "/Users/dqin/Documents/FAME/watson_experiment/sample_face_and_result/face_1.jpg"

try:
    # with open(happy_face_path, 'rb') as images_file:
    with open(face_0_path, 'rb') as images_file:
        car_results = service_v3.classify(
            images_file=images_file,
            threshold='0.1',
            classifier_ids=classifier_id).get_result()
    print(json.dumps(car_results, indent=2))
except ApiException as ex:
    print(ex)

car_results

sorted_classes = sorted(car_results['images'][0]['classifiers'][0]['classes'], key=lambda t: t["score"], reverse=True)
sorted_classes

import tempfile, os

f = tempfile.TemporaryDirectory(dir="/Users/dqin/Documents/FAME/watson_experiment/intermediate_folder")
f.name
os.listdir(f.name)
f.cleanup()
