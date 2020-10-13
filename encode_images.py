import cv2
import face_recognition
import os

def load_images(path_to_images):
    # takes the path of the students images to load them
    # returns a list of those images
    images = []

    images_name = os.listdir(path_to_images)

    for image_name in images_name:
        images.append(cv2.imread(f'{path_to_images}/{image_name}'))

    return images

path_to_images = "Resources/Student_images"
load_images(path_to_images)