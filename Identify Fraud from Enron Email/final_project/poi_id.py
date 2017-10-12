#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi', 'total_poi_emails',
                    'bonus', 'salary', 'total_stock_value', 'expenses',
                    'exercised_stock_options', 'long_term_incentive'] # You will need to use more features

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
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline

pipe = Pipeline([('kbest', SelectKBest()), ('NB', GaussianNB())])
param_grid = {'kbest__k':[1, 2, 3, 5, 'all']}
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
