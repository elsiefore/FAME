# Copy images to desired places...
import shutil, os

multiface_paths = "/Users/dqin/Documents/FAME/watson_experiment/resources/FDDB-folds/multi_face_filenames_sorted.txt"

skip_first = 40 # skip first ... images
take_number = 50 # take next ... images
dest_folder = "/Users/dqin/Documents/FAME/watson_experiment/resources/multi_faces"

with open(multiface_paths, "r") as f:
    count  = 0
    for cur_l in f:
        count = count + 1
        if (count >= skip_first) and (count < skip_first + take_number):
            # copy file
            file_name = cur_l.strip().split("/")[-1]
            shutil.move(cur_l.strip(), os.path.join(dest_folder, file_name))