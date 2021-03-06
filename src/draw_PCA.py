# copyright: yueshi@usc.edu
# modified: yutongou@usc.edu shujiayy@usc.edu xiangchl@usc.edu
import pandas as pd 
import hashlib
import os 
from utils import logger
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np


from sklearn.feature_selection import SelectFromModel
from sklearn import datasets
from sklearn.linear_model import LassoCV
from sklearn.linear_model import Lasso
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import PCA
from ggplot import *

from utils import logger

def lassoSelection(X_train, y_train, n):
	'''
	Lasso feature selection.  Select n features. 
	'''
	#lasso feature selection
	#print (X_train)
	clf = LassoCV()
	sfm = SelectFromModel(clf, threshold=0)
	sfm.fit(X_train, y_train)
	X_transform = sfm.transform(X_train)
	n_features = X_transform.shape[1]
	
	#print(n_features)
	while n_features > n:
		sfm.threshold += 0.01
		X_transform = sfm.transform(X_train)
		n_features = X_transform.shape[1]
	features = [index for index,value in enumerate(sfm.get_support()) if value == True  ]
	logger.info("selected features are {}".format(features))
	return features


if __name__ == '__main__':


	data_dir ="/Users/Tony/Desktop/"

	data_file = data_dir + "miRNA_matrix_label.csv"

	df = pd.read_csv(data_file)
	# print(df)
	y_data = df.pop('label').values

	df.pop('file_id')

	columns =df.columns
	#print (columns)
	X_data = df.values
	
	# split the data to train and test set
	X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.3, random_state=0)

	# standardize the data.
	scaler = StandardScaler()
	scaler.fit(X_train)
	X_train = scaler.transform(X_train)
	X_test = scaler.transform(X_test)

	
	# n = 100
	# features_columns = lassoSelection(X_train, y_train, n)
	# features_columns = [49, 217, 240, 285, 287, 514, 1860]
	features_columns = [9, 13, 49, 54, 71, 74, 78, 96, 107, 
	144, 149, 163, 179, 180, 185, 187, 191, 194, 195, 203, 204, 
	205, 217, 226, 240, 242, 248, 252, 253, 254, 269, 276, 282, 
	284, 285, 287, 301, 309, 316, 325, 328, 338, 342, 353, 356,
	464, 487, 490, 495, 498, 500, 505, 514, 518, 538, 588, 594, 
	631, 714, 764, 767, 768, 795, 856, 894, 897, 957, 967, 991, 
	1006, 1056, 1066, 1101, 1106, 1121, 1125, 1214, 1285, 1299, 
	1309, 1330, 1342, 1371, 1388, 1462, 1527, 1530, 1577, 1632, 
	1637, 1655, 1689, 1722, 1742, 1768, 1791, 1834, 1838, 1848, 1860]
	df = pd.DataFrame(X_train[:,features_columns],columns=features_columns)
	df["label"] = y_train
	df['label'] = df['label'].apply(lambda i: str(i))
	print(df["label"].values)
	# pca_50 = PCA(n_components=100)
	# pca_result_50 = pca_50.fit_transform(df[features_columns].values)
	# print ('Cumulative explained variation for 50 principal components: {}'.format(np.sum(pca_50.explained_variance_ratio_)))
	
	pca = PCA(n_components=3)
	pca_result = pca.fit_transform(df[features_columns].values)
	df['pca-one'] = pca_result[:,0]
	df['pca-two'] = pca_result[:,1] 
	df['pca-three'] = pca_result[:,2]

	print ('Explained variation per principal component: {}'.format(pca.explained_variance_ratio_))
	rndperm = np.random.permutation(df.shape[0])
	chart = ggplot(df.loc[rndperm[:1500],:], aes(x='pca-one', y='pca-two', color='label')) + geom_point(size=75,alpha=0.8) + ggtitle("First and Second Principal Components colored by digit")
	chart.show()




