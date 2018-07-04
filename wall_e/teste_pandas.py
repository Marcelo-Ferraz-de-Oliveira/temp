import pandas as pd

'male' = 1
'female' = 2
'S' = 1
'Q' = 2
"C" = 3

dataframe = pd.read_csv("/media/sf_Dados_Bolsa_Wall_e/Titanic/train.csv")
dataframe = dataframe.fillna(0)
Y_train = dataframe['Survived']
X_train = dataframe.drop(['Survived','Name'],axis=1)
print(X_train)
#X_train.replace()

#print(Y_train.head())
#print(X_train.head())
#for feat in X_train:
#    print(feat)

#print(dataframe)

#import numpy as np
from matplotlib import pyplot as plt
#clients = 
#plt.scatter(X_train['Age'],Y_train, alpha=0.25, c=Y_train)
#plt.scatter(X_train['Fare'],Y_train, alpha=0.25, c=Y_train)
#plt.show()

from sklearn import tree
clf = tree.DecisionTreeClassifier()
#clf = clf.fit(X_train,Y_train)

#print(clf.score(X_train,Y_train))