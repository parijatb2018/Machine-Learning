# Serve model as a flask application

import pickle
import pandas as pd
import numpy as np
import feature_engine
import sklearn
from flask import Flask, request, render_template
#import gmaps
import requests 

from sklearn.neighbors import KNeighborsRegressor


d1=None
capper=None
scaler=None
features=None
engine = None
engine_rf= None
engine_KNN=None
features_rf=None


app = Flask(__name__)



def load_mapdict():
    global d1
    # model variable refers to the global variable
    with open('mapdict.pkl', 'rb') as f:
        d1 = pickle.load(f)

def load_outlier_capper():
    global capper
    # model variable refers to the global variable
    with open('outlier_capper.pkl', 'rb') as f:
        capper = pickle.load(f)

def load_scaler():
    global scaler
    # model variable refers to the global variable
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

def load_features():
    global features
    # model variable refers to the global variable
    with open('features.pkl', 'rb') as f:
        features = pickle.load(f)

def load_engine():
    global engine
    # model variable refers to the global variable
    with open('engine.pkl', 'rb') as f:
        engine = pickle.load(f)

def load_engine_rf():
    global engine_rf
    # model variable refers to the global variable
    with open('engine_rf.pkl', 'rb') as f:
        engine_rf = pickle.load(f)

def load_engine_KNN():
    global engine_KNN
    # model variable refers to the global variable
    with open('engine_KNN.pkl', 'rb') as f:
        engine_KNN = pickle.load(f)

def load_features_rf():
    global features_rf
    # model variable refers to the global variable
    with open('features_rf.pkl', 'rb') as f:
        features_rf = pickle.load(f)


@app.route('/')
def index():
    # Connecting to a template (html file)
    return render_template('00-Basic-Template.html')
    #return "Hello World"



@app.route('/predict', methods=['GET','POST'])
def get_prediction():
    # Works only for a single sample
     if request.method == 'POST':
        var_city = request.form['var_city']
        print('City:',var_city)
        address = request.form['address']

        with open('apikey.txt') as f:
            api_key = f.readline()
            f.close

        #address=address= address+','+var_city+','+'ON, Canada'
        #1743 Arthur St E

        if address!='':
            address=address
            print('address:',address)
        elif (address=='') and (var_city=='Rare'):
            print('am here')
            return render_template('00-Basic-Template.html',Flag='Enter The Address to Proceed!')
        elif (address=='') and (var_city!='Rare'):
            print('address:',address)
            address=var_city

        URL = 'https://maps.googleapis.com/maps/api/geocode/json'
        PARAMS = {'address':address, 'key':api_key}
        r = requests.get(url = URL, params = PARAMS)
        data2 = r.json()

        if data2['status']=='OK':
            for xx in data2['results'][0]['address_components']:
                if xx['types'][0]=='administrative_area_level_1':
                    if xx['long_name']=='Ontario':
                        print(xx['long_name'])
                        Tag1=True
                    else:
                        Tag1=False

            for xx in data2['results'][0]['address_components']:
                if xx['types'][0]=='locality':
                    if xx['long_name']==var_city:
                        print(xx['long_name'])
                        Tag2=True
                    else:
                        Tag2=False
                        var_city=xx['long_name']
                        print(xx['long_name'])
            # extracting latitude, longitude and formatted address 
            # of the first matching location 
            #print('status',data2['status'])
            print(Tag1,Tag2)
            if (Tag1==True) or (Tag2==True):
                latitude = data2['results'][0]['geometry']['location']['lat'] 
                longitude = data2['results'][0]['geometry']['location']['lng'] 
                address= address+','+var_city+','+'ON, Canada'
                print(latitude,longitude)
    
            else:
                print('status',data2['status'])
                return render_template('00-Basic-Template.html',Flag='Enter Correct Address!')#,approxage=approxage)
            #print('status',data2['status'])
            #print('Enter Corrct Address')

        #var_list=request.form.get('myList')


        
        var_approxage = request.form['var_approxage']
        var_approxsqft = request.form['var_approxsqft']
        var_propertynew = request.form['var_propertynew']
        var_bedroomstotal = int(request.form['var_bedroomstotal'])
        var_kitchens = int(request.form['var_kitchens'])
        var_washrooms = int(request.form['var_washrooms'])
        var_maintenancefee = float(request.form['var_maintenancefee'])
        var_lifeofad = int(request.form['var_lifeofad'])

        var_city=var_city[0].upper()+var_city[1:].lower()
        if var_city in d1['city'].keys() and d1['city']!='Rare':
            var_city= int(d1['city'][var_city])
        else:
            var_city= int(d1['city']['Rare'])

        if var_approxage in d1['approxage'].keys() and var_approxage!='Rare':
            var_approxage= int(d1['approxage'][var_approxage])
        else:
            var_approxage= int(d1['approxage']['Rare'])

        if var_approxsqft in d1['approxsqft'].keys() and var_approxsqft!='Rare':
            var_approxsqft= int(d1['approxsqft'][var_approxsqft])
        else:
            var_approxsqft= int(d1['approxsqft']['Rare'])

        var_propertynew=var_propertynew[0].upper()+var_propertynew[1:].lower()
        if var_propertynew in d1['propertynew'].keys() and var_propertynew!='Other':
            var_propertynew= int(d1['propertynew'][var_propertynew])
        else:
            var_propertynew= int(d1['propertynew']['Other'])


        # print('var_city:',var_city)
        # print('var_approxage:',var_approxage)
        # print('var_approxsqft:',var_approxsqft)
        # print('var_propertynew:',var_propertynew)




        #data = np.array(data)[np.newaxis, :]  # converts shape from (4,) to (1, 4)
        alien_data={'city':var_city,'approxage':var_approxage,'approxsqft':var_approxsqft,'propertynew':var_propertynew,\
           'bedroomstotal':var_bedroomstotal,'kitchens':var_kitchens,'washrooms':var_washrooms,\
           'maintenancefee':var_maintenancefee,'lifeofad':var_lifeofad,'kitchens_na':0,'washrooms_na':0\
            ,'maintenancefee_na':0,'soldprice_na':0}
        aliendata=pd.DataFrame(alien_data,index=[0],columns=alien_data.keys())
        
        cols= aliendata.columns

        capper.fit(aliendata)
        aliendata=capper.transform(aliendata)

        aliendata_tr= pd.DataFrame(scaler.transform(aliendata), columns=cols)

        aliendata_sel=aliendata_tr[features]


        alienprice_pred_Lasso=engine.predict(aliendata_sel)

        alienprice_pred_KNN=engine_KNN.predict(aliendata_sel)

        aliendata_sel_rf=aliendata[features_rf]
        alienprice_pred_rf=engine_rf.predict(aliendata_sel_rf)

        print('Lasso:',round(np.exp(alienprice_pred_Lasso)[0],2))

        print('KNN:',round(np.exp(alienprice_pred_KNN)[0],2))

        print('RF:',round(np.exp(alienprice_pred_rf)[0],2))


        


        prediction_all= round((round(np.exp(alienprice_pred_KNN)[0],2)+\
                    round(np.exp(alienprice_pred_rf)[0],2)+\
                    round(np.exp(alienprice_pred_Lasso)[0],2))/3,2)

        print('all_avg:',prediction_all)

      


        prediction2= round((round(np.exp(alienprice_pred_KNN)[0],2)+\
                    round(np.exp(alienprice_pred_rf)[0],2))/2,2)

        print('pred2:',prediction2)

      

        prediction_min= min(round(np.exp(alienprice_pred_KNN)[0],2),\
                        round(np.exp(alienprice_pred_rf)[0],2))

        print('min_pred:',prediction_min)

        prediction_max= max(round(np.exp(alienprice_pred_KNN)[0],2),\
                round(np.exp(alienprice_pred_rf)[0],2))

        print('max_pred:',prediction_max)

        #-------------------------------#
        # KNN-- Finding nearest neighbours of the alien
        df=pd.read_csv('KNN.csv')
        list=df.columns

        dict={}
        for i,k in enumerate(list):
            dict[k]=i

        distance=[]

        for i in range(len(df)):
            latcomp=(latitude-df.iloc[i,dict['latitude']])**2
            longcomp=(longitude-df.iloc[i,dict['longitude']])**2
            dist=np.sqrt(latcomp+longcomp)
            
            if dist>1.5:
                distance.append(i)
        
        df.drop(df.index[distance],inplace=True) # dropping distance>1.5

        print('df size:',len(df))

        if len(df)==0:
            return render_template('00-Basic-Template.html',Flag='Sorry! No Data Found...Enter a Different Address')#,approxage=approxage)
        elif len(df)<4:
            return render_template('00-Basic-Template.html',Flag='Sorry! Sufficient Data not available...Enter a Different Address')


        df['soldprice']=round(np.exp(df['soldprice']),2)

        x_test_knn=aliendata_tr
        #y_test_knn=prediction

        y_train_knn=df['soldprice']

        train_vars=['city',
                     'approxage',
                     'approxsqft',
                     'propertynew',
                     'bedroomstotal',
                     'kitchens',
                     'washrooms',
                     'maintenancefee',
                     'lifeofad',
                     'kitchens_na',
                     'washrooms_na',
                     'maintenancefee_na',
                     'soldprice_na']

        x_train_knn=df[train_vars]

        x_train_knn=pd.DataFrame(scaler.transform(x_train_knn),columns=cols)

        #print('before regressor')

        neigh = KNeighborsRegressor(n_neighbors=4,algorithm='kd_tree')
        neigh.fit(x_train_knn, y_train_knn)

        _,predictors=neigh.kneighbors(x_test_knn,n_neighbors=4)

        list2=predictors[0].tolist()

        print('list2 len:',len(list2))

        lat_long_price=[[round(df.iloc[i,dict['latitude']],7),round(df.iloc[i,dict['longitude']],7),df.iloc[i,dict['soldprice']]] for i in list2]

        average_neighbor_price=round(sum([lat_long_price[i][2] for i in range(len(lat_long_price))])/4,2)

        print('avg_nbr:',average_neighbor_price)

        #------------------------------#

        # pdediction value Tweaking:

        prediction_list=[prediction_all,prediction_min,prediction2,prediction_max]

        diff=abs(min(prediction_list)-average_neighbor_price)
        prediction=min(prediction_list)

        for val in prediction_list:
            diffx=abs(val-average_neighbor_price)                
            if diffx<diff:
                prediction=val
                diff=diffx

        print('pred:',prediction)


        #return jsonify(data)
        #aliendata.head(2)
        #prediction = model.predict(aliendata)  # runs globally loaded model on the data
    #return str(prediction[0])
    #output=prediction[0]
     #return render_template('00-Basic-Template.html',prediction=prediction)#,approxage=approxage)
     return render_template('map.html',address=address, latitude=round(latitude,7),longitude=round(longitude,7),price=prediction,llp=lat_long_price)
    #return(str(type(prediction[0])))
    #return(str(prediction.shape))
    #return (str(prediction))
    #return {'prediction':prediction}


if __name__ == '__main__':
    load_engine()
    load_mapdict()
    load_outlier_capper()
    load_scaler()
    load_features()
    load_features_rf()
    load_engine_rf()
    load_engine_KNN()


    # load model at the beginning once only
    #app.run(host='0.0.0.0', port=80)
    #app.run(port=80, debug=True)
    app.run(host='127.0.0.1',port=5000, debug=True)
    #app.run(host='0.0.0.0',port=5000, debug=True)
