# Import the dependencies.

%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, text

from datetime import datetime, timedelta

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(autoload_with = engine)

# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """Start at the homepage"""
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api.v1.0/<start><br/>"
        f"/api.v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def.precipitation():
    """Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value."""
    """Return the JSON representation of your dictionary."""
    
    # Create a session (link) from Python to the DB
    
    session = Session(engine)
    
    # Query all participation values based on the date
    
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()

    # Convert list of tupules into Dictionary
    # Create a dictionary from the row data and append to a list of precipitation values
    
    all_precipitation = []
    for date, prcp in results:
        precipitation_dictionary = {}
        precitipation_dictionary[date] = prcp
        all_precipitation.append(precipitation_dictionary)
    
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def.stations():
    """Return a JSON list of stations from the dataset."""
    
    # Create a session (link) from Python to the DB
    
    session = Session(engine)
    
    # Query all stations
    
    results = session.query(Station.id, Station.station, Station.name, Station.latitue, Station.longitude, Station.elevation).all()
    
    session.close()
    
    # Create a dictionary from the row data and append to a list of all stations values
    
    all_stations = []
    for id,station,name,latitude,longitude,elevation in results:
        station_dictionary = {}
        
        station_dictionary['Id'] = id
        station_dictionary['station'] = station
        station_dictionary['name'] = name
        station_dictionary['latitude'] = latitude
        station_dictionary['longitude'] = longitude
        station_dictionary['elevation'] = elevation
        
        all_stations.append(station_dictionary)
     
    return jsonify(all_stations)

@ app.route("/api/v1.0/tobs")
def.tobs():
    """Query the dates and temperature observations of the most-active station for the previous year of data."""
    """Return a JSON list of temperature observations for the previous year."""
    
    # Create a session (link) from Python to the DB
    
    session = Session(engine)
    
    # Query the last 12 months of precipitation data
    
    last_data_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    
    formated_last_data_date = datetime.strptime(last_data_date, "%Y-%m-%d")

    date_one_year_ago = formated_last_data_date - timedelta(days = 365)
    
    # Perform a query to retrieve the data and precipitation scores
    
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= date_one_year_ago).all()
    
    session.close()
    
    # Create a dictionary from the row data and append to a list of temperatures
    
    all_temperatures = []
    for tobs, date in results:
        tobs_dictionary = {}
        
        tobs_dictionary['date'] = date
        tobs_dictionary['tobs'] = tobs
        
        all_temperatures.append(tobs_dictionary)
     
    return jsonify(all_temperatures)

@app.route("/api/v1.0/<start>/<end>")
def.start_end_temperatures():
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range."""
    """For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date."""
    """For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive."""
    
    # Create a session (link) from Python to the DB
    
    session = Session(engine)
    
    results_tobs = session.query(Measurement.tobs).\
        filter(Measurement.station == stations_measurements_rows[0][0]).\
        filter(Measurement.date >= date_one_year_ago).all()

    temperatures = session.query(
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)).all()
    
    temperature_values = {}
    temperature_values[func.min(Measurement.tobs) = temp_min
    temperature_values[func.max(Measurement.tobs) = temp_max
    temperature_values[func.avg(Measurement.tobs) = temp_avg
    
    return jsonify(temperature_values)

@ app.route("api/v1.0/<start>")
def.start_temperatures():
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range."""
    """For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date."""
    """For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive."""
    
    # Create a session (link) from Python to the DB
    
    session = Session(engine)
    
    results_tobs = session.query(Measurement.tobs).\
        filter(Measurement.station == stations_measurements_rows[0][0]).\
        filter(Measurement.date >= date_one_year_ago).all()

    temperatures = session.query(
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)).all()
    
    temperature_values = {}
    temperature_values[func.min(Measurement.tobs) = temp_min
    temperature_values[func.max(Measurement.tobs) = temp_max
    temperature_values[func.avg(Measurement.tobs) = temp_avg
    
    return jsonify(temperature_values)

if __name__ == '__main__':
    app.run(debug=True)
    
 

    




