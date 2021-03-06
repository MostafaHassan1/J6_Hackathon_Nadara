# J6_Hackathon_Nadara


## Team Members
- Team Leader : Mostafa Hassan
- Team Member 1 : Mohanad Shawky
- Team Member 2 : Amira Abd El-Azeem
- Team Member 3 : Omnya Hosny

## Problem Statement 

Online Examination Application with face recognition to detect cheating by false identity or group attendance,
 and also using eye tracking to try to detect if someone is looking to the far right or left for reading something not on the computer he/she using   
## Solution

* Steps taken for solving the problem.
  - For face recognition
    - We take a picture of the student to encode and add it to our database so we can recognize him
    - In the live video we take the student face and encode it 
    - We compare his encoding to the rest of the encodings to see if there is a match
    - For performance wise, the face recognition and encodings only works every 60 frame (~1sec) 
  - For group attendance
    - We detect how many faces in the live feed 
    - If there is more than one we show a cheater detected image
    - For performance wise, the face recognition and encodings only works every 30 frame (~500ms) 

  - For eye tracking (Not very high accuracy, because we are using a standard laptop camera)
    - We first detect the eyes by using the dlib 68-face-points model detector 
    - Use a threshold trackbar until the eyes's pupil is the only white part in the image
    - Use dilation, erosion and median blur to make the contour bigger and clearer
    - Using blob area calculation to detect the center of the blob shape of the eyes
    - We check if the center is close to the 68-face-points that corresponds to the eyes left or right boundaries
    - If it's close, then the student is cheating by looking away from the screen
    
* We used python with openCV, dlib and face-recognition libraries  
* For why we choose those libraries 
    - openCV is fast, well documented and has a huge community behind it
    - dlib has pretrained models that is fast and has a huge accuracy (our face recognition accuracy is 98%)
    - face-recognition is built on top of dlib and uses the same models but with more simplified functions and less code  
## Methodology 

  * The architecture of the project is simple we only have a single table database that holds the image's encode and person name
  * We didn't use any dataset since we have a pretrained models
  * The dlib face recognition model that we used has 98% accuracy 
## System Architecture proposal

  * We used a standard laptop camera with openCV to open the camera and take the frames. 

## Steps to run the software

* We first need to install python, c++ compiler, cmake c++ tools

* Python Libs: opencv-python, cmake, dlib, face-recognition (the order is important), and pymysql for the database

* You need to open your mysql server, change the database configs in DB.py and then run that file

* If you want to add a person to the database, run NewPerson.py

* For simplicity if you don't want to use the database, if you want you can just run the code but you have to put your student image in a dirct. : Resources/Students_images (or change that path in main_face_recognition.py load_images function), and also in the VideoCap.init change the lines as described in the comment

* To run the face recognition run main.py, for eye tracking run eyeTracking.py