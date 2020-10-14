import threading

import cv2

from main_face_recognition import load_images, face_recog, encode_images


class VideoCap:

    def __init__(self, src=0):
        """
        responsible for getting the camera live feed in a its own thread
        """
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.names = ["unknown"]
        # indicate if the stream is stopped
        self.stopped = False

    def start(self):
        """
        starts the thread and fire the get function that gets the live feed
        """
        threading.Thread(target=self.get_and_show, args=()).start()
        return self

    def get_and_show(self):
        """
        responsible for keeping the live feed running and showing the frame if it's not grabbed or stopped
        """
        while not self.stopped:
            if (not self.grabbed) or cv2.waitKey(1) == ord("q"):
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()
                # put the names we recognized on the frame
                cv2.putText(self.frame, " ,".join(self.names), (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
                cv2.imshow("Live Video", self.frame)

    def stop(self):
        self.stream.release()
        cv2.destroyAllWindows()
        self.stopped = True



