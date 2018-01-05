# import the necessary packages
from __future__ import print_function

import argparse
import cPickle

import numpy as np

from model.googlenet import GoogleNetExtractor
from model.utils import Conf
from model.utils import dataset

# construct the argument parser and parse the command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True, help="path to configuration file")
ap.add_argument("-i", "--image", required=True, help="path to the image to predict")
args = vars(ap.parse_args())

# load the configuration, label encoder, and classifier
print("[INFO] loading model...")
conf = Conf(args["conf"])
le = cPickle.loads(open(conf["label_encoder_path"]).read())
model = cPickle.loads(open(conf["classifier_path"]+ conf["model"] + ".cpickle").read())

imagePath = args["image"]



oe = GoogleNetExtractor()
(labels, images) = dataset.build_batch([imagePath], conf["googlenet_fixed_size"])
features = oe.describe(images)
for (label, vector) in zip(labels, features):
    prediction = model.predict(np.atleast_2d(vector))[0]
    print(prediction)
    prediction = le.inverse_transform(prediction)
    print("[INFO] predicted: {}".format(prediction))