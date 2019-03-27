# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 04:08:45 2019

@author: Parijat
"""
import pandas as pd
import pickle

# Importing the dataset
#dataset = pd.read_csv('amazon_cells_labelled.txt', delimiter = '\t', quoting = 3, header=None)
#dataset = pd.read_csv('imdb_labelled.txt', delimiter = '\t', quoting = 3, header=None)
dataset = pd.read_csv('yelp_labelled.txt', delimiter = '\t', quoting = 3, header=None)
# Cleaning the texts
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
corpus = []
for i in range(0, 1000):
    review = re.sub('[^a-zA-Z]', ' ', dataset[0][i])
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    review = ' '.join(review)
    corpus.append(review)

# Creating the Bag of Words model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 1500)
#cv = CountVectorizer()
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, 1].values

# Splitting the dataset into the Training set and Test set
#from sklearn.cross_validation import train_test_split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

# Accuracy function

def accuracy(confusion_matrix):
    diagonal_sum = confusion_matrix.trace()
    sum_of_all_elements = confusion_matrix.sum()
    return diagonal_sum / sum_of_all_elements 

# loading and Using the model from disk
loaded_model = pickle.load(open('NB_model.sav', 'rb'))
result = loaded_model.score(X_test, y_test)
print('\n')
print('Accuracy:',result*100,'%')