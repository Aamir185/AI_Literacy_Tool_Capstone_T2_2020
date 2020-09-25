import cv2
import dlib

# loading dlib front face detector
dlibDetector = dlib.get_frontal_face_detector()

# predictor is already trained dataset by dlib
dlibPredictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# getting image from directory
img = cv2.imread("1.jpg")

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
        cv2.circle(img=img, center=(x, y), radius=3, color=(0, 255, 255), thickness=0)

# display image with facial marks
cv2.imshow(winname="Face", mat=img)
cv2.waitKey(delay=0)
cv2.destroyAllWindows()