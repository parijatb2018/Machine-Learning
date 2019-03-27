# Natural Language Processing

# Importing the libraries
#import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
import pickle

# Importing the dataset
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

# Naive Bayes Classifier------------------------>>>
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

print('NB Accuracy:',accuracy(cm)*100,'%')

# saving the DT model 
filename = 'NB_model.sav'
pickle.dump(classifier, open(filename, 'wb'))

''' >>> Use this block for testing Accuracy
# loading and Using the model from disk
loaded_model = pickle.load(open('NB_model.sav', 'rb'))
result = loaded_model.score(X_test, y_test)
print(result)

'''


#Random Forest Classifier------------------------------>>>
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

print('RF Accuracy:',accuracy(cm)*100,'%')

# saving the DT model 
filename = 'RF_model.sav'
pickle.dump(classifier, open(filename, 'wb'))

''' >>> Use this block for testing Accuracy
# loading and Using the model from disk
loaded_model = pickle.load(open('RF_model.sav', 'rb'))
result = loaded_model.score(X_test, y_test)
print(result)

'''

# Decision Tree Classifier----------------------------->>>
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier(criterion = 'entropy', min_samples_split=10, random_state = 0)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

print('DT Accuracy:',accuracy(cm)*100,'%')


# saving the DT model 
filename = 'DT_model.sav'
pickle.dump(classifier, open(filename, 'wb'))

''' >>> Use this block for testing Accuracy
# loading and Using the model from disk
loaded_model = pickle.load(open('DT_model.sav', 'rb'))
result = loaded_model.score(X_test, y_test)
print(result)

'''







