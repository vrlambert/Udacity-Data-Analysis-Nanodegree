#!/usr/bin/python

import numpy
def outlierCleaner(predictions, ages, net_worths):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where
        each tuple is of the form (age, net_worth, error).
    """

    cleaned_data = []
    predictions = numpy.reshape(predictions,(len(predictions),)).tolist()
    ages = numpy.reshape(ages,(len(ages),)).tolist()
    net_worths = numpy.reshape(net_worths,(len(net_worths),)).tolist()
    for pred, age, net_worth in zip(predictions, ages, net_worths):
        error = (net_worth - pred)**2
        cleaned_data.append((age, net_worth, error))

    cleaned_data.sort(key=lambda x: x[2])
    length = int(len(cleaned_data) * 0.9)
    return cleaned_data[:length]
