# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 10:45:10 2018
review the table you created. 
@author: joelee
"""
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, MetaData, Table , select, or_ , and_

# Create engine using the `gtdb.sqlite` database file
engine = create_engine("mysql://gtdb_admin:ktjljmjj@gtdb-insta.csuho8dvfguv.us-east-1.rds.amazonaws.com:3306/gtdb")
conn = engine.connect()

## I found that the class activity is garbage, and does not accurately reflect a well-formed table.  
## Declare a Base using `automap_base()
#Base = automap_base()
## Use the Base class to reflect the database tables
#Base.prepare(engine, reflect=True)
## Print all of the classes mapped to the Base
#
#print (Base.classes.keys())
#
#mykey = Base.classes.incident_id
#session = Session(engine)
#
#first_row = Session.query(mykey).first()
#print(first_row.__dict__)
#
#for row in session.query(mykey.stock, mykey.volume, mykey.percent_change).limit(15):
#    print(row)

# Using googled references instead:  
inspector = inspect(engine)

# Get table information
print (inspector.get_table_names())

# Get column information
print (inspector.get_columns('incidents_tbl'))


# Create a MetaData instance

meta = MetaData(engine,reflect=True)
table = meta.tables['incidents_tbl']
print (table)

select_st = select([table]).where(
   table.c.iyear == '2001')
res = conn.execute(select_st)
for _row in res: print (_row)