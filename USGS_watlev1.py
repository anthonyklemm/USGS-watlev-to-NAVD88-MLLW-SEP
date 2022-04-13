# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 12:38:07 2022

This code processes tab-delimited USGS water level gauge data to extract
the minimum daily waterlevel values and then graphs the results, including
a 90-day rolling average of the minimum daily water level values with a linear-
regression trendline as an analog to relative sealevel rise trends.
Data can be found through the USGS water dashboard: https://dashboard.waterdata.usgs.gov/

This method produces a quick approximation of the separation value between the
orthometric height datum of the gauge in NAVD88 to NOAA's conventional charting
datum of Mean Lower Low Water (MLLW), if the gauge in in a tidally influenced
waterway. More on tidal datums can be found at NOAA's WEbsite: 
https://tidesandcurrents.noaa.gov/

**note, you may need to look at the text file extracted from the USGS website
to count how many rows to skip, and modify that on line 33 in the script**

@author: Anthony.R.Klemm
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'qt')

wkdir_path = "C:/Users/Anthony.R.Klemm/Desktop/"
filename = "lostmans.txt"
file_input=wkdir_path+filename
#read waterlevel tide file from USGS in pandas
df = pd.read_csv(file_input, skiprows=(34), sep = "\t", low_memory=False)
df = df.iloc[1: , :]
for columns in df:
    try:
        df.drop("agency_cd", axis=1, inplace=True)
        df.drop("site_no", axis=1, inplace=True)
        df.drop("171342_00010_cd", axis=1, inplace=True)
        df.drop("tz_cd", axis=1, inplace=True)
        df.drop("170226_00060", axis=1, inplace=True)
        df.drop("170226_00060_cd", axis=1, inplace=True)
        df.drop("170228_00065_cd", axis=1, inplace=True)
        df.drop("170231_72137", axis=1, inplace=True)
        df.drop("170231_72137_cd", axis=1, inplace=True)
        df.drop("171330_00480", axis=1, inplace=True)
        df.drop("171335_72255", axis=1, inplace=True)
        df.drop("171330_00480_cd", axis=1, inplace=True)
        df.drop("171335_72255_cd", axis=1, inplace=True)
        df.drop("171342_00010", axis=1, inplace=True)
        df.drop("62944_00065_cd", axis=1, inplace=True)
        df.drop("abc", axis=1, inplace=True)
    except KeyError:
        continue

for columns in df:
    try:
        df.rename(columns={"170228_00065":"147223_62620"}, inplace=True)
        df.rename(columns={"62944_00065":"147223_62620"}, inplace=True)
    except KeyError:
        continue
print(df.head())

#define timestamp as datetime format
format = '%Y-%m-%d %H:%M:%S'
df['datetime'] = pd.to_datetime(df['datetime'], format=format)

#create datetime index allowing data resample for minimum daily waterlevel
df = df.set_index(pd.DatetimeIndex(df['datetime']))
print(df.dtypes)
df['147223_62620'] = df['147223_62620'].astype('float')

g = df.resample('D')['147223_62620']

df['min_daily_watlev'] = g.transform('min')

#only keep first daily record
df = df.groupby(df.index.date).apply(lambda x: x.iloc[[0]])

df.index = df.index.droplevel(0)
#create 90 day rolling average
df['90day_avg'] = df.min_daily_watlev.rolling(90).mean().shift(-45)
df['total_avg'] = df.min_daily_watlev.mean()

#calculate the mean daily low water level at NAVD88
df2 = df[['min_daily_watlev']].mean()

#convert to meters and prepare data for graphing
df2 = df2/3.28084
df2 = df2[0]
df2 = str(round(df2,3))
df3 = df[['min_daily_watlev']].std()
df3 = df3/3.28084
df3 = df3[0]
df3 = str(round(df3,3))
df4 = df[['90day_avg']].mean()
df4 = df4/3.28084
df4 = df4[0]
df4 = str(round(df4,3))
df['filtered_avg'] = df4
df['filtered_avg'] = df[['filtered_avg']].apply(pd.to_numeric)
df5 = df[['90day_avg']].std()
df5 = df5/3.28084
df5 = df5[0]
df5 = str(round(df5,3))

#print the results in the IPython console
print('Average Minimum Waterlevel = ' + df2 + ' std_dev = ' + df3)
print('Filtered Min Watlev = ' + df4 + ' std_dev = ' + df5)

#create the graph
x = df['datetime']
y = (df['min_daily_watlev']/3.28084)
z = (df['90day_avg']/3.28084)
a = (df['total_avg']/3.28084)
b = df['filtered_avg']

plt.plot(x,y, label='Minimum Daily Waterlevel')
plt.plot(x,z, label='90-day rolling average', linewidth=3.5)
plt.plot(x,a, label='Unfiltered Mean = ' + df2 +'m (std_dev = ' + df3 + 'm)')
plt.plot(x,b, label='90-day Filtered Mean = ' + df4 +'m (std_dev = ' + df5 + 'm)')
plt.xlabel('Date', fontweight='bold')
plt.ylabel('Meters at NAVD88', fontweight='bold')
plt.title('USGS Minimum Daily Waterlevel Values at ' + filename[:-4], fontweight='bold')
plt.grid()
plt.legend()
plt.show()

#create separate plot with 90-day rolling average and linear regression trendline
df = df['90day_avg']/3.28084
df = df.reset_index(drop=True)
df = df.reset_index(drop=False)
sns.lmplot('index','90day_avg', data=df, fit_reg=True).set(
    title="Minimum daily water levels 90-day rolling average with relative sealevel rise trendline at "+ filename[:-4])
