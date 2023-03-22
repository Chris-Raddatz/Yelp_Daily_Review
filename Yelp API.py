#Project to make a bot that takes in the top restaurants from Yelp in 78750 and plots them 
#on a map of north austin.

import requests
import pandas as pd
from pandas import json_normalize
api_url = "https://api.yelp.com/v3/businesses/search"

# Get data about NYC cafes from the Yelp API
api_key = 'Your key' #Personal API key


params = {"term" : "restaurants",
          "location" : "Austin, TX 78750"} #Looking for restaurants in Austin TX
headers = {"Authorization": "Bearer {}".format(api_key)}
# Get data about NYC cafes from the Yelp API
response = requests.get(api_url, 
                        headers=headers, 
                        params=params) #Pulls data with our api key, parameters and the url at top

# Extract JSON data from the response
data = response.json()

#Create table
def get_table(data):
    restaurants = json_normalize(data['businesses'], 
                            sep = '-', 
                            record_path = 'categories', #Picks which data to pull, 
                            meta = ['name',
                                    'alias',
                                    'rating',
                                    ['coordinates', 'latitude'], #Pulls lat
                                    ['coordinates', 'longitude'], #Pulls long
                                    ['location', 'address1']], #Pulls Address
                            meta_prefix = 'biz_') #Gives prefix 
    
    restaurants['biz_name'] = restaurants['biz_name'].drop_duplicates() #Inserts NaN for duplicates
    restaurants.dropna(inplace = True)  #Drops said NaN
    restaurants.reset_index(inplace = True, drop = True) 
    restaurants.drop(columns = ['alias', 'biz_alias'], axis = 1, inplace = True) #DRop irrelevant columns

    restaurants['biz_coordinates-latitude'] = restaurants['biz_coordinates-latitude'].astype(float)
    restaurants['biz_coordinates-longitude'] = restaurants['biz_coordinates-longitude'].astype(float) #Change to float for distance module later on

    #print(restaurants)

    return restaurants

def get_distance(data):
    from geopy import distance
    home_coordinates = (0,0) #Input Lat and Long of your coordinates

    travel_distances = [] #initialize list

    for lat, long in zip(data['biz_coordinates-latitude'], data['biz_coordinates-longitude']): #For each lat, long in dataset, calculate the distance and append to our list
        travel_distance = distance.distance(home_coordinates, (lat, long)).miles
        travel_distances.append(travel_distance)

    data['travel_distance'] = travel_distances #Make a new column with our list of distances
    return data


restaurants = get_table(data) #Retrieve data
restaurants = get_distance(restaurants) #Retrieve distance from home
restaurants['rank'] = range(1,21) #Give them an actual #1-20 ranking

restaurants.sort_values(by = ['travel_distance'], ascending = True, inplace = True)

clean = restaurants[['rank','title', 'biz_name', 'biz_rating','biz_location-address1','travel_distance']] #Slice the dataset for specific columns
clean.rename({"rank" : "Rank", "title" : "Type", "biz_name" : "Business", "biz_rating" : "Rating", "biz_location-address1" : "Address", "travel_distance" : "Distance From Home"}, axis = 1, inplace = True) #More comprehensible titles

from datetime import datetime
clean['Date of Ranking'] = pd.Timestamp.today().strftime('%Y-%m-%d') #Put the date of ranking


from pathlib import Path  
filepath = Path(r"C:\Users\Documents\Yelp Review{}.csv".format(pd.Timestamp.today().strftime('%Y-%m-%d')))  
filepath.parent.mkdir(parents=True, exist_ok=True)  
clean.to_csv(filepath, index = False) #Saving to documents