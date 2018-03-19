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
from sqlalchemy import create_engine

# Create engine using the `gtdb.sqlite` database file
engine = create_engine("sqlite:///gtdb.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)
# Print all of the classes mapped to the Base
Base.classes.keys()

# Create a session
session = Session(engine)

first_row = session.query().first()
first_row.__dict__