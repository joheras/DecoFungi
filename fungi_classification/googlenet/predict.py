# import the necessary packages
from __future__ import print_function
from model.utils import Conf
import numpy as np
import argparse
from model.utils import dataset
import cPickle
from sklearn.metrics import accuracy_score
import h5py
from imutils import paths
import cv2


def categoryOfFungiImage(image, oe):
    # load the configuration, label encoder, and classifier
    print("[INFO] loading model...")
    conf = Conf("/home/joheras/pythonprojects/api/cv_api/fungi_classification/googlenet/conf/fungi.json")
    le = cPickle.loads(open(conf["label_encoder_path"]).read())
    model = cPickle.loads(open(conf["classifier_path"]+ conf["model"] + ".cpickle").read())
    image = dataset.prepare_image(image, conf["googlenet_fixed_size"])
    features = oe.describe([image])
    prediction = model.predict(np.atleast_2d(features[0]))[0]
    prediction = le.inverse_transform(prediction)
    return prediction