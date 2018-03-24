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

#engine = create_engine("mysql://gtdb_admin:ktjljmjj@gtdb-insta.csuho8dvfguv.us-east-1.rds.amazonaws.com:3306/gtdb")
engine = create_engine("mysql://gtdb_admin:ktjljmjj@127.0.0.1:3306/gtdb")
conn = engine.connect()

# Create a "Metadata" Layer That Abstracts our SQL Database
# ----------------------------------
Base.metadata.create_all(engine)

# Create a Session Object to Connect to DB
# ----------------------------------
session = Session(bind=engine)
  
#  test query printed to screen -- to be deleted
# incident_list = session.query(Incidents)
# for incident in incident_list:
#     print(incident.incident_id, incident.iyear, incident.icountry_txt,
#           incident.ilatitude, incident.ilongitude)

# for each_year in range (2000 , 2016):
#     i_of_a_year = session.query(Incidents).filter(Incidents.iyear==each_year).count()
#     print(each_year, "", i_of_a_year)


#################################################
# Flask Setup
#################################################
from flask import Flask, jsonify, render_template
from flask.ext.cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
# app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
# app.config['CORS_HEADERS'] = 'Content-Type'



#################################################
# Navigation Routes
#################################################


@app.route('/')  # index.html
def index():
    return render_template('index.html')

# Commented out the below endpoints, because I 
# think we can just nav to these from the index 
# page.  
@app.route('/terrorHeatMap')  # heatmap
def heatmapit():
    return render_template('terrorHeatMap.html')

@app.route('/terrorExplorerMap')  # heatmap
def explorermapit():
    return render_template('terrorExplorer.html')

# @app.route('/chloropleth_page')  # chloropleth
# def chloroplethit(chloropleth_page):
#     return render_template('chloropleth_page.html')

@app.route('/chloropleth_page')  # chloropleth
def chloroplethit(chloropleth_page):
    return render_template('chloropleth_page.html')



#################################################
# Datacall Routes
#################################################
# cors = CORS(app, resources={r"/incident_locs/": {"origins": "http://localhost:5000"}}) #http://localhost:5000
@app.route ("/incident_locs/")
# @cross_origin(origin='localhost',headers=['Content- Type']) #@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def incident_locs():
  yr_incident_list = []
  incident_list =  session.query(Incidents)
  for incident in incident_list:
    incident_details = {}
    location_details = {}
    location_details["latitude"] = str(incident.ilatitude)
    location_details["longitude"] = str(incident.ilongitude)
    incident_details["incident_year"] = str(incident.iyear)
    incident_details["location"] = location_details
    yr_incident_list.append(incident_details)
  json_yr_incident_list = jsonify(yr_incident_list)
  # json_yr_incident_list.headers.add('Access-Control-Allow-Origin', '*')
  return json_yr_incident_list

@app.route ("/incident_locs/<chosen_year>")
def incident_coords(chosen_year):
  yr_incident_list = []
  incident_list =  session.query(Incidents).filter(Incidents.iyear==chosen_year)
  for incident in incident_list:  
    incident_details = {}
    location_details = {}
    location_details["latitude"] = str(incident.ilatitude)
    location_details["longitude"] = str(incident.ilongitude)
    incident_details["incident_year"] = str(incident.iyear)
    incident_details["location"] = location_details
    incident_details["nkill"] = str(incident.nkill)
    yr_incident_list.append(incident_details)
  json_yr_incident_list = jsonify(yr_incident_list)
  # json_yr_incident_list.headers.add('Access-Control-Allow-Origin')
  return json_yr_incident_list



  # query_result = [ {
  #   "year" : "2016",  
  #   "location" : {
  #     "latitude" : "37.75996673124653",
  #     "longitude" : "-122.42364395748542"
  #   },
  # }
  # , {
  #   "year" : "2015",
  #   "location" : {
  #     "latitude" : "37.78398055926338",
  #     "longitude" : "-122.41177829599216"
  #   },
  # }
  # ]
#  Use superheros as an example, passing in a year, and then quyering for 
# the results related to that year.  
# This part is not correct/complete yet.  lEave as a placeholder for now.
# mock data
  # return jsonify(query_result)



# @app.route ("/incident_facts")
# def incident_coords_facts():

#   incident_details = []
#   incident_list = session.query(Incidents).filter(Incidents.iyear==chosen_year)
#   for incident in incident_list:
#     incident_details = {}
#     incident_details["incident_year"] = incident.iyear
#     incident_details["latitude"] = incident.ilatitude
#     incident_details["longitude"] = incident.ilongitude
#     incident_details["nkills"] = incident.nkills
#     query_result.append(incident_details)
#   return jsonify(incident_details)



  # query_result2 = [ {
  #   "year" : "2016",
  #   "location" : {
  #     "latitude" : "37.742956117638094",
  #     "longitude" : "-122.47783489270445"
  #   },
  #   "nkill" : "14",
  #   }
  #   ]
  # return jsonify(query_result2)
#  Use superheros as an example, passing in a year, and then quyering for 
# the results related to that year, including the facts
# This part is not correct/complete yet.  lEave as a placeholder for now.

# mock data

# @app.route("/api/v1.0/justice-league/superhero/<superhero>")
# def justice_league_by_superhero__name(superhero):
"""Fetch the Justice League character whose superhero matches
       the path variable supplied by the user, or a 404 if not."""
   


if __name__ == "__main__":
    app.run(debug=True)


