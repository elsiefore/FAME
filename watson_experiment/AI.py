"""
    Expression Classes:
        All together 7 expression classes:
            ANGRY, DISGUST, FEAR, HAPPY, NEUTRAL, SAD, SURPRISE


    Input: img_path (from local),
           time_stamp (seconds since the video start, when this image is screen captured)
           intermediate_folder (a folder for holding all the temporary files)

    Output:
    [{
       “expressions”: {
        “Expression_1” : count1,
        “Expression_2”:  count2,
        “Expression_3” : count3,
        ...
        },
       “timestamp”: 10; # time from the beginning of video
    }]
"""

import json, os, tempfile
from ibm_watson import VisualRecognitionV4, VisualRecognitionV3, ApiException
from ibm_watson.visual_recognition_v4 import FileWithMetadata, AnalyzeEnums
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from PIL import Image
from collections import Counter

"""
    System parameters
"""
version_name = '2020-03-20'
Watson_API_key = 'UNj_AQojzpzeg5q5FvmaMu2a3jathuqDB79_DjpAGJb_'

# Watson Visual Recognition URL:
VR_service_url = 'https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/de0d73f8-faaa-4318-9ed6-492a2822bf20'

# Different ID for each Watson service:
face_detection_CID = "0105d854-d33a-455a-989f-91ce7048982c"
classifier_id = "FaceClassification_746624536"

authenticator = IAMAuthenticator(Watson_API_key)
service_v4 = VisualRecognitionV4(version_name, authenticator=authenticator)
service_v4.set_service_url(VR_service_url)
service_v3 = VisualRecognitionV3(version_name, authenticator=authenticator)


def format_face_coords(ibm_analyze_result):
    """
    Parse the face coords extracted from IBM service_v4.

    :param ibm_analyze_result: the json object directly returned from IBM face detection service_v4
        see an example in "watson_experiment/sample_face_and_result/sample_output.json"
    :return: a list of location, each looks like
                {
                  "left": 64,
                  "top": 72,
                  "width": 124,
                  "height": 151
                },
    """
    objects = ibm_analyze_result['images'][0]['objects']['collections'][0]['objects']
    return [obj['location'] for obj in objects]


def recognize_faces(img_path=None, img_url=None):
    """
    Call Watson Face Recognition model, to recognize faces in an input images

    :param img_path: local path of input raw image file. Only one of img_path or img_url should be used.
    :param img_url: http/https url for input raw image. Only one of img_path or img_url should be used.
    :return: List of array, each element is the coordinates of faces, based on which faces can be cropped
    """

    try:
        assert (bool(img_path and img_url) is False)
        assert (bool(img_path or img_url) is True)
    except AssertionError:
        print("One and only one of the img_path or img_url should be specified")

    if img_path:
        with open(img_path, 'rb') as img_f:
            analyze_images = service_v4.analyze(collection_ids=face_detection_CID,
                                                features=AnalyzeEnums.Features.OBJECTS.value,
                                                images_file=[FileWithMetadata(img_f)]
                                                ).get_result()
    else:
        analyze_images = service_v4.analyze(collection_ids=face_detection_CID,
                                            features=AnalyzeEnums.Features.OBJECTS.value,
                                            image_url=[img_url]
                                            ).get_result()
    return format_face_coords(analyze_images)


def crop_faces(img_path, face_coords, save_folder_path):
    """
    Corp faces based on image and list of face coordinates

    :param img_path: input raw image file path
    :param face_coords: List of array, each element is the coordinates of faces, based on which faces can be cropped
            returned from extract_faces(). e.g.
            [{'left': 64, 'top': 72, 'width': 124, 'height': 151},
            {'left': 228, 'top': 30, 'width': 182, 'height': 200}]
    :param save_folder_path: Where the cropped images should be saved. Default None, i.e. save to the current folder
    :return: The temporary folder where cropped faces are stored
    """
    save_folder_path
    f = tempfile.TemporaryDirectory(dir=save_folder_path)

    im = Image.open(img_path)
    for i, coord in enumerate(face_coords):
        cur_fname = "face_" + str(i) + ".jpg"
        right = coord['left'] + coord['width']
        bottom = coord['top'] + coord['height']
        cur_face = im.crop((coord['left'], coord['top'], right, bottom))
        cur_face.save(os.path.join(f.name, cur_fname), 'jpeg')
    return f


def classify_one_face(face_file_path, threshold=0.2):
    """
    Classify one single face's expression

    :param face_file_path: the path of one face image
    :param threshold: the threshold for classification
    :return: o dictionary of
    {
     'class':'some_expression_name',
     'score': the corresponding score
    }
    """
    try:
        with open(face_file_path, 'rb') as images_file:
            classes = service_v3.classify(
                images_file=images_file,
                threshold=threshold,
                classifier_ids=classifier_id).get_result()
            sorted_classes = sorted(classes['images'][0]['classifiers'][0]['classes'], key=lambda t: t["score"],
                                    reverse=True)
            return sorted_classes[0]
    except ApiException as ex:
        print(ex)


def classify_faces_temp_dir(faces_temp_dir_obj):
    """
    :param faces_temp_dir_obj: a temporary directory object that holds all the cropped faces in one image.
        This object will be 'cleanup' once all the classification is finished
    :return: a dictionary of
    {
       “expressions”: {
        “Expression_1” : count1,
        “Expression_2”:  count2,
        “Expression_3” : count3,
        ...
        },
       “timestamp”: 10; # time from the beginning of video, to be modified later
    }
    """
    face_paths = filter(lambda x: not x.startswith('.'), os.listdir(faces_temp_dir_obj.name))
    classification_results = [classify_one_face(os.path.join(faces_temp_dir_obj.name, face_p)) for face_p in face_paths]
    expressions = [t['class'] for t in classification_results]
    expressions_dict = Counter(expressions)
    faces_temp_dir_obj.cleanup()
    return dict(expressions_dict)


def analyze_one_image(img_path, time_stamp, intermediate_folder):
    """

    :param img_path: path of the raw image
    :return: a dictionary of
    {
       “expressions”: {
        “Expression_1” : count1,
        “Expression_2”:  count2,
        “Expression_3” : count3,
        ...
        },
       “timestamp”: 10; # time from the beginning of video, to be modified later
    }
    """
    face_coords = recognize_faces(img_path)
    faces_temp_dir_obj = crop_faces(img_path, face_coords, intermediate_folder)
    expression_count = classify_faces_temp_dir(faces_temp_dir_obj)
    return {"expressions": expression_count, "timestamp": time_stamp}


if __name__ == "__main__":
    # face_coords = recognize_faces(img_url=sample_img_url)
    # temp_f = crop_faces(sample_img_path, face_coords, intermediate_folder)
    # expression_count_dict = classify_faces_temp_dir(temp_f)
    # print(expression_count_dict)

    # test file path
    sample_img_path = "/Users/dqin/Documents/FAME/watson_experiment/sample_face_and_result/img_404.jpg"
    sample_img_url = 'https://i.ibb.co/6WK91F0/img-404.jpg'
    happy_face_path = "/Users/dqin/Documents/FAME/watson_experiment/sample_face_and_result/face_happy.jpg"
    intermediate_folder = "/Users/dqin/Documents/FAME/watson_experiment/intermediate_folder"  # folder used to store intermediate corp faces

    output = analyze_one_image(img_path=sample_img_path, time_stamp=5, intermediate_folder=intermediate_folder)
    print(output)
