# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 12:03:36 2018

@author: joelee
"""

 # import csv file and pull into a pandas dataframe
 # end result incidents_df
 # Dependencies
import pandas as pd

incidents_csv = "gtdb_0617_proj_cols_short.csv"  #  
# Read our Data file with the pandas library
# Not every CSV requires an encoding, but be aware this can come up
incidents_df = pd.read_csv(incidents_csv, encoding = "ISO-8859-1")

 # display columns imported to confirm column names  
#print(incidents_df.head())

# Dates show up as NaN where there are blanks. 
# replace the NaNs with blanks
incidents_df = incidents_df.fillna({'Date':0, 'nkill':0, 'nwound':0})
#print(incidents_df.head(40))
# I'm not sure why, but putting a zero date value 
# assigns it a date of 1/1/1970

incidents_df['Date'] = pd.to_datetime(incidents_df['Date'])
#print(incidents_df.head(40))

# incident nkill and nwound come in as float64.  convert to int64
incidents_df['nkill'] = incidents_df['nkill'].fillna(0).astype(int)
incidents_df['nwound'] = incidents_df['nwound'].fillna(0).astype(int)   

 # inspect the df datatypes, and convert any datatypes necessary for 
 # proper behavior
 # event_id = integer; 
 # year = integer
 # month = integer
 # day = integer
 # country_id = integer
 # country_txt = varchar
 # lat = float
 # long = float
 # attack Type 1 nvarchar
 # 
incidents_df = incidents_df.rename(columns={"eventid":"incident_id", 
                                            "Date":"idate", 
                                            "country":"icountry_id", 
                                            "country_txt":"icountry_txt",
                                            "latitude":"ilatitude", 
                                            "longitude":"ilongitude", 
                                            "attacktype1":"attacktype_id", 
                                            "attacktype1_txt":"attacktype_txt", 
                                            "targtype1":"targtype_id", 
                                            "targtype1_txt":"targtype_txt", 
                                            "weaptype1":"weaptype_id", 
                                            "weaptype1_txt": "weaptype_txt",
                                            "property":"property_flg"
                                            })
#print(incidents_df.head())

print(incidents_df['idate'].dtype)

#print(incidents_df.count())
# lat/long missing for 959-907 of the sample rows.  
 # remove rows where lat is nan or blank
incidents_df = incidents_df[pd.notnull(incidents_df['ilatitude'])]
#print(incidents_df.count())

print (incidents_df.dtypes)
# text columns come in as objects instead of strings.  examples online indicate this is ok. 
incidents_df['icountry_txt'] = incidents_df['icountry_txt'].astype('S50')
print (incidents_df.dtypes)


#print(incidents_df)

#for idx in incidents_df.index:
#    print (incidents_df.loc[idx, 'idate'])
#    print (incidents_df.loc[idx, 'icountry_txt'])
#    print (incidents_df.loc[idx, 'gname'])

  
# I consider this clean enough. 
