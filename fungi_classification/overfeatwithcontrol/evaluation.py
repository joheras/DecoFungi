# import the necessary packages
from __future__ import print_function

import argparse
import cPickle

import numpy as np
from imutils import paths
from sklearn.metrics import accuracy_score

from model.overfeat import OverfeatExtractor
from model.utils import Conf
from model.utils import dataset

# construct the argument parser and parse the command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True, help="path to configuration file")
args = vars(ap.parse_args())

# load the configuration, label encoder, and classifier
print("[INFO] loading model...")
conf = Conf(args["conf"])
le = cPickle.loads(open(conf["label_encoder_path"]).read())
model = cPickle.loads(open(conf["classifier_path"]+ conf["model"] + ".cpickle").read())

imagePaths = list(paths.list_images(conf["evaluation_path"]))

oe = OverfeatExtractor()
(truelabels, images) = dataset.build_batch(imagePaths, conf["overfeat_fixed_size"])
features = oe.describe(images)
controlImages = dataset.build_batch_control_evaluation(imagePaths, conf["overfeat_fixed_size"])
featuresControl = oe.describe(controlImages)
features = [x+y for (x,y) in zip(features,featuresControl)]

truelabels = [x[0:x.find(':')] for x in truelabels]
labels = []
for (label, vector) in zip(truelabels, features):
    prediction = model.predict(np.atleast_2d(vector))[0]
    print(prediction)
    prediction = le.inverse_transform(prediction)
    labels.append(prediction)
    print("[INFO] predicted: {}, true label: {}".format(prediction,label))

print(accuracy_score(truelabels,labels))