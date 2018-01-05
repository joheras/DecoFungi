import argparse
import cPickle

import cv2
import numpy as np
from scipy.spatial import distance

from model.googlenet import GoogleNetExtractor
from model.utils import Conf
from model.utils import dataset

# construct the argument parser and parse the command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=False, help="path to configuration file",default="conf/fungi.json")
ap.add_argument("-i", "--image", required=False, help="path to the image to classify",default="/home/joheras/Escritorio/Research/Fungi/FungiImages/decoloracion/naranja/+++/2.jpg")
ap.add_argument("-t", "--control", required=False, help="path to the control image",default="/home/joheras/Escritorio/Research/Fungi/FungiImages/decoloracion/naranja/control.jpg")
ap.add_argument("-p", "--plain", required=False, help="path to the plain image",default="/home/joheras/Escritorio/Research/Fungi/FungiImages/plain.jpg")
args = vars(ap.parse_args())
conf = Conf(args["conf"])

control = cv2.imread(args["control"])
control = cv2.resize(control, (100, 100))
plain = cv2.imread(args["plain"])
plain = cv2.resize(plain, (100, 100))
image = cv2.imread(args["image"])
image = cv2.resize(image, (100, 100))


le = cPickle.loads(open(conf["label_encoder_path"]).read())
oe = GoogleNetExtractor()
features = oe.describe(np.array([dataset.prepare_image(cv2.imread(args["image"]), conf["googlenet_fixed_size"])], dtype="float"))


model = cPickle.loads(open(conf["classifier_path"]+ conf["model"] + ".cpickle").read())
prediction = model.predict_proba(np.atleast_2d(features))[0]
prediction = le.inverse_transform(np.argmax(prediction))




# Construct the different ranges depending on the classification
if prediction=='-':
	combinations = [(control * float(100-n) / 100 + plain * float(n) / 100).astype("uint8") for n in
				range(0, 26, 1)]
	combinationPercentage = [n for n in range(0, 26, 1)]
elif prediction=='+':
	combinations = [(control * float(100 - n) / 100 + plain * float(n) / 100).astype("uint8") for n in
					range(25,51, 1)]
	combinationPercentage = [n for n in range(25,51, 1)]
elif prediction=='++':
	combinations = [(control * float(100 - n) / 100 + plain * float(n) / 100).astype("uint8") for n in
					range(50, 76, 1)]
	combinationPercentage = [n for n in range(50, 76, 1)]
elif prediction=='+++':
	combinations = [(control * float(100 - n) / 100 + plain * float(n) / 100).astype("uint8") for n in
					range(75, 101, 1)]
	combinationPercentage = [n for n in range(75, 101, 1)]

imageLAB = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
histLAB = cv2.calcHist([imageLAB], [0,1,2], None, [8,8,8], [0,256,0,256,0,256])
histLAB = cv2.normalize(histLAB).flatten()
histsLAB = [cv2.normalize(
	cv2.calcHist([cv2.cvtColor(im, cv2.COLOR_BGR2LAB)], [0,1,2], None, [8,8,8], [0,256,0,256,0,256])).flatten() for im in combinations]
# Compare histograms
comparisonLABeuclidean = [distance.euclidean(histLAB, histLAB2) for histLAB2 in histsLAB]
print(comparisonLABeuclidean)
mins = np.where(np.asarray(comparisonLABeuclidean) == np.asarray(comparisonLABeuclidean).min())

for m in mins:
	print("Decolourization: " + str(combinationPercentage[m]) + "%")

cv2.putText(image, prediction, (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
		(0, 255, 0), 3)
cv2.imshow("Image", image)
cv2.waitKey(0)