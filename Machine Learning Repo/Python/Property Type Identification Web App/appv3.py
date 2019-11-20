# Serve model as a flask application

import pickle
import pandas as pd
import numpy as np
#import feature_engine
import sklearn
from flask import Flask, request, render_template
#import gmaps
import requests 

from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from geopy.geocoders import Nominatim

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

import re

#import nltk


#from sklearn.neighbors import KNeighborsRegressor


#d1=None
#capper=None
#scaler=None
#features=None
engine_svm = None
engine_nb= None
engine_rf=None
corpus_alien=None


app = Flask(__name__)


def load_corpus_alien():
    global corpus_alien
    # model variable refers to the global variable
    with open('corpus.pkl','rb') as f:
        corpus_alien=pickle.load(f)

def load_engine_svm():
    global engine_svm
    # model variable refers to the global variable
    with open('SVM_model.sav', 'rb') as f:
        engine_svm = pickle.load(f)

def load_engine_nb():
    global engine_nb
    # model variable refers to the global variable
    with open('NB_model.sav', 'rb') as f:
        engine_nb = pickle.load(f)

def load_engine_rf():
    global engine_rf
    # model variable refers to the global variable
    with open('RF_model.sav', 'rb') as f:
        engine_rf = pickle.load(f)

def most_frequent(List): 
    return max(set(List), key = List.count)


@app.route('/')
def index():
    # Connecting to a template (html file)
    return render_template('00-Basic-Template.html')
    #return "Hello World"



@app.route('/predict', methods=['GET','POST'])
def get_prediction():
    # Works only for a single sample
     if request.method == 'POST':
        #var_city = request.form['var_city']
        #print('City:',var_city)
        address = request.form['address']

        with open('apikey.txt') as f:
            api_key = f.readline()
            f.close

        address_raw=address
        adrs=re.sub('[^a-zA-Z0-9]', '', address)

        address=address+',NS,Canada'
        address_core=address

        geolocator = Nominatim(user_agent="XX")
        location = geolocator.geocode(address)
        print('type:',type(location))
        

        if type(location)!=type(None):

            aa=location.raw

            a1=aa['display_name']
            a2=aa['class']
            a3=aa['type']

            latitude=float(aa['lat'])
            longitude=float(aa['lon'])

            print(a1)

            address=a1
            a12=address.split(', ')
            name=a12[0]

            xalien=''
            if a2!='building':
                xalien=name+' '+a2+' '+a3
            elif a2=='building':
        
                    xalien=name+' '+a3
        else:
            return render_template('00-Basic-Template.html',Flag='Enter Correct Address to Proceed!')



        print(xalien)

        review = re.sub('[^a-zA-Z]', ' ', xalien)
        review = review.lower()
        review = review.split()
        ps = PorterStemmer()
        review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        corpus_alien.append(review)

        cv = CountVectorizer(max_features = 1380)
        xalien= cv.fit_transform(corpus_alien).toarray()

        x_alien=xalien[[-1]]

        yalien_NB=engine_nb.predict(x_alien)
        yalien_RF=engine_rf.predict(x_alien) 
        yalien_SVM=engine_svm.predict(x_alien)

        yalien_list=[yalien_NB[0],yalien_RF[0],yalien_SVM[0]]

        yalien=most_frequent(yalien_list)

        prediction=''
        if yalien==0:
            prediction=' Residential'
        elif yalien==1:
            prediction=' Commercial'

        print(address)
        print(a1)
        print(yalien_list)
            
        return render_template('map.html',address=address_core, latitude=round(latitude,7),longitude=round(longitude,7),pred=prediction)
'''

        if 'photo_reference' in data33['candidates'][0]['photos'][0].keys():    
            photoreference=data33['candidates'][0]['photos'][0]['photo_reference']
            print(photoreference)
        else:
            photoreference=''
            r4=400


        if photoreference!='':

            URL4='https://maps.googleapis.com/maps/api/place/photo'

            PARAMS4 = {'photoreference':photoreference,'maxwidth':400,'key':api_key}

            r4 = requests.get(url = URL4, params = PARAMS4)

            if r4.status_code == 200:
                file=a12[0]+'.'+'jpg'
                with open(file, 'wb') as f:
                    f.write(r4.content)
            else:
                file_alt='download.jpg'

        #address= name+','+address_core

     #return render_template('map.html',address=address, latitude=round(latitude,7),longitude=round(longitude,7),pred=prediction,llp=lat_long_price)
     if (r4.status_code != 200) or (photoreference==''):
        return render_template('map.html',address=address_core, latitude=round(latitude,7),longitude=round(longitude,7),pred=prediction,pic=file_alt)
     elif r4.status_code == 200:
        return render_template('map.html',address=address_core, latitude=round(latitude,7),longitude=round(longitude,7),pred=prediction,pic=file)

'''



if __name__ == '__main__':    
    #load_mapdict()
    #load_outlier_capper()
    #load_scaler()
    #load_features()
    load_corpus_alien()
    load_engine_nb()
    load_engine_rf()
    load_engine_svm()


    # load model at the beginning once only
    #app.run(host='0.0.0.0', port=80)
    #app.run(port=80, debug=True)
    app.run(host='127.0.0.1',port=5000, debug=True)
    #app.run(host='0.0.0.0',port=5000, debug=True)
