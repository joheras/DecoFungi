import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold

def compare_methods(dataset,listAlgorithms,listParameters,listAlgorithmNames,listNiters,normalization=False):

    # Loading dataset
    df = pd.read_csv(dataset)
    data = df.ix[:, :-1].values
    labels = df.ix[:, -1].values
    kf = KFold(n_splits=10,shuffle=True,random_state=42)
    results = {name:[] for name in listAlgorithmNames}

    for i,(train_index,test_index) in enumerate(kf.split(data)):
        print "Iteration " + str(i)

        trainData , testData = data[train_index],data[test_index]
        trainLabels, testLabels = labels[train_index], labels[test_index]

        # Normalization
        if normalization:
            trainData = np.asarray(trainData).astype("float64")
            trainData -= np.mean(trainData, axis=0)
            trainData /= np.std(trainData, axis=0)
            testData = np.asarray(testData).astype("float64")
            testData -= np.mean(testData, axis=0)
            testData /= np.std(testData, axis=0)

        for clf,params,name,n_iter in zip(listAlgorithms,listParameters,listAlgorithmNames,listNiters):
            print(name)
            if params is None:
                model = clf
            else:
                model = RandomizedSearchCV(clf, param_distributions=params,n_iter=n_iter)
            model.fit(trainData, trainLabels)
            predictions = model.predict(testData)
            results[name].append(accuracy_score(testLabels, predictions))

    return results



