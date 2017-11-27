# Signifcant amounts of code and inspiration taken from
# https://www.kaggle.com/helgejo/titanic/an-interactive-data-science-tutorial

import pandas as pd
import numpy as np

test = pd.read_csv('test.csv')
train = pd.read_csv('train.csv')

full = train.append( test , ignore_index = True )
titanic = full[ :891 ]

del train, test

# Data preparation using numpy and pandas
sex = pd.Series( np.where( full.Sex == 'male' , 1 , 0 ) , name = 'Sex' )
embarked = pd.get_dummies( full.Embarked , prefix='Embarked' )
pclass = pd.get_dummies( full.Pclass , prefix='Pclass' )

# Fill missing values
# Create dataset
imputed = pd.DataFrame()

# Fill missing values of Age with the average of Age (mean)
imputed[ 'Age' ] = full.Age.fillna( full.Age.mean() )

# Fill missing values of Fare with the average of Fare (mean)
imputed[ 'Fare' ] = full.Fare.fillna( full.Fare.mean() )

print imputed.head()
