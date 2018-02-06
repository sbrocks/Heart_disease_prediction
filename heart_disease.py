# Importing the libraries
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

# Importing the dataset
dataset=pd.read_csv('http://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data',header=None)
#print(dataset.describe())          

# To replace ? with NaN in the dataset
dataset[[11,12]]=dataset[[11,12]].replace('?',np.NaN)

# To find no. of missing values (may not include ? ,etc ,so, check before using)
#print(dataset.apply(lambda x:sum(x.isnull()),axis=0))

X=dataset.iloc[:,:-1].values
y=dataset.iloc[:,13].values

for index,item in enumerate(y):
	if not (item==0):
		y[index]=1



# Handling missing data (11,12)
from sklearn.preprocessing import Imputer
imputer=Imputer(missing_values='NaN',strategy='mean',axis=0)
imputer=imputer.fit(X[:,11:13])
X[:,11:13]=imputer.transform(X[:,11:13])

# Splitting the dataset into Training set and Test set
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Applying LDA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
lda = LDA(n_components = 2)
X_train = lda.fit_transform(X_train, y_train)
X_test = lda.transform(X_test)


# Fitting Naive Bayes to the Training set
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

# 81.96% accuracy