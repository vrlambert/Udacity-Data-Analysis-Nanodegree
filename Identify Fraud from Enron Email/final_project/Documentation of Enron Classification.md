
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

From the start, I knew the algorithm would require several financial features to classify correctly. Rather than manually searching each one for patterns, I decided to used automatic selection to choose a the most important features for classification, such as SelectKBest. I didn't input all the financial features, only those that I personally felt would correlate well with increased knowledge or participation in the fraud. The financial features I added for possible use are:

- 'salary'
- 'bonus'
- 'exercised_stock_options'
- 'total_stock_value',
- 'long_term_incentive'
- 'expenses'

In addition to using the financial features, I wanted to be able to use communication between people, particularly POIs to help determine their status. Rather than include both emails to POIs and emails from POIs I combined them both into one feature, 'total_poi_emails', which is the sum of the from_poi emails and the to_poi emails. The code I used to create this feature is shown below.

```python
for person in data_dict:
    from_poi = data_dict[person]['from_poi_to_this_person']
    to_poi = data_dict[person]['from_this_person_to_poi']
    if from_poi == 'NaN' or to_poi == 'NaN':
        data_dict[person]['total_poi_emails'] = 'NaN'
    else:
        data_dict[person]['total_poi_emails'] = from_poi + to_poi
```

Since I chose a naive Bayes classifier, feature scaling was not required. However, if I had chosen an algorithm where distance or margin is important, such as SVM, feature scaling would have been critical.

Using SelectKBest, the features are scored and only the top several features are used in the algorithm. The scores for the features used in this classifier are listed below, ranging from bonus (17.0) to long_term_incentive (0.5). Using a grid search to find the optimal number of features selected 5. The features selected therefore are bonus, total POI emails, expense, exercised stock options, and salary. Surprisingly, expenses was a higher predictor of being a POI than salary or stock options.

Feature Importances:
1. bonus ............................... 17.0
2. total_poi_emails ............... 10.6
3. expenses ........................... 9.3
4. exercised_stock_options ... 3.0
5. salary ................................. 2.3
6. total_stock_value ............... 2.1
7. long_term_incentive .......... 0.5

### Algorithm Selection and Tuning

During algorithm selection I tried naive Bayes, support vector machines, and decision trees using their respective scikit-learn implementations. For each algorithm, I tuned the key parameter before choosing a final algorithm. When tuning an algorithm, it is important to balance algorithm bias with overfitting to maximize the number of points that are correctly classified. There are several methods for tuning parameters, including manual systematic tuning or automated tuning with a function like GridSearchCV. Classification results depend heavily on the parameters and algorithm chosen.

During initial tests, the SVM had trouble returning any positive values even with very high C values, although the accuracy was about 0.9. C values were tried between .01 and 1000, varying by factor of 10. The decision tree algorithm fared much better. Some of the parameter tunes of the minimum sample split and number of samples reached an accuracy of about 0.8, with precision and recall both just above 0.3. With the low number of samples, all the different algorithms ran quickly.

The most successful algorithm was naive Bayes. Although naive Bayes does not require any tuning, I still used SelectKBest to find the ideal number of features to use. The ideal number of features is 5, eliminating total stock value and long term incentive.

### Validation and Evaluation

When designing a machine learning algorithm, it is important to validate the model and quantify its performance. One key error that must be avoided is not splitting the data into testing and training sets, or accidentally training and testing the data on the same set. An ideal validation test will give a good idea of the performance of the algorithm without too much bias or overfitting.

In my naive Bayes algorithm I stuck with the standard train/test split. I considered using something more complicated, such as stratifiedKFold and performing the optimization multiple times. However, I already had achieved good performance with only the standard validation method so I decided to stick with it. For evaluation metrics I calculated accuracy, precision, and recall.

Accuracy is the total percent of samples classified correctly. This is not always a good metric to use, especially in a dataset like the Enron corpus where there are many more non-POI than POI. Better metrics to report are the precision and recall. The precision is the number of true positives divided by the total number of positives. Higher precision means that the algorithm is less likely to report false positives, in other words the positives that are reported are more likely to be true. The recall is the number of true positives divided by the number of real samples (true positives plus false negatives). The recall represents the ability of the algorithm to find the persons if interest.

When tested with the simple test/train split, the following performance is achieved:
- Accuracy ......0.79
- Precision ..... 0.33
- Recall ............ 0.5

These values are decent. The tester script uses a more accurate stratified shuffle split. Stratified shuffle split splits the data so that the percentage of each class in each portion are similar in proportion to the overall data. The values reported by the tester script are:
- Accuracy ...... 0.84650
- Precision ...... 0.45184
- Recall ........... 0.34950
