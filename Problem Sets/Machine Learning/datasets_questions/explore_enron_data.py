#!/usr/bin/python

"""
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000

"""

import pickle

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))

poi = 0
total_paynan = 0
for person in enron_data:
    data = enron_data[person]
    if data['poi'] is True:
        poi += 1
        if data['total_payments'] == 'NaN':
            total_paynan += 1

print 'poi: ', poi
print 'total_paynan: ', total_paynan
print total_paynan / float(poi)
