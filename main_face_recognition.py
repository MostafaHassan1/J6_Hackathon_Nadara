import os
import cv2
import face_recognition


def load_images():
    """
     returns a list of those images and the corresponding student's name
     """
    # change this path to any path you have pictures in it 
    path_to_images = "Resources/Student_images"
    images = []
    students_names = []
    images_name = os.listdir(path_to_images)

    for image_name in images_name:
        images.append(face_recognition.load_image_file(f'{path_to_images}/{image_name}'))
        # to remove the image extension
        students_names.append(os.path.splitext(image_name)[0])
    return images, students_names


def encode_images(images):
    """
    takes the Students images we want to encode
    returns the encodings
    """
    encodings = []
    for img in images:
        encode = face_recognition.face_encodings(img)[0]
        encodings.append(encode)
    return encodings


def face_recog(frame, known_faces_encodings: list, students_names: list):

        names = []
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        faces_encodings = face_recognition.face_encodings(rgb_small_frame)
        for unknown_face_encoding in faces_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_faces_encodings, unknown_face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = students_names[first_match_index]
            names.append(name)

        if len(names) == 0:
           names = ["No face is visible"]

        return names

# if you want to see the encodings just remove the first 3 comments
#images, students_names = load_images()
#encodings = encode_images(images)
#print(encodings)
# face_recog(encodings, students_names)
