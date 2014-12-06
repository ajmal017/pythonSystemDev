#!/usr/bin/python
# -*- coding: utf-8 -*-
# grid_search.py

from sys import path
import os
path.append(os.getcwd() + '/../engine')
path.append(os.getcwd() + '/../')
import datetime
import pandas as pd
import sklearn

from sklearn import cross_validation
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import LinearSVC, SVC

from forecast import create_lagged_series

if __name__ == "__main__":
    #Create lagged series
    snpret = create_lagged_series(
        "^GSPC", datetime.datetime(2001,1,10), 
        datetime.datetime(2005,12,31), lags=5
        )
 
    #use prior two days of returns as predictor
    X = snpret[["Lag1", "Lag2"]]
    # direction as response
    y = snpret["Direction"]
    
    # Train/test split
    # 50% of data used for training and 50% used for testing
    # random_state - data is not sequentially divided, but sampled randomly
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.5, random_state=42
        ) 
        
    """ Set the parameters by cross-validation
    This will create a cartesian product of all parameter lists, a list of
    every possible parameter combination. 
    list(ParameterGrid(tuned_parameters))
    """
    tuned_parameters = [
        {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}
        ]
    
    model = GridSearchCV(SVC(C=1), tuned_parameters, cv=10)
    model.fit(X_train, y_train)
    
    print "Optimised parameters found on this training set:"
    print model.best_estimator_, "\n"
    
    print "Grid scores calculated on training set:"
    for params, mean_score, scores in model.grid_scores_:
        print "%0.3f for %r" % (mean_score, params)
    
    
