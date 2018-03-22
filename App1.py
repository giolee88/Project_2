#################################################
# Database Setup
#################################################
# import necessary libraries
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.ext.automap import automap_base # automap is not picking up our PK
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float  
# Import PyMySQL (Not needed if mysqlclient is installed)
import pymysql

Base = declarative_base()
pymysql.install_as_MySQLdb()


# explicitly create my table definition
class Incidents(Base):
    __tablename__ = 'incidents_tbl'
    incident_id = Column(Integer, primary_key=True)
    iyear = Column(Integer)             
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
    property = Column (Integer)

engine = create_engine("mysql://gtdb_admin:ktjljmjj@gtdb-insta.csuho8dvfguv.us-east-1.rds.amazonaws.com:3306/gtdb")
conn = engine.connect()

# Create a "Metadata" Layer That Abstracts our SQL Database
# ----------------------------------
Base.metadata.create_all(engine)

# Create a Session Object to Connect to DB
# ----------------------------------
session = Session(bind=engine)
  
#  test query printed to screen -- to be deleted
incident_list = session.query(Incidents)
for incident in incident_list:
    print(incident.incident_id, incident.iyear, incident.icountry_txt,
          incident.ilatitude, incident.ilongitude)

for each_year in range (2000 , 2016):
    i_of_a_year = session.query(Incidents).filter(Incidents.iyear==each_year).count()
    print(each_year, "", i_of_a_year)


#################################################
# Flask Setup
#################################################
from flask import Flask, jsonify

app = Flask(__name__)

#################################################
# Navigation Routes
#################################################
@app.route('/')  # index.html
def index():
    return render_template('index.html')

# Commented out the below endpoints, because I 
# think we can just nav to these from the index 
# page.  
# @app.route('/heatmap_page')  # heatmap
# def heatmapit(heatmap_page):
#     return render_template('heatmap_page.html')

# @app.route('/chloropleth_page')  # chloropleth
# def chloroplethit(chloropleth_page):
#     return render_template('chloropleth_page.html')


#################################################
# Datacall Routes
#################################################

@app.route ("/incident_locs")
def incident_coords(incident_locs):
#  Use superheros as an example, passing in a year, and then quyering for 
# the results related to that year.  
# This part is not correct/complete yet.  lEave as a placeholder for now.

# mock data
query_result = 
[ {
  "year" : "2016"
  "location" : {
    "latitude" : "37.75996673124653",
    "longitude" : "-122.42364395748542"
  },
}
, {
  "year" : "2016",
  "location" : {
    "latitude" : "37.78398055926338",
    "longitude" : "-122.41177829599216"
  },
}
]

return jsonify(query_result)


@app.route ("/incident_facts")
def incident_coords_facts(incident_facts):
#  Use superheros as an example, passing in a year, and then quyering for 
# the results related to that year, including the facts
# This part is not correct/complete yet.  lEave as a placeholder for now.

# mock data
query_result = [ {
  "year" : "2016",
  "location" : {
    "latitude" : "37.742956117638094",
    "longitude" : "-122.47783489270445"
  },
  "nkill" : "14",
}
]
return jsonify(query_result)



if __name__ == "__main__":
    app.run(debug=True)


