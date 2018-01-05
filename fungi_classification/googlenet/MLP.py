#=======================================================================================================================
# Multilayer perceptron is given in a separate file since it is not available in the python version employed in
# the other files.
#=======================================================================================================================

from sklearn.cross_validation import train_test_split

from sklearn.model_selection import RandomizedSearchCV

from scipy.stats import randint as sp_randint
from time import time
from sklearn.metrics import classification_report,accuracy_score,roc_auc_score
from sklearn.ensemble import AdaBoostClassifier
from random import sample
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np

# Fixing some variables
dataset = "output/fungi/googlenet-train.csv"
# Loading dataset
df = pd.read_csv(dataset)
trainData = df.ix[:,:-1].values
trainLabels = df.ix[:,-1].values
dataset = "output/fungi/googlenet-test.csv"
df = pd.read_csv(dataset)
testData = df.ix[:,:-1].values
testLabels = df.ix[:,-1].values




#================================================================================================================
print("MultiLayer Perceptron")
#================================================================================================================

from sklearn.neural_network import MLPClassifier
clf = MLPClassifier(random_state=84)
n_iter_search = 20
param_dist = {'activation':['identity', 'logistic', 'tanh', 'relu'], 'solver':['lbgfs','sgd','adam'],
              'alpha': sp_randint(0.0001, 1),'learning_rate':['constant','invscaling','adaptive'],'momentum':[0.9,0.95,0.99]}
model = RandomizedSearchCV(clf, param_distributions=param_dist,
                                   n_iter=n_iter_search)

model.fit(trainData, trainLabels)
predictionsMLP = model.predict(testData)
print(classification_report(testLabels,predictionsMLP))
print(accuracy_score(testLabels,predictionsMLP))
