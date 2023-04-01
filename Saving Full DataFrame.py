#To take all of our yelp data and collect in one dataframe, then save it to a csv file

import pandas as pd #Import necessary libraries
import glob
import os

dataframe = pd.DataFrame() #Initialize dataframe to append our data to

path = r"C:\Users\Chris\OneDrive\Documents\Yelp Ratings" # Path of our csv
all_files = glob.glob(os.path.join(path , "*.csv")) #Takes all csv files in our folder and converts them to a list

li = [] #Initialize list

for filename in all_files: #Reads through each csv file and appends it to our list 
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

dataframe = pd.concat(li, axis=0, ignore_index=True) #Concatenates the list of csv's to our initialized dataframe
print(dataframe)


#Save the new summary dataframe into a new folder, so it doesn't get lumped in when we create the summary table
from pathlib import Path  
filepath = Path(r"C:\Users\Chris\OneDrive\Documents\Yelp Ratings\Summary Table\Summary Ratings.csv")  
filepath.parent.mkdir(parents=True, exist_ok=True)  
dataframe.to_csv(filepath, index = False) 
