# Importing all necessary libraries
# https://cloud.ibm.com/docs/services/cloud-object-storage/libraries?topic=cloud-object-storage-python#using-python


import cv2
import os

from django.core.files.storage import FileSystemStorage


def convert_video_to_frame(filename):
    # Read the video from specified path
    fs = FileSystemStorage()
    cam = cv2.VideoCapture(fs.base_location+filename)
    # frame
    currentframe = 0
    fps = cam.get(cv2.CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
    skip = int(fps) - 1
    file_path_list = []
    while True:
        #print('wgi...')
        # reading from frame
        ret, frame = cam.read()
        if ret:
            if skip:
                skip = skip - 1
                #print('skip...' + str(skip))
                continue
            else:
                skip = int(fps) - 1
            # if video is still left continue creating images
            name = fs.base_location + str(filename) + '_img_' + str(currentframe) + '.jpg'
            #print('Creating...' + name)
            file_path_list.append(name)
            # writing the extracted images
            cv2.imwrite(name, frame)

            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    cam.release()
    #cv2.destroyAllWindows()
    return file_path_list

