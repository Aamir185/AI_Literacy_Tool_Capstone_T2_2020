# USAGE
# python detect_age.py --image images/adrian.png
# then the code will output a new image with age detection 
# which is named as original filename + "_output"

# import the necessary packages
import numpy as np
import argparse
import cv2
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

face_detector = os.path.join(BASE_DIR, "Scripts\\face_detector")
gender_detector = os.path.join(BASE_DIR, "Scripts\\gender_detector")

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-f", "--face", default=face_detector,
	help="path to face detector model directory")
ap.add_argument("-a", "--age", default=gender_detector,
	help="path to age detector model directory")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# define the list of age buckets our age detector will predict
AGE_BUCKETS = ["Male","Female"]

# load our serialized face detector model from disk
print("[INFO] loading face detector model...")
prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
weightsPath = os.path.sep.join([args["face"],
	"res10_300x300_ssd_iter_140000.caffemodel"])
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load our serialized age detector model from disk
print("[INFO] loading age detector model...")
prototxtPath = os.path.sep.join([args["age"], "gender_deploy.prototxt"])
weightsPath = os.path.sep.join([args["age"], "gender_net.caffemodel"])
ageNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the input image and construct an input blob for the image
image = cv2.imread(args["image"])
(h, w) = image.shape[:2]
blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300),
	(104.0, 177.0, 123.0))

# pass the blob through the network and obtain the face detections
print("[INFO] computing face detections...")
faceNet.setInput(blob)
detections = faceNet.forward()

# loop over the detections
for i in range(0, detections.shape[2]):
	# extract the confidence (i.e., probability) associated with the
	# prediction
	confidence = detections[0, 0, i, 2]

	# filter out weak detections by ensuring the confidence is
	# greater than the minimum confidence
	if confidence > args["confidence"]:
		# compute the (x, y)-coordinates of the bounding box for the
		# object
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")

		# extract the ROI of the face and then construct a blob from
		# *only* the face ROI
		face = image[startY:endY, startX:endX]
		faceBlob = cv2.dnn.blobFromImage(face, 1.0, (227, 227),
			(78.4263377603, 87.7689143744, 114.895847746),
			swapRB=False)

		# make predictions on the age and find the age bucket with
		# the largest corresponding probability
		ageNet.setInput(faceBlob)
		preds = ageNet.forward()
		i = preds[0].argmax()
		age = AGE_BUCKETS[i]
		ageConfidence = preds[0][i]

		# display the predicted age to our terminal
		text = "{}".format(age, ageConfidence * 100)
		print("[INFO] {}".format(text))

		img_output = cv2.imread(os.path.join(BASE_DIR, "media\images\output\output_image.jpg"))

		# draw the bounding box of the face along with the associated
		# predicted age
		y = startY - 10 if startY - 10 > 10 else startY + 10
		#cv2.rectangle(image, (startX, startY), (endX, endY),
		#	(0, 0, 255), 2)
		cv2.putText(img_output, text, (startX+150, y),
			cv2.FONT_HERSHEY_SIMPLEX, 1.2, (50, 41, 250), 2)

# display the output image
#cv2.imshow("Image", image)
#cv2.waitKey(0)

# output images as files
#image_filename = re.findall(r".+/(.+)\..+", args['image'])
#image_suffix = re.findall(r".+\.(.+)", args['image'])
#image_dir = re.findall(r"(.+)/.+", args['image'])

#output_filename = image_dir[0] + '/' + image_filename[0] + "_output" + '.' + image_suffix[0]
#cv2.imwrite(output_filename, image)
#print("[INFO] Image output is done, file path is \'{0}\'".format(output_filename))


output_path = os.path.join(BASE_DIR, "media\images\output\output_image.jpg")
#cv2.imwrite(output_path, image)
cv2.imwrite(output_path, img_output)
cv2.waitKey(0)