
from VideoCap import VideoCap
from main_face_recognition import load_images, face_recog, encode_images

if __name__ == '__main__':
    # # for testing
    images, names = load_images()
    encodings = encode_images(images)
    video = VideoCap().start()

    while not video.stopped:
        video.names = face_recog(video.frame, encodings, names)

