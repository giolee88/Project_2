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
#  import sqlite3
import pandas as pd

incidents_csv = "gtdb_0617_proj_cols.csv"  #  
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
incidents_df['latitude'] = incidents_df['latitude'].astype(float)
incidents_df['longitude'] = incidents_df['longitude'].astype(float)
incidents_df['iyear'] = incidents_df['iyear'].astype(int)

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
# trim off columns that appear to be difficult to maintain data integrity on. 

org_inc_df = incidents_df[[  #  "incident_id",
                           "iyear", "icountry_txt", "ilatitude", "ilongitude", 
                           "attacktype_txt", "targtype_txt", "gname", 
                           "weaptype_txt", "nkill"
                           ]]



 # Import SQL Alchemy
from sqlalchemy import create_engine # , func

# Import PyMySQL (Not needed if mysqlclient is installed)
import pymysql
pymysql.install_as_MySQLdb()

# Import and establish Base for which classes will be constructed 
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Import modules to declare columns and column data types
from sqlalchemy import Column, Integer, String, Float  # , Date  , ForeignKey
from sqlalchemy_utils import database_exists, create_database, drop_database


# Create the Incident class
class Incidents(Base):
    __tablename__ = 'incidents_tbl'
    incident_id = Column(Integer, primary_key=True)
    iyear = Column(Integer)             # incident year Column(String(255))
#    imonth = Column(Integer)            # incident month  Column(Float)
#    iday = Column(Integer)              # incident day (String(255))
#    idate = Column(Date)                # Incident Date
#    icountry_id = Column(Integer)
    icountry_txt = Column(String(50))
    ilatitude = Column(Float)
    ilongitude = Column(Float)
#    attacktype_id  = Column (Integer)
    attacktype_txt = Column (String(50))
#    targtype_id  = Column (Integer)
    targtype_txt = Column (String(50))
    gname = Column (String(100))
#    weaptype_id = Column(Integer)
    weaptype_txt = Column(String(100))
    nkill = Column(Integer)
#    nwound = Column(Integer)
#    property_flg = Column (Integer)
    
# Create a connection to a SQLite database
# sqlite blows chunks.  commenting out the sqlite db and Switching to mysql
#engine = create_engine('sqlite:///gtdb.sqlite')
#     here we create a connection to the mysql database engine.  
engine = create_engine("mysql://gtdb_admin:ktjljmjj@gtdb-insta.csuho8dvfguv.us-east-1.rds.amazonaws.com:3306/gtdb")
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


for idx in org_inc_df.index:
    incident_row = Incidents(  #incident_id=org_inc_df.loc[idx,'incident_id'],
                             iyear=org_inc_df.loc[idx,'iyear'],
#                             imonth= org_inc_df.loc[idx,'imonth'],
#                             iday= org_inc_df.loc[idx,'iday'],
#                             idate= org_inc_df.loc[idx,'idate'],
#                             icountry_id= org_inc_df.loc[idx,'icountry_id'],
                             icountry_txt= org_inc_df.loc[idx,'icountry_txt'],
                             ilatitude= org_inc_df.loc[idx,'ilatitude'],
                             ilongitude= org_inc_df.loc[idx,'ilongitude'],
#                             attacktype_id= org_inc_df.loc[idx,'attacktype_id'],
                             attacktype_txt= org_inc_df.loc[idx,'attacktype_txt'],
#                             targtype_id= org_inc_df.loc[idx,'targtype_id'],
                             targtype_txt= org_inc_df.loc[idx,'targtype_txt'],
                             gname= org_inc_df.loc[idx,'gname'],
#                             weaptype_id= org_inc_df.loc[idx,'weaptype_id'],
                             weaptype_txt= org_inc_df.loc[idx,'weaptype_txt'],
                             nkill= org_inc_df.loc[idx,'nkill'],
#                             nwound= org_inc_df.loc[idx,'nwound'],
#                             property_flg= org_inc_df.loc[idx,'property_flg']
                             )
    
# Add these objects to the session
    session.add(incident_row)
# Commit the objects to the database
    session.commit()


#connn = sqlite3.connect('gtdb.sqlite')
#c = connn.cursor()

#we only added this following portion to attempt to fix sqlite, but don't need it in mysql

#c.executescript('''
#    PRAGMA foreign_keys=off;
#
#    BEGIN TRANSACTION;
#    ALTER TABLE incidents_tbl RENAME TO old_table;
#
#    /*create a new table with the same column names and types while
#    defining a primary key for the desired column*/
#    CREATE TABLE incidents_tbl (incident_id Integer PRIMARY KEY NOT NULL,
#                            iyear INTEGER, 
#                            icountry_txt TEXT, 
#                            ilatitude REAL,
#                            ilongitude REAL, 
#                            attacktype_txt TEXT, 
#                            targettype_txt TEXT, 
#                            gname TEXT, 
#                            weaptype_txt TEXT, 
#                            nkill INTEGER);
#    
#    INSERT INTO incidents_tbl SELECT * FROM old_table;
#
#    DROP TABLE old_table;
#    COMMIT TRANSACTION;
#
#    PRAGMA foreign_keys=on;''')


# c.close()

conn.close()
print ('OK')



# 2nd approach:  use pandas .to_sql() 
#incidents_df.to_sql(name='incidents_tbl.', 
#                    con=engine, if_exists = 'fail', index=False)
#session.commit()
# I find that the 2nd approach doesn't allow the assignment of a key.  

#conn.close()