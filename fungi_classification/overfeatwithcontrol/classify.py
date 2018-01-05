import argparse
import cPickle

import cv2
import numpy as np

from model.overfeat import OverfeatExtractor
from model.utils import Conf
from model.utils import dataset

# construct the argument parser and parse the command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=False, help="path to configuration file",default="conf/fungi.json")
ap.add_argument("-i", "--image", required=False, help="path to the image to classify",default="/home/joheras/Escritorio/Research/Fungi/FungiImages/decoloracion/fucsina/control.jpg")
ap.add_argument("-t", "--control", required=False, help="path to the control image",default="/home/joheras/Escritorio/Research/Fungi/FungiImages/decoloracion/fucsina/control.jpg")
args = vars(ap.parse_args())
conf = Conf(args["conf"])

le = cPickle.loads(open(conf["label_encoder_path"]).read())
oe = OverfeatExtractor(conf["overfeat_layer_num"])
features = oe.describe(np.array([dataset.prepare_image(cv2.imread(args["image"]), conf["overfeat_fixed_size"])], dtype="float"))
featuresControl = oe.describe(np.array([dataset.prepare_image(cv2.imread(args["control"]), conf["overfeat_fixed_size"])], dtype="float"))


model = cPickle.loads(open(conf["classifier_path"]+ conf["model"] + ".cpickle").read())
prediction = model.predict_proba(np.atleast_2d(features+featuresControl))[0]
prediction = le.inverse_transform(np.argmax(prediction))
image = cv2.imread(args["image"])
cv2.putText(image, prediction, (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
		(0, 255, 0), 3)
cv2.imshow("Image", image)
cv2.waitKey(0)