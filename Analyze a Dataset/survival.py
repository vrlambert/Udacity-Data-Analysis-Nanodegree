# Signifcant amounts of code and inspiration taken from
# https://www.kaggle.com/helgejo/titanic/an-interactive-data-science-tutorial

import pandas as pd
import numpy as np

test = pd.read_csv('test.csv')
train = pd.read_csv('train.csv')

full = train.append( test , ignore_index = True )
titanic = full[ :891 ]

del train, test
