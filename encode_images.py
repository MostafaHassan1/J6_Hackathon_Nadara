import face_recognition
import os

def load_images(path_to_images):
    # takes the path of the students images to load them
    # returns a list of those images and the corresponding student's name
    images = []
    students_names = []
    images_name = os.listdir(path_to_images)

    for image_name in images_name:
        images.append(face_recognition.load_image_file(f'{path_to_images}/{image_name}'))
        # to remove the image extension
        students_names.append(os.path.splitext(image_name)[0])
    return images, students_names

def encode_images(path_to_images):
    # takes the path of the students images to load them
    # returns dict of students names and their encodings
    images, students_names = load_images(path_to_images)
    encodings = {}
    for img, student_name in zip(images,students_names):
        encode = face_recognition.face_encodings(img)
        encodings[student_name]= encode
    return encodings


path_to_images = "Resources/Student_images"
encodings= encode_images(path_to_images)
print(encodings)
