import cv2
import dlib
import numpy as np
import argparse
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())
# loading dlib front face detector
dlibDetector = dlib.get_frontal_face_detector()

# predictor is already trained dataset by dlib
pred_loc = os.path.join(BASE_DIR, "Example_1\\shape_predictor_68_face_landmarks.dat")

dlibPredictor = dlib.shape_predictor(pred_loc)

# getting image from directory
#img = cv2.imread("1.jpg")
img = cv2.imread(args["image"])
img_output = cv2.imread(os.path.join(BASE_DIR, "..\media\images\output\output_image.jpg"))

# converting image into grayscale with cv2
gray_image = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)

# Use detector to find landmarks
faceMarks = dlibDetector(gray_image)

# this loop make sure every face marks gets detected and marked
for marks in faceMarks :
    marks.left()
    marks.top()
    marks.right()
    marks.bottom()


    #creating border against marks detected on face
    landmarks = dlibPredictor (image=gray_image, box=marks)

    # Loop through all the points
    for facialmarks in range(0, 68):
        x = landmarks.part(facialmarks).x
        y = landmarks.part(facialmarks).y

        # Draw a circle
        cv2.circle(img=img_output, center=(x, y), radius=3, color=(50, 41, 250), thickness=2)

# display image with facial marks
#cv2.imshow(winname="Face", mat=img)
#cv2.waitKey(delay=0)
#cv2.destroyAllWindows()
output_path = os.path.join(BASE_DIR, "..\media\images\output\output_image.jpg")
#cv2.imshow('asas',img)
cv2.imwrite(output_path, img_output)
cv2.waitKey(0)