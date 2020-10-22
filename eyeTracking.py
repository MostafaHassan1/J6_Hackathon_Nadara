import cv2
import dlib
import numpy as np


def shape_to_np(shape, dtype="int"):
    # initialize the list of (x, y)-coordinates
    coords = np.zeros((68, 2), dtype=dtype)
    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    # return the list of (x, y)-coordinates
    return coords


def eye_on_mask(mask, side):  # takes the image and the side which it will draw the eye in
    points = [shape[i] for i in side]
    points = np.array(points, dtype=np.int32)
    mask = cv2.fillConvexPoly(mask, points, 255)
    # cv2.fillConvexPoly fun. takes an image, points as a NumPy array with data type = np.int32
    # and color as arguments and returns an image with the area between those points filled with that color.
    return mask


def contouring(thresh, mid, img, right=False):
    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    try:
        cnt = max(cnts, key=cv2.contourArea)  # finding contour with maximum area (eyeball)
        M = cv2.moments(cnt)  # to find the centers of the eyeballs.
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        if right:
            cx += mid  # Adding value of mid to x coordinate of centre of
            # right eye to adjust for dividing into two parts
        cv2.circle(img, (cx, cy), 1, (0, 255, 0), -1)  # drawing over eyeball with green
        return cy, cx
    except:
        pass  # occurs when eyes are not detected


#def calc_eye_


def get_eye_ball_center(list, right=False, x=False):
    coordinate = 0
    if x:
        c = 1
    else:
        c = 0

    if right:
        x = 42
        while x <= 47:
            coordinate += list[x][c]
            x = x + 1

    else:
        x = 36
        while x <= 41:
            coordinate += list[x][c]
            x = x + 1

    # print('list entered element: ' + coordinate)

    coordinate = coordinate // 6

    # print('coordinate: ' + str(coordinate))
    return coordinate


def compare_eye_center_positions(x1, y1, x2, y2):
    print('x1: '+str(x1))
    print('x2: ' + str(x2))
    print('y1: ' + str(y1))
    print('y2: ' + str(y2))

    img1 = cv2.imread('Resources/cheater.jpg')
    if (x1 == x2) or (y1 == y2):
        cv2.destroyWindow('cheater image')
    else:
        cv2.imshow('cheater image', img1)
        cv2.waitKey(0)



def compare_eyeballs(y_left, x_left, y_right, x_right, y_center, x_center,img):
    try:
        diff_x= abs(x_left-x_right)/4
        print("diff ", diff_x)
        print('left point coord: ' + str(x_left) +','+str(y_left))
        print('right point coord: ' + str(x_right)+','+ str(y_right))
        print('center point coord: ' + str(x_center)+','+str(y_center))
        cv2.putText(img,'left : '+str(x_left)+"  center : "+ str(x_center)+ "  right : "+str(x_right),(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1)
        img1 = cv2.imread('Resources/cheater.jpg')
        if x_center-diff_x <= x_left:
            cv2.imshow('cheater image looking left', img1)
            cv2.waitKey(0)
       # elif (y_center+ 7<= y_left) or (y_center+7 <= y_right):
        #    cv2.imshow('cheater image looking up', img1)
         #   cv2.waitKey(0)
        elif x_center+diff_x >= x_right:
            cv2.imshow('cheater image looking right', img1)
            cv2.waitKey(0)
        else:
            cv2.destroyWindow('cheater image')
    except:
        pass


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('Resources/shape_68.dat')

left = [36, 37, 38, 39, 40, 41]  # keypoint indices for left eye
right = [42, 43, 44, 45, 46, 47]  # keypoint indices for right eye

cap = cv2.VideoCapture(0)
ret, img = cap.read()
# thresh = img.copy()

cv2.namedWindow('image')
kernel = np.ones((20, 20), np.uint8)  # used for dilation of eyes in the mask
process_frame = False
# def nothing(x):
#    pass
#
# cv2.createTrackbar('threshold', 'image', 0, 255, nothing)

while (True):
    image2 = np.zeros((1000, 1000, 3), np.uint8)
    ret, img = cap.read()
    if not process_frame:
        process_frame = True
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 1)  # contains all the faces detected
        # so we need to save only the person that i must track his eyes istead of saving all the faces
        # if the previous step done we will never need for-loop as we will have one face
        # print('# of detected faces: ' + str(rects))
        # rectP1 = rects.rectangles[0][0]
        # rectP2 = rects.rectangles[0][1]
        # print('rect values: ' + str(rectP1) + str(rectP2))
        # cv2.rectangle(img, rects[0][0], rects[0][1], (0, 0, 255), 3)
        # faceBoxRectangleS = tuple of dlib.rectangle(left=someNewLeftValue, top=someNewTopValue, right=someNewRightValue, bottom=someNewBottomValue)
        for rect in rects:
            shape = predictor(gray, rect)  # to predict all face objects
            shape = shape_to_np(shape)  # to convert all face objects' keypoints to (x, y)-coordinates
            # print('shape points: '+ str(shape))
            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            mask = eye_on_mask(mask, left)  # takes the left eye points to fill the space between them with white color
            mask = eye_on_mask(mask, right)
            mask = cv2.dilate(mask, kernel, 5)  # to expand the created white area
            eyes = cv2.bitwise_and(img, img, mask=mask)  # Using cv2.bitwise_and with our mask as the mask on our image,
            # we can segment out the eyes.
            # Convert all the (0, 0, 0) pixels to (255, 255, 255) so that only the eyeball is the only dark part left
            mask = (eyes == [0, 0, 0]).all(axis=2)
            eyes[mask] = [255, 255, 255]
            mid = (shape[42][0] + shape[39][0]) // 2
            eyes_gray = cv2.cvtColor(eyes, cv2.COLOR_BGR2GRAY)
            #threshold = cv2.getTrackbarPos('threshold', 'image')
            threshold = 152
            # print('threshold value is: ' + str(threshold))
            _, thresh = cv2.threshold(eyes_gray, threshold, 255, cv2.THRESH_BINARY)
            thresh = cv2.erode(thresh, None, iterations=2)  # 1
            thresh = cv2.dilate(thresh, None, iterations=4)  # 2
            thresh = cv2.medianBlur(thresh, 3)  # 3 smoothing the image
            thresh = cv2.bitwise_not(thresh)  # to find the eyeballs it need to be white and its background black
            hmadaLeft = contouring(thresh[:, 0:mid], mid, img)
            hmadaRight = contouring(thresh[:, mid:], mid, img, True)

            # Change one pixel draw left eye
            image2[shape[36][1], shape[36][0]] = (200, 0, 200)
            image2[shape[37][1], shape[37][0]] = (200, 0, 200)
            image2[shape[38][1], shape[38][0]] = (200, 0, 200)
            image2[shape[39][1], shape[39][0]] = (200, 0, 200)
            image2[shape[40][1], shape[40][0]] = (200, 0, 200)
            image2[shape[41][1], shape[41][0]] = (200, 0, 200)
            # eye_center_x = get_eye_ball_center(shape, False, True)
            # eye_center_y = get_eye_ball_center(shape)
            # image2[eye_center_x, eye_center_y] = (0, 0, 255)
            # print('place of forward ceneter: ' + str((eye_center_x, eye_center_y)))
            image2[hmadaLeft] = (255, 0, 0)
            # print('place of real time ceneter: ' + str(hmadaLeft))
            try:
                compare_eyeballs(shape[36][1], shape[36][0], shape[39][1], shape[39][0], hmadaLeft[0], hmadaLeft[1],img)
            except:
               pass
            # compare_eye_center_positions(eye_center_x, eye_center_y, hmadaLeft[0], hmadaLeft[1])

             # Change one pixel to draw right eye
            image2[shape[42][1], shape[42][0]] = (200, 0, 200)
            image2[shape[43][1], shape[43][0]] = (200, 0, 200)
            image2[shape[44][1], shape[44][0]] = (200, 0, 200)
            image2[shape[45][1], shape[45][0]] = (200, 0, 200)
            image2[shape[46][1], shape[46][0]] = (200, 0, 200)
            image2[shape[47][1], shape[47][0]] = (200, 0, 200)
             # eye_center_x = get_eye_ball_center(shape, True, True)
             # eye_center_y = get_eye_ball_center(shape, True)
             # image2[eye_center_x, eye_center_y] = (0, 0, 255)
             # print('place of forward ceneter: ' + str((eye_center_x, eye_center_y)))
            image2[hmadaRight] = (255, 0, 0)
            # print('place of real time ceneter: ' + str(hmadaRight))
            # compare_eye_center_positions(eye_center_x, eye_center_y, hmadaRight[0], hmadaRight[1])
            try:
                compare_eyeballs(shape[42][1], shape[42][0], shape[45][1], shape[45][0], hmadaRight[0], hmadaRight[1],img)
            except:
                pass
            # for (x, y) in shape[36:48]:
            #     cv2.circle(img, (x, y), 2, (255, 0, 0), -1)
        process_frame = False
    # show the image with the face detections + facial landmarks

    # Save
    # cv2.imwrite("result.png", image2)
    # cv2.imshow('eyePoints', image2)

    cv2.imshow('eyes', img)
    cv2.destroyWindow('image')
    cv2.destroyWindow('eyePoints')
    # cv2.imshow("image", thresh)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
