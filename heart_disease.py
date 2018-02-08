# Importing the libraries
import sys,json
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

def read_in():
	lines=sys.stdin.readlines()
	return json.loads(lines[0])

def main():
	lines=read_in()
	np_lines=np.array(lines)
	np_lines=np_lines.reshape(1,-1)
	dataset=pd.read_csv('http://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data',header=None)
	dataset[[11,12]]=dataset[[11,12]].replace('?',np.NaN)
	X=dataset.iloc[:,:-1].values
	y=dataset.iloc[:,13].values
	for index,item in enumerate(y):
		if not (item==0):
			y[index]=1

	from sklearn.preprocessing import Imputer
	imputer=Imputer(missing_values='NaN',strategy='mean',axis=0)
	imputer=imputer.fit(X[:,11:13])
	X[:,11:13]=imputer.transform(X[:,11:13])
	from sklearn.preprocessing import StandardScaler
	sc = StandardScaler()
	X_train = sc.fit_transform(X) 
	X_test = sc.transform(np_lines)
	from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
	lda = LDA(n_components = 2)
	X_train = lda.fit_transform(X_train, y)
	X_test = lda.transform(X_test)
	from sklearn.naive_bayes import GaussianNB
	classifier = GaussianNB()
	classifier.fit(X_train, y)
	y_pred = classifier.predict(X_test)
	print(y_pred[0])

if __name__ == '__main__':
	main()

# 81.96% accuracy