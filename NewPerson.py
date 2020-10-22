import DB
import face_recognition
def insertNewPersonWithImage():
    image_path = input("Enter full image path: ")
    name = input("Person name: ")
    img = ''
    encode = []
    try:
        with face_recognition.load_image_file(image_path) as img:
            encode = face_recognition.face_encodings(img)[0]
    except Exception as e:
        print("Failed to load image: {}".format(e))
    

    DB.insertPersonWithDataset(name, encode)

    print(name, " Added successfully!")
