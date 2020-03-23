# !pip3 install opencv-python==4.1.2.30
# lastest4.2 version has some funny bug
import numpy as np
import sys
sys.path.extend(["/Users/dqin/Documents/FAME/watson_experiment"])
import cv2 as cv
import os
from util import ibm_location_to_cv

# img = np.zeros((512,512,3), np.uint8)
# img = cv.line(img, (100,100), (300,300), (0,0,255),4)
# img = cv.rectangle(img, (250,30), (450,200), (0,255,255), 5)
# img = cv.imread('logos.jpg')

folder_path = "/Users/dqin/Documents/FAME/watson_experiment/resources/FDDB-folds"
file_names = sorted([x for x in os.listdir(folder_path) if 'transformed' in x])


def draw_on_image(img_name, location):
    img_path = os.path.join("/Users/dqin/Documents/FAME/watson_experiment/resources/originalPics", img_name + ".jpg")
    img = cv.imread(img_path)
    (top, left), (width, height) = ibm_location_to_cv(location)
    print((left, top))
    print((left + width, top + height))

    img = cv.rectangle(img, (left, top), (left + width, top + height), (0, 255, 255), 3)
    cv.imshow('Draw01', img)


# TODO: Need to search on how to corp selected part of image?

for f in file_names:
    with open(os.path.join(folder_path, f), "r") as f:
        cur_img_name = ""
        for line in f:
            if "img_" in line:
                cur_img_name = line.strip()
            elif line.strip().isdigit():
                continue
            else:
                # if cur_img_name != '2002/07/31/big/img_945':
                #     continue
                location = [int(float(x)) for x in line.strip().split(", ")]
                # if any([x < 0 for x in location]):  # check for the -ve error...
                if True:
                    draw_on_image(cur_img_name, location)
                    cv.waitKey(1000)
                    cv.destroyAllWindows()
                    input("press for next...")
                    # print(locations)
