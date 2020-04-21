import cv2

from django.core.files.storage import FileSystemStorage


def convert_video_to_frame(filename):
    fs = FileSystemStorage()
    cam = cv2.VideoCapture(fs.base_location+filename)
    currentframe = 0
    fps = cam.get(cv2.CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
    skip = int(fps) - 1
    file_path_list = []
    while True:
        ret, frame = cam.read()
        if ret:
            if skip:
                skip = skip - 1
                continue
            else:
                skip = int(fps) - 1
            name = fs.base_location + str(filename) + '_img_' + str(currentframe) + '.jpg'
            file_path_list.append(name)
            cv2.imwrite(name, frame)
            currentframe += 1
        else:
            break

    cam.release()
    return file_path_list

