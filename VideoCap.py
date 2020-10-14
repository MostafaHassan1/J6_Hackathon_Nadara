from threading import Thread

import cv2


class VideoCap:
    """
    responsible for getting the camera live feed in a its own thread
    """

    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        # indicate if the stream is stopped
        self.stopped = False

    """
    strats the thread and fire the get function that gets the live feed 
    """

    def start(self):
        Thread(target=self.get_and_show, args=()).start()
        return self

    """
    responsible for keeping the live feed running and showing the frame if it's not grabbed or stopped
    """

    def get_and_show(self):
        while not self.stopped:
            if (not self.grabbed) or cv2.waitKey(1) == ord("q"):
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()
                cv2.imshow("Live Video", self.frame)

    def stop(self):
        self.stopped = True

# # for testing
# video = VideoCap().start()
# while not video.stopped:
#   print("image:",video.frame)
