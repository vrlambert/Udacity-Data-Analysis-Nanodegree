#!/usr/bin/python

"""
    This is the code to accompany the Lesson 1 (Naive Bayes) mini-project.

    Use a Naive Bayes Classifier to identify emails by their authors

    authors and labels:
    Sara has label 0
    Chris has label 1
"""

import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()




#########################################################
def classify(features_train, labels_train):
    ### import the sklearn module for GaussianNB
    classifier = GaussianNB()
    t0 = time()
    classifier.fit(features_train, labels_train)
    print "training time:", round(time()-t0, 3), "s"
    return classifier

clf = classify(features_train, labels_train)
t1 = time()
pred = clf.predict(features_test)
print "pred time:", round(time() - t1, 3), "s"
print accuracy_score(pred, labels_test)
#########################################################
