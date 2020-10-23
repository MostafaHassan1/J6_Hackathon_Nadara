import cv2
import face_recognition

import DB
from main_face_recognition import load_images, face_recog, encode_images


class VideoCap:

    def __init__(self, src=0):
        """
        responsible for getting the camera live feed in a its own thread
        """
        self.stream = cv2.VideoCapture(src)
        # get the names and encodings from the database
        # can be replaced with main_face_recognition.load_images and encode_images if you don't want to work with database
        self.encodings, self.student_names = DB.getAllPeople()
        (self.grabbed, self.frame) = self.stream.read()
        self.names = ["unknown"]
        # indicate if the stream is stopped
        self.stopped = False

    def get_and_show(self):
        """
        responsible for keeping the live feed running and showing the frame if it's not grabbed or stopped
        and running the face recognition function on the live frame
        """
        no_of_frames = 0
        while not self.stopped:
            if (not self.grabbed) or cv2.waitKey(1) == ord("q"):
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

                no_of_frames += 1
                # controls how many frames we recognize (for now 1 per 60 frames)
                if no_of_frames % 60 == 0:
                    self.names = face_recog(self.frame, self.encodings, self.student_names)
                # Detect how mant faces in the frame
                if no_of_frames % 30 == 0:
                    # using locations instead of encodings because it's faster and we don't need to recognize them
                    locations = face_recognition.face_locations(self.frame)
                    # if more than one then it's group cheating
                    if len(locations) > 1:
                        img = cv2.imread("Resources/you_failed.jpg")
                        cv2.imshow("Cheating reason: more than one attended", img)

                # put the names we recognized on the frame
                cv2.putText(self.frame, " ,".join(self.names), (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
                cv2.imshow("Live Video", self.frame)

    def stop(self):
        self.stream.release()
        cv2.destroyAllWindows()
        self.stopped = True
