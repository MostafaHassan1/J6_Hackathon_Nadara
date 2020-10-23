from PIL import Image

import DB
import face_recognition


def insertNewPersonWithImage():
    image_path = input("Enter full image path: ")
    name = input("Person name: ")
    img = ''
    # # an example of the path
    #image_path= "Resources/Student_images/Mostafa_Hassan.jpg"
    encode = []
    try:
        img = face_recognition.load_image_file(image_path)
        encode = face_recognition.face_encodings(img)[0]
        list = encode.tolist()
        DB.insertPersonWithDataset(name, list)
        print(name, " Added successfully!")
    except Exception as e:
        print("Failed to load image: {}".format(e))


if __name__ == '__main__':
    insertNewPersonWithImage()
