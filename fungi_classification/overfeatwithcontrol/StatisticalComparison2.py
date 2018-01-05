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
dataset = "output/fungi/overfeatwithcontrol-train.csv"
# Loading dataset
df = pd.read_csv(dataset)
trainData = df.ix[:,:-1].values
trainLabels = df.ix[:,-1].values
dataset = "output/fungi/overfeatwithcontrol-test.csv"
df = pd.read_csv(dataset)
testData = df.ix[:,:-1].values
testLabels = df.ix[:,-1].values


data=np.append(trainData,testData,axis=0)
labels = np.append(trainLabels,testLabels,axis=0)


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




listAlgorithms = [clfRF,clfSVC,clfGB,clfKNN,clfLR,clfMLP]
listParams = [param_distRF,param_distSVC,param_distGB,param_distKNN,param_distLR,param_distMLP]
listNames = ["Random Forest", "SVM", "Gradient Boost", "KNN", "Logistic Regression", "Neural Network"]

for i in range(5, 10):
    print("Iteration " + str(i + 1))

    # Splitting dataset
    (trainData, testData, trainLabels, testLabels) = train_test_split(data, labels, test_size=0.25, random_state=i + 1)



    for clf, params, name, n_iter in zip(listAlgorithms, listParams, listNames, [20,10,20,10,5,10]):
        if params is None:
            model = clf
        else:
            model = RandomizedSearchCV(clf, param_distributions=params, n_iter=n_iter)
        model.fit(trainData, trainLabels)
        predictions = model.predict(testData)
        print(accuracy_score(testLabels, predictions))











