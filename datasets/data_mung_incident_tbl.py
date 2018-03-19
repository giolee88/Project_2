# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 21:16:22 2018
This script will clean up our terrorism event table.  
It will then create a tableby reading from the referenced csv file. 
The csv file had minor datamunging done in excel as well, including:
    -- eliminating columns we were not interested in.  
    -- adding a date column
    -- no edits appear needed to the column titles. 
@author: joelee
"""
# 
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

#print(incidents_df['idate'].dtype)

#print(incidents_df.count())
# lat/long missing for 959-907 of the sample rows.  
 # remove rows where lat is nan or blank
incidents_df = incidents_df[pd.notnull(incidents_df['ilatitude'])]
#print(incidents_df.count())

#print (incidents_df.dtypes)
# text columns come in as objects instead of strings.  examples online indicate this is ok. 

#print(incidents_df.head())
  
# I consider this clean enough. 

 # Import SQL Alchemy
from sqlalchemy import create_engine # , func

# Import PyMySQL (Not needed if mysqlclient is installed)
import pymysql
pymysql.install_as_MySQLdb()

# Import and establish Base for which classes will be constructed 
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Import modules to declare columns and column data types
from sqlalchemy import Column, Integer, String, Float, Date  # , ForeignKey
from sqlalchemy_utils import database_exists, create_database, drop_database

# Create the Incident class
class Incidents(Base):
    __tablename__ = 'incidents_tbl'
    incident_id = Column(Integer, primary_key=True)
    iyear = Column(Integer)             # incident year Column(String(255))
    imonth = Column(Integer)            # incident month  Column(Float)
    iday = Column(Integer)              # incident day (String(255))
    idate = Column(Date)                # Incident Date
    icountry_id = Column(Integer)
    icountry_txt = Column(String(50))
    ilatitude = Column(Float)
    ilongitude = Column(Float)
    attacktype_id  = Column (Integer)
    attacktype_txt = Column (String(50))
    targtype_id  = Column (Integer)
    targtype_txt = Column (String(50))
    gname = Column (String(100))
    weaptype_id = Column(Integer)
    weaptype_txt = Column(String(100))
    nkill = Column(Integer)
    nwound = Column(Integer)
    property_flg = Column (Integer)
    
# Create a connection to a SQLite database
engine = create_engine('sqlite:///gtdb.sqlite')

if database_exists(engine.url):
    drop_database(engine.url)
if not database_exists(engine.url):
    create_database(engine.url)
conn = engine.connect()

# Create the incidets_tbl table within the database
Base.metadata.create_all(conn)


# To push the objects made and query the server we use a Session object
from sqlalchemy.orm import Session
session = Session(bind=engine)

## First approach--to write a row for each row in the df
## For each row of the dataframe, create an instance of the Incidents class


for idx in incidents_df.index[1:]:
    incident_row = Incidents(incident_id=incidents_df.loc[idx,'incident_id'],
                             iyear=incidents_df.loc[idx,'iyear'],
                             imonth= incidents_df.loc[idx,'imonth'],
                             iday= incidents_df.loc[idx,'iday'],
                             idate= incidents_df.loc[idx,'idate'],
                             icountry_id= incidents_df.loc[idx,'icountry_id'],
                             icountry_txt= incidents_df.loc[idx,'icountry_txt'],
                             ilatitude= incidents_df.loc[idx,'ilatitude'],
                             ilongitude= incidents_df.loc[idx,'ilongitude'],
                             attacktype_id= incidents_df.loc[idx,'attacktype_id'],
                             attacktype_txt= incidents_df.loc[idx,'attacktype_txt'],
                             targtype_id= incidents_df.loc[idx,'targtype_id'],
                             targtype_txt= incidents_df.loc[idx,'targtype_txt'],
                             gname= incidents_df.loc[idx,'gname'],
                             weaptype_id= incidents_df.loc[idx,'weaptype_id'],
                             weaptype_txt= incidents_df.loc[idx,'weaptype_txt'],
                             nkill= incidents_df.loc[idx,'nkill'],
                             nwound= incidents_df.loc[idx,'nwound'],
                             property_flg= incidents_df.loc[idx,'property_flg']
                             )
    
# Add these objects to the session
    session.add(incident_row)
# Commit the objects to the database
    session.commit()
conn.close()

# 2nd approach:  use pandas .to_sql() 
#incidents_df.to_sql(name='incidents_tbl.', 
#                    con=engine, if_exists = 'fail', index=False)
#session.commit()
# I find that the 2nd approach doesn't allow the assignment of a key.  

#conn.close()