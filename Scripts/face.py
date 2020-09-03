import numpy as np
import argparse
import cv2
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

face_detector = os.path.join(BASE_DIR, "Scripts\\face_detector")
age_detector = os.path.join(BASE_DIR, "Scripts\\age_detector")

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-f", "--face", default=face_detector, 
	help="path to face detector model directory")
ap.add_argument("-a", "--age",default=age_detector,
	help="path to age detector model directory")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

AGE_BUCKETS = ["(0-2)", "(3-11)", "(12-20)", "(21-29)", "(30-38)",
	"(39-47)", "(48-59)", "(60-100)"]

prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
weightsPath = os.path.sep.join([args["face"],
	"res10_300x300_ssd_iter_140000.caffemodel"])
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

prototxtPath = os.path.sep.join([args["age"], "age_deploy.prototxt"])
weightsPath = os.path.sep.join([args["age"], "age_net.caffemodel"])
ageNet = cv2.dnn.readNet(prototxtPath, weightsPath)

image = cv2.imread(args["image"])
(h, w) = image.shape[:2]
blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300),
	(104.0, 177.0, 123.0))

faceNet.setInput(blob)
detections = faceNet.forward()

for i in range(0, detections.shape[2]):
	confidence = detections[0, 0, i, 2]

	if confidence > args["confidence"]:
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")

		face = image[startY:endY, startX:endX]
		faceBlob = cv2.dnn.blobFromImage(face, 1.0, (227, 227),
			(78.4263377603, 87.7689143744, 114.895847746),
			swapRB=False)

		ageNet.setInput(faceBlob)
		preds = ageNet.forward()
		i = preds[0].argmax()
		age = AGE_BUCKETS[i]
		ageConfidence = preds[0][i]

		#text = "{}: {:.2f}%".format(age, ageConfidence * 100)
		text = "{}".format(age)
		print("[INFO] {}".format(text))

		y = startY - 10 if startY - 10 > 10 else startY + 10
		cv2.rectangle(image, (startX, startY), (endX, endY),
			(50, 41, 250), 3)
		#cv2.putText(image, text, (startX, y),
		#	cv2.FONT_HERSHEY_SIMPLEX, 0.8, (27, 154, 65), 2)

#cv2.imshow("Image", image)
output_path = os.path.join(BASE_DIR, "media\images\output\output_image.jpg")
cv2.imwrite(output_path, image)
cv2.waitKey(0)