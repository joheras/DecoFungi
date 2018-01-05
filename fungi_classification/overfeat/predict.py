# import the necessary packages
from __future__ import print_function
from model.utils import Conf
from model.overfeat import OverfeatExtractor
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
    #print("[INFO] loading model...")
    conf = Conf("/home/joheras/pythonprojects/api/cv_api/fungi_classification/overfeat/conf/fungi.json")
    le = cPickle.loads(open(conf["label_encoder_path"]).read())
    model = cPickle.loads(open(conf["classifier_path"]+ conf["model"] + ".cpickle").read())

    imagePaths = list(paths.list_images(conf["evaluation_path"]))

    image = dataset.prepare_image(image, conf["overfeat_fixed_size"])
    features = oe.describe([image])
    #truelabels = [x[0:x.find(':')] for x in truelabels]
    prediction = model.predict(np.atleast_2d(features[0]))[0]
    prediction = le.inverse_transform(prediction)
    return prediction