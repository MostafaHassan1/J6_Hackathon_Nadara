import cv2
import face_recognition

from main_face_recognition import load_images, face_recog, encode_images


class VideoCap:

    def __init__(self, src=0):
        """
        responsible for getting the camera live feed in a its own thread
        """
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_BRIGHTNESS, 60)
        (self.grabbed, self.frame) = self.stream.read()
        self.names = ["unknown"]
        # indicate if the stream is stopped
        self.stopped = False

    #def start(self):
        """
        starts the thread and fire the get function that gets the live feed
        """
        #self.get_and_show()
        #return self

    def get_and_show(self):
        """
        responsible for keeping the live feed running and showing the frame if it's not grabbed or stopped
        """
        no_of_frames = 0
        images, student_names = load_images()
        encodings = encode_images(images)
        while not self.stopped:
            if (not self.grabbed) or cv2.waitKey(1) == ord("q"):
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

                no_of_frames += 1
                # controls how many frames we recognize (for now 1 per 60 frames)
                if no_of_frames % 60 == 0:
                    self.names = face_recog(self.frame, encodings, student_names)
                if no_of_frames % 30 == 0:
                    # using locations instead of encodings because it's faster and we don't need to recognize them
                    locations = face_recognition.face_locations(self.frame)
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
