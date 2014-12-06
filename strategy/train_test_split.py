#!/usr/bin/python
# -*- coding: utf-8 -*-
# train_test_split.py

from sys import path
import os
path.append(os.getcwd() + '/../engine')
path.append(os.getcwd() + '/../')
import datetime
import sklearn

from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.lda import LDA
from sklearn.metrics import confusion_matrix
from sklearn.qda import QDA
from sklearn.svm import LinearSVC, SVC

from forecast import create_lagged_series

if __name__ == "__main__":
    #Create lagged series
    snpret = create_lagged_series(
        "^GSPC", datetime.datetime(2001,1,10), 
        datetime.datetime(2008,12,31), lags=5
        )
 
    #use prior two days of returns as predictor
    X = snpret[["Lag1", "Lag2", "Lag3"]]
    # direction as response
    y = snpret["Direction"]

    # Train/test split
    # 70% of data used for training and 20% used for testing
    # random_state - data is not sequentially divided, but sampled randomly
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=0.7, random_state=42
        ) 

    #create parametrised models
    print "Hit Rates/Confusion Matrices:\n"
    models = [("LR", LogisticRegression()), 
              ("LDA", LDA()), 
              ("QDA", QDA()), 
              ("LSVC", LinearSVC()), 
              ("RSVM", SVC(
                C=1000000.0, cache_size=200, class_weight=None, 
                coef0=0.0, degree=3, gamma=0.0001, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False)
                ), 
              ("RF", RandomForestClassifier(
                n_estimators=1000, criterion='gini',max_depth=None, min_samples_split=2, min_samples_leaf=1, max_features='auto', bootstrap=True, oob_score=False, n_jobs=1, random_state=None, verbose=0)
                )]

    #iterate through the models
    for m in models:
    #train each of the models 
         m[1].fit(X_train, y_train)

         #make an array of predictions on test set
         pred = m[1].predict(X_test)

         #output the hit-rate and confusion matrix for each model
         print "%s:\n%0.3f" % (m[0], m[1].score(X_test, y_test))
         print "%s\n" % confusion_matrix(pred, y_test)
    print "[[ Correct Up Period,  Incorrect Up Period]"
    print " [Incorrect Down Per,  Correct Down Period]]"

