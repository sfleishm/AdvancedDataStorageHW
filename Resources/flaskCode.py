import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# 10.3 Activity 10 for most of this stuff


engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB

app = Flask(__name__)



@app.route("/")
def home():
    print("Moving to the Home Page")
    return ("Welcome to the Home Page <p>\
        Here are the routes for this homework assignment:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    mdate = Base.classes.measurement
    #results = session.query(mdate.station).all()
    #stations = []
    weatherStuff = []
    prcpData = session.query(mdate.date, mdate.prcp).\
        filter(mdate.date >= '2016-08-23').\
        order_by(mdate.date).all()
    #prcpData
    #for station in results:
    #    station_dict = {}
    #    station_dict["station"] = station
    #    stations.append(station_dict)
    for date, prcp in prcpData:
        weatherData = {}
        weatherData["date"] = date
        weatherData["prcp"] = prcp
        weatherStuff.append(weatherData)
    
#session.query(func.count(mdate.date)).all()
# grabs the first date - 2010-01-01
#session.query(mdate.date).order_by(mdate.date).first()
# grabs the last date - 2017-08-23
#session.query(mdate.date).order_by(mdate.date.desc()).first()
    #prcpData = session.query(mdate.date, mdate.prcp).\
    #    filter(mdate.date >= '2016-08-23').\
    #    order_by(mdate.date).all()
    #prcpData
    print("You are navigating to the precipitation")
    #return(jsonify(stations))
    return(jsonify(weatherStuff))


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stationData = Base.classes.station
    stationInfo = []
    stationQuery = session.query(stationData.station, stationData.name, \
        stationData.latitude, stationData.longitude, stationData.elevation)\
        .group_by(stationData.station)

    for station, name, latitude, longitude, elevation in stationQuery:
        stationDict = {}
        stationDict["station"] = station
        stationDict["name"] = name
        stationDict["latitude"] = latitude
        stationDict["longitude"] = longitude
        stationDict["elevation"] = elevation
        stationInfo.append(stationDict)
    print("You are navigating to the stations section")
    return(jsonify(stationInfo))

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    mdate = Base.classes.measurement
    tobsData = []
    tobsQuery = session.query(mdate.tobs,mdate.date).\
        filter(mdate.station=='USC00519281').\
        filter(mdate.date >= '2016-08-23')
    
    for tobs, date in tobsQuery:
        tobsDict = {}
        tobsDict["tobs"] = tobs
        tobsDict["date"] = date
        tobsData.append(tobsDict)
    print("Navigating to USC00519281 past year data")
    #return("USC00519281 past year data")
    return(jsonify(tobsData))

# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps(start_date, end_date):
    session = Session(engine)
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    #first = start_date
    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    return jsonify(query)
    #return(start_date)
    #return str(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    #    filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all())
    #return(session.query)
    #print(calc_temps('2012-02-28','2012-03-05'))
    #return (start_date, end_date)
    #return (end_date)
    #return (f"{start_date},{end_date}") # this works
#this will return the start date correctly

@app.route("/api/v1.0/<start_date>")
def calc_temps2(start_date):
    session = Session(engine)

    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    #query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    return jsonify(query)

if __name__ == "__main__":
    app.run(debug=True)
