# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 08:37:08 2022

@author: Faith
"""

import requests, json
from pandas import DataFrame
import pandas as pd

'''
url = "https://data.bts.gov/resource/g3h6-334u.json" # Need to figure out how to make it so all columns show

resource = pd.read_json(url)
#print(resource.head())

df4 = pd.DataFrame(resource)
pd.set_option('display.max_columns',12)

print(df4.head(10))

print(df4[df4['sysname'].str.contains("New York")].head())

'''

#--------------------------------------------------------------------------------------------------------------------

# Read in CSV file for Bike Sharing
df4 = pd.read_csv(r'C:\Users\Faith\Documents\CS 620 - Data Science Class\CS 620 Project\Docked_Bikeshare.csv')

#Show first 10 rows of df4
print(df4.head(10))

#Show only information related to New York
print(df4[df4['sysname'].str.contains("New York")].head())

print('Show columns that are included in bikedf dataframe')
print(df4.columns)

# Slice dataframe to only include information for SysName, Year, assigned_month, and sum_min
bikedf1 = df4.loc[:,['sysname', 'year', 'assigned_month', 'sum_min' ]]

print('\n', 'Preview Bikedf1 dataframe')
print(bikedf1.head())

print('\n','Check data types of columns in bikedf1')
print(bikedf1.dtypes)


# Function that remove commas from number fields
def remove_NumberCommas(x):
	return str(x.replace(',', ''))


# Remove commas from year field
bikedf1["year"] = bikedf1["year"].apply(remove_NumberCommas)

#Change datatype for year field to int
bikedf1["year"] = bikedf1["year"].astype(int)


#Remove commas from sum_min field
bikedf1["sum_min"] = bikedf1["sum_min"].apply(remove_NumberCommas)

#Change data type of columnn sum_min to float
bikedf1["sum_min"] = bikedf1["sum_min"].astype(float)

#Change data type of columnn year to int
bikedf1["year"] = bikedf1["year"].astype(str).astype(int)
#Too here*******



print('\n','Check for Updated data types')
print(bikedf1.dtypes)


#print('\n','View bikedf1 with data type changes')
#print(bikedf1.head(), '\n')

# Function that remove ')' from value
def remove_CloseParath(x):
    return str(x.replace(')', ''))
    

#Prepping column sysname by removing certain parts to get 
bikedf1['sysname'] = bikedf1['sysname'].str.split('\(').str[-1].str.strip()
bikedf1['sysname'] = bikedf1['sysname'].apply(remove_CloseParath)

print('\n','Show dataframe after prepping column sysname and data type change of year and sum_min')
print(bikedf1.head())


# Make column for State and city by splitting sysname column based on comma
bikedf1[['City','State']] = bikedf1.sysname.str.split(",",expand=True)


print('\n', 'Show dataframe for added columns City and State')
print(bikedf1.head())

#Group dataframe by month, year, city, and state

grouped_bikedf1 = bikedf1.groupby(['City', 'State', 'year', 'assigned_month'])

# Provide Avg sum_mins for each grouping
mean_df = grouped_bikedf1.mean()

mean_df = mean_df.reset_index()

#rename columns

mean_df.rename(columns={'year': 'Year', 'sum_min': 'Avg_Mins', 'assigned_month': 'Month'}, inplace=True)

print('\n','Dataframe of column renames, and sum_mins calculated as avg minutes' 
      ,'\n','by City, State, Year, and Month', '\n')
print(mean_df.head(), '\n')


#Convert sum_mins to hours

def Convert_to_hrs(x):
    return x / 60

#Add new column for Avg_Hrs
mean_df['Avg_Hrs'] = mean_df['Avg_Mins'].apply(Convert_to_hrs)

#Create new Dataframe
Bike_Mnth = mean_df

#Rename values in City column
Bike_Mnth.loc[Bike_Mnth["City"] == "New York", "City"] = 'New York City'
Bike_Mnth.loc[Bike_Mnth["City"] == "Washington", "City"] = 'DC' 

#Filter dataframe to only return information for New York City, DC, and San Francisco
Bike_Mnth = Bike_Mnth[Bike_Mnth['City'].str.contains("New York|Francisco|DC")]

print('Bike information by month:', '\n')
print(Bike_Mnth.head())

#-----------------------------------------------------------------------------------------------------------
# Information for public transit

transiturl = "https://data.bts.gov/resource/dc74-f8qd.json" 
transit = pd.read_json(transiturl)
#print(resource.head())

df5 = pd.DataFrame(transit)
pd.set_option('display.max_columns',12)

print('\n', 'Transit information by month:', '\n')
print(df5.head(10))

# Slice dataframe to only include information for agency, date, current_ridership
transitdf1 = df5.loc[:,['agency', 'date', 'current_ridership']]

transitdf1['Year'] = pd. DatetimeIndex(transitdf1['date']). year
transitdf1['Month'] = pd. DatetimeIndex(transitdf1['date']). month

print('\n', 'Preview transitdf1 dataframe')
print(transitdf1.head())

print('\n','Check data types of columns in transitdf1')
print(transitdf1.dtypes)

#Check Unique Values in Agency column
print('\n', 'Check Unique Values in Agency column')
print(transitdf1.agency.unique())

#Change Value names for agency column

transitdf1.loc[transitdf1["agency"] == "New York City MTA Rail", "agency"] = 'New York City'
transitdf1.loc[transitdf1["agency"] == "WMATA Bus and Rail", "agency"] = 'DC'
transitdf1.loc[transitdf1["agency"] == "San Francisco BART Rail", "agency"] = 'San Francisco'

#Rename column agency

transitdf1.rename(columns={'agency': 'City'}, inplace=True)

#print(transitdf1.dtypes)

# Create new dataframes with only specific columns for transit information
transitdf2 = transitdf1.loc[:,['City', 'Year', 'Month', 'current_ridership']]

#Group dataframe for transitdf1 by a, year, city, and state
grouped_tdf2 = transitdf2.groupby(['City', 'Year', 'Month'])

#Provide Median current ridership by month and city
grouped_tdf3 = grouped_tdf2.median()

grouped_tdf3 = grouped_tdf3.reset_index()

#rename column current_ridership
grouped_tdf3.rename(columns={'current_ridership': 'Median_Ridership'}, inplace=True)





#print(mean_df.City.unique())

#print(grouped_tdf3.head(20))

#------------------------------------------------------------------------------------------------------------

# Combine information for Bike_Mnth and grouped_tdf3

Combined_df = pd.merge(Bike_Mnth, grouped_tdf3,  how='left', left_on=['City','Year', 'Month'], right_on = ['City','Year', 'Month'])

#Return top 100 records from Combined_df
print('\n','Return top 100 records from Combined_df', '\n')

print(Combined_df.head(100))

#-------------------------------------------------------------------------------------------------------------
# Write DataFrames to excel

#Bike_Mnth.to_excel(r'C:\Users\Faith\Documents\Github Python\Transit Information\BikeData.xlsx', index=False)
#grouped_tdf3.to_excel(r'C:\Users\Faith\Documents\Github Python\Transit Information\TransitData.xlsx', index=False)
#Combined_df.to_excel(r'C:\Users\Faith\Documents\Github Python\Transit Information\CombinedData.xlsx', index=False)
  

# print('DataFrame is written to Excel File successfully.')


#--------------------------------------------------------------------------------------------------------------
# Visual Information for Bike riding and Transit Ridership by Month

import seaborn as sns
import matplotlib.pyplot as plt

Combined2020 = Combined_df[(Combined_df.Year == 2020)]
Combined2021 = Combined_df[(Combined_df.Year == 2021)]

# Create line graph in Seaborn for Bike_Month in 2020
sns.lineplot(data=Combined2020, x="Month", y="Avg_Hrs", hue='City', markers=True)

plt.ylabel("Avg Hrs Biked")
plt.title('Trending Avg Hrs Biked in 2020')

plt.show()


# Create line graph in Seaborn for Transit Information 2020

sns.lineplot(data=Combined2020, x="Month", y="Median_Ridership", hue='City', markers=True)

plt.ylabel("Median Ridership")
plt.title('Trending Median Ridership in 2020')

plt.show()

# Create line graph in Seaborn for Bike_Month in 2021

sns.lineplot(data=Combined2021, x="Month", y="Avg_Hrs", hue='City', markers=True)

plt.ylabel("Avg Hrs Biked")
plt.title('Trending Avg Hrs Biked in 2021')

plt.show()

# Create line graph in Seaborn for Transit Information 2021

sns.lineplot(data=Combined2021, x="Month", y="Median_Ridership", hue='City', markers=True)

plt.ylabel("Median Ridership")
plt.title('Trending Median Ridership in 2021')

plt.show()





