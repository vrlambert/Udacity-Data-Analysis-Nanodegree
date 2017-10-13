#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

import numpy as np

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

scale = True
classifier_type = 'NB'

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi', 'total_poi_emails',
                    'salary', 'deferral_payments', 'total_payments',
                    'loan_advances', 'bonus', 'restricted_stock_deferred',
                    'deferred_income', 'total_stock_value', 'expenses',
                    'exercised_stock_options', 'other', 'long_term_incentive',
                    'restricted_stock', 'director_fees', 'to_messages',
                     'from_poi_to_this_person', 'from_messages',
                      'from_this_person_to_poi', 'shared_receipt_with_poi'] # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
data_dict.pop('TOTAL', 0)

### Task 3: Create new feature(s)

for person in data_dict:
    from_poi = data_dict[person]['from_poi_to_this_person']
    to_poi = data_dict[person]['from_this_person_to_poi']
    if from_poi == 'NaN' or to_poi == 'NaN':
        data_dict[person]['total_poi_emails'] = 'NaN'
    else:
        data_dict[person]['total_poi_emails'] = from_poi + to_poi

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
if scale is True:
    print 'Using scaled dataset'
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    data = scaler.fit_transform(data)

labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline

k_feat_choices = [3, 5, 6, 8, 12, 'all']

if classifier_type == 'DT':
    print 'Using Decision Tree'
    from sklearn.tree import DecisionTreeClassifier
    pipe = Pipeline([('kbest', SelectKBest()),
                     ('DT', DecisionTreeClassifier())])
    param_grid = {'kbest__k':k_feat_choices,
                  'DT__min_samples_split':[2, 3, 4, 5, 7, 10]}
elif classifier_type == 'SVM':
    print 'Using SVM'
    from sklearn.svm import SVC
    pipe = Pipeline([('kbest', SelectKBest()), ('svc', SVC())])
    param_grid = {'kbest__k':k_feat_choices,
                  'svc__C':[.01, .1, 1, 10, 100]}
elif classifier_type == 'NB':
    print 'Using Naive Bayes'
    from sklearn.naive_bayes import GaussianNB
    pipe = Pipeline([('kbest', SelectKBest()), ('NB', GaussianNB())])
    param_grid = {'kbest__k':k_feat_choices}
else:
    raise ValueError, 'Incorrect classifier specified'

clf = GridSearchCV(pipe, param_grid = param_grid, scoring = 'f1')
### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

clf.fit(features_train, labels_train)

print 'Feature Scores:'
for score, feature in sorted(zip(clf.best_estimator_.named_steps.kbest.scores_,
                          features_list[1:]), reverse = True):
    print round(score, 2), feature
print '\n'
pred = clf.predict(features_test)

from sklearn import metrics
print 'Accuracy:', metrics.accuracy_score(labels_test, pred)
print 'Precision:', metrics.precision_score(labels_test, pred)
print 'Recall:', metrics.recall_score(labels_test, pred)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf.best_estimator_, my_dataset, features_list)
