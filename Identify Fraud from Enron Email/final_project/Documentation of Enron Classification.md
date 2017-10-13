
## Identify Fraud in Enron Emails
Victor Lambert - October 2017

During its peak, Enron was one of the largest corporations in the United States. However, the company collapsed quickly as a result of large scale corporate fraud. This project uses the Enron corpus, a collection of emails and financial information made public during the lawsuit, to try to find persons of interest (POI) in the Enron case. Machine learning algorithms provide the ability to distinguish between POI and non-POI using this data.

In this project, a machine learning classifier is chosen, tuned, and validated for the purpose of distinguishing persons of interest from other people. In the end, the best result I found was with several different features and a Gaussian Naive Bayes classifier. The primary code for this project is contained in the file 'poi_id.py'.

### Dataset Basics

First, some basic facts about the dataset:

- total people in dataset ....... 146
- features per person .............. 21
- POI in dataset ...................... 18
- non-POI .............................. 128

In addition to there being a variety of data points available, there are several weaknesses in the data. Though there are 35 POI in total, only 18 are in the dataset. Many of the people of interest did not work directly at Enron or don't have their data available for some other reason. The algorithm will have to make due with only 18/146 positive labels, which means there is heavily skewed distribution of the classes. This will have to be taken into account when evaluating the performance of the identifier.

Several values are also missing from the dataset, represented with a 'NaN' string. Missing values will decrease the viability of features, but the algorithms will have to use other features to account for this. For example:

- number of salaries in dataset .... 95/146
- number of emails .......................111/146

Outliers are also a concern in this financial data analysis. There is one important outlier from the financial data, the name is 'TOTAL', which is clearly not a real person. The values are about an order of magnitude greater than the rest of the data, so the 'TOTAL' entry is removed from the dataset. Other high values, although different from others, have explanation in the data. For example, Jeffrey Skilling and Kenneth Lay have much higher stock and bonus values, but this is consistent with them being the CEO and chairman of the company.

### Feature Selection

From the start, I knew the algorithm would require several financial features to classify correctly. Rather than manually searching each one for patterns, I decided to use univariate selection to choose a the most important features for classification, specifically SelectKBest. I input all available financial features, the full list is:

['salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees']

In addition to using the financial features, I wanted to be able to use communication between people, particularly POIs, to help determine their status. Rather than include both emails to POIs and emails from POIs I combined them both into one feature, 'total_poi_emails', which is the sum of the from_poi emails and the to_poi emails. I hoped that the total would be a stronger predictor than one of the two alone. The code I used to create this feature is shown below.

```python
for person in data_dict:
    from_poi = data_dict[person]['from_poi_to_this_person']
    to_poi = data_dict[person]['from_this_person_to_poi']
    if from_poi == 'NaN' or to_poi == 'NaN':
        data_dict[person]['total_poi_emails'] = 'NaN'
    else:
        data_dict[person]['total_poi_emails'] = from_poi + to_poi
```

In addition to the total emails feature, I input most of the other email features as well. I excluded the email address, which is a text string so is not relevant to the machine learning classification. The full list of used email features is:

['to_messages', 'total_poi_emails', 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi']

The three algorithms I chose to test were decision trees, naive Bayes, and SVM. Though decision trees and naive Bayes do not require feature scaling, it is critical for SVM in this case. Scaling is particularly important because the values for the email features are much lower than the values for bonuses and other financial features. I employed a min/max scaling which changes each feature to a range from 0-1. This allows for better comparison of email and financial features in the SVM.

```python
if scale is True:
    print 'Using scaled dataset'
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    data = scaler.fit_transform(data)
```

A quick note is that this code doesn't output the scaling to the pickled dataset. This would be an issue if the SVM was selected as the final algorithm, but I had much better performance with both decision trees and naive Bayes so this isn't an issue.

Using SelectKBest, the features are scored and only the top several features are used in the algorithm. The scores for the features used in this classifier are listed below, ranging from bonus (30.65) to deferral_payments (0.01). During parameter tuning I used a grid search to select the ideal number of features for each algorithm. Bonus, salary, and stock value are the highest predictors of POI, and surprisingly shared_receipt_with_poi is also a very strong predictor. One interesting note is that emails from POI to a person are a much stronger predictor than emails to POI, and my combined feature falls about halfway between (although all three of these email features aren't very strong). The full list of feature importances is below.

Feature Importances:
1. 30.65 bonus
1. 15.81 salary
1. 10.81 total_stock_value
1. 10.67 shared_receipt_with_poi
1. 9.96 exercised_stock_options
1. 8.96 total_payments
1. 8.49 deferred_income
1. 8.05 restricted_stock
1. 7.53 long_term_incentive
1. 7.04 loan_advances
1. 4.94 from_poi_to_this_person
1. 4.31 expenses
1. 3.2 other
1. 2.64 total_poi_emails
1. 2.61 to_messages
1. 1.64 director_fees
1. 0.68 restricted_stock_deferred
1. 0.43 from_messages
1. 0.11 from_this_person_to_poi
1. 0.01 deferral_payments

### Algorithm Selection and Tuning

During algorithm selection I tried naive bayes, support vector machines, and decision trees using their respective scikit-learn implementations. When tuning an algorithm, it is important to balance algorithm bias with overfitting to maximize the number of points that are correctly classified. There are several methods for tuning parameters, including manual systematic tuning or automated tuning with a function like GridSearchCV. For each algorithm, I tuned the key parameters using GridSearchCV before choosing a final algorithm. Classification results depend heavily on the parameters and algorithm chosen. For all the algorithms, I allowed the grid search to select the ideal number of features, ranging from 3 to all of the given features.

During initial tests, the SVM had trouble returning any positive values for a large range of C values, although the accuracy was 0.86. Since there were no true positives returned, the precision and recall were both 0.0. C values were tried between .01 and 100, varying by factor of 10. The decision tree algorithm fared much better. The parameter tunes of the minimum sample split and number of features reached an accuracy of 0.84, with precision at 0.25 and recall at 0.20. For the decision tree, a the min_samples_split was varied from 2 to 10. With the low number of samples, all the different algorithms ran quickly.

The most successful algorithm was naive Bayes. Although naive Bayes does not require any tuning, I still used SelectKBest to find the ideal number of features to use. The ideal number of features is 6, selected the top 6 features from the list above. The local performance of the naive Bayes algorithm was good, with accuracy of 0.89, precision of 0.5, and recall of 0.6.

### Validation and Evaluation

When designing a machine learning algorithm, it is important to validate the model and quantify its performance. One key error that must be avoided is not splitting the data into testing and training sets, or accidentally training and testing the data on the same set. An ideal validation test will give a good idea of the performance of the algorithm without too much bias or overfitting.

In my naive Bayes algorithm I stuck with the standard train/test split. I considered using something more complicated, such as stratifiedKFold and performing the optimization multiple times. However, I already had achieved good performance with only the standard validation method so I decided to stick with it. For evaluation metrics I calculated accuracy, precision, and recall.

Accuracy is the total percent of samples classified correctly. This is not always a good metric to use, especially in a dataset like the Enron corpus where there are many more non-POI than POI. Better metrics to report are the precision and recall. The precision is the number of true positives divided by the total number of positives. Higher precision means that the algorithm is less likely to report false positives, in other words the positives that are reported are more likely to be true. The recall is the number of true positives divided by the number of real samples (true positives plus false negatives). The recall represents the ability of the algorithm to find the persons if interest.

When tested with the simple test/train split, the following performance is achieved:
- Accuracy ......0.89
- Precision ..... 0.50
- Recall .......... 0.60

These values are decent. The tester script uses a more accurate stratified shuffle split. Stratified shuffle split splits the data so that the percentage of each class in each portion are similar in proportion to the overall data. The values reported by the tester script are:
- Accuracy ...... 0.847
- Precision ...... 0.403
- Recall ........... 0.313
