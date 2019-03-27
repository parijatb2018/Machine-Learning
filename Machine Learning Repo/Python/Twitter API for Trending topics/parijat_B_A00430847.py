# Assignment#4
"""
Created on Mon Feb 18 23:45:29 2019

@author: Parijat
"""


#>> 1.Finding World Trending topics in Twitter<<

import tweepy
import json

# Twitter API authentication
consumer_key = 'yCOLjBn0P0RAWxVDOY4G3RzX9'
consumer_secret = 'rwmPeDJ7Z9dYenvNpdY9Qzc82BMIts6ErE6QOaWJVGCOuciMhL'
access_token = '114791180-Vw7mXFgDILtd7N23MGqgLQ1xDENeS7ItQxmyYT4F'
access_token_secret = 'FmJNXMRIqSVgS2gjUXrxBrolaeEQUuhdxJb8XUAwA3qQ7'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

world_trends = api.trends_place(1) # catching world trends in Twitter

trends = json.loads(json.dumps(world_trends, indent=1)) # parsing trends in to json

#print(trends)

trendList=[]

for trend in trends[0]["trends"]:    # putting trend names into list
    temp=trend["name"].strip("#")    
    trendList.append(temp)  
    
    
print(trendList) # printing trend names

print('\n')        
        
#>> 2.Finding related news<<
        
from newsapi import NewsApiClient

# News API authentication
newsapi = NewsApiClient(api_key='b8cb59bf84dd43d3834f0095939bfb74')


nd={} # related news dictionary
templist1=[]
templist2=[] 

for i in range(0,len(trendList)): # looping for each trend
    
    all_articles = newsapi.get_everything(q=trendList[i],sources='google news')
    

    
    n=len(all_articles['articles'])


    for j in range(0,n):    # looping for all news articles for a trend
    
        v1= all_articles['articles'][j]['source']['name']       
        templist2.append(v1)    
        
        v2= all_articles['articles'][j]['title']       
        templist2.append(v2)   
        
        v3= all_articles['articles'][j]['url']       
        templist2.append(v3)    
        
        templist1.append(templist2)
        templist2=[]

    nd[trendList[i]]=templist1
    templist1=[]
    
with open('nd.txt', 'w+') as f:
    f.write(json.dumps(nd, indent=4))    

print('done! please refer nd.txt')
#Format: {trend1:[[source1,title1,url1],[source2,..]],trendi:[[],..]}   

#print(json.dumps(nd, indent=4))# printing related news against trending topics to dictionary > 
                              







