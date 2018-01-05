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
from sklearn.cross_validation import train_test_split
from scipy.stats import randint as sp_randint
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import scipy
from sklearn.neighbors import KNeighborsClassifier

# Fixing some variables
dataset = "output/fungi/googlenetwithcontrol.csv"
# Loading dataset
df = pd.read_csv(dataset)
data = df.ix[:, :-1].values
labels = df.ix[:, -1].values
(trainData, testData, trainLabels, testLabels) = train_test_split(data, labels, test_size=0.25, random_state=42)
#================================================================================================================
print("RandomForest")
#================================================================================================================
clfRF = RandomForestClassifier(random_state=84,n_estimators=20)

# specify parameters and distributions to sample from
param_distRF = {"max_depth": [3, None],
              "max_features": sp_randint(1, min(11,len(trainData[0]))),
              "min_samples_leaf": sp_randint(1, 11),
              "bootstrap": [True, False],
              "criterion": ["gini", "entropy"]}


#================================================================================================================
print("SVM")
#================================================================================================================

clfSVC = SVC(random_state=84)
# specify parameters and distributions to sample from
param_distSVC = {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001],
  'kernel': ['rbf'], 'class_weight':['balanced', None]}


#================================================================================================================
print("KNN")
#================================================================================================================

param_distKNN = {'n_neighbors':sp_randint(3, 30)}
clfKNN = KNeighborsClassifier()


#================================================================================================================
print("Logistic Regression")
#================================================================================================================

clfLR = LogisticRegression(random_state=84)
param_distLR = {'C': [0.1,0.5,1, 10, 100, 1000]}


#================================================================================================================
print("MultiLayer Perceptron")
#================================================================================================================


clfMLP = MLPClassifier(random_state=84)

param_distMLP = {'activation':['identity', 'logistic', 'tanh', 'relu'], 'solver':['lbgfs','sgd','adam'],
              'alpha': sp_randint(0.0001, 1),'learning_rate':['constant','invscaling','adaptive'],'momentum':[0.9,0.95,0.99]}


#================================================================================================================
print("Gradient Boost")
#================================================================================================================
clfGB = GradientBoostingClassifier(random_state=84,n_estimators=20)

# specify parameters and distributions to sample from
param_distGB = {"max_depth": [3, None],
              "max_features": sp_randint(1, min(11,len(trainData[0]))),
              "min_samples_leaf": sp_randint(1, 11),
              "criterion": ["friedman_mse", "mse", "mae"]}




listAlgorithms = [clfRF,clfSVC,clfKNN,clfLR,clfMLP]
listParams = [param_distRF,param_distSVC,param_distKNN,param_distLR,param_distMLP]
listNames = ["RF", "SVM", "KNN", "LR", "MLP"]
from Comparing import compare_methods
results = compare_methods(dataset,listAlgorithms,listParams,listNames,[20,10,10,5,10],normalization=False)

df = pd.DataFrame.from_dict(results,orient='index')
df.to_csv('../results'+dataset[dataset.rfind("/"):])












