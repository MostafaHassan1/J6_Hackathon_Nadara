import threading

from VideoCap import VideoCap
from main_face_recognition import load_images, face_recog, encode_images

if __name__ == '__main__':
    # # for testing
    images, names = load_images()
    encodings = encode_images(images)
    video = VideoCap().start()
    threading.Thread(target=face_recog,args=(video,encodings,names)).start()
    print(threading.enumerate())
    # while not video.stopped:
       # if not Thread.is_alive(face_rec_thread):
        #    face_rec_thread = Thread(target=face_recog, args=(video.frame, encodings, names)).start()
        # video.names=Thread(target=face_recog,args=(video.frame,encodings,names)).start()
       # video.names = face_recog(video.frame, encodings, names)

