import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of dates and temperature observations from the last year"""
    # 
    today = dt.date.today()
    ayear =  dt.timedelta(days=365)
    year_ago = (today - ayear).isoformat()
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > year_ago).all()
    results = dict(results)

    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations():
    """Return a json list of stations from the dataset"""
    # 
    results = session.query(Station.station).group_by(Station.station).all()
    list_results = [x[0] for x in results]
    list_results

    return jsonify(list_results)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a json list of Temperature Observations (tobs) for the previous year"""
    # 
    today = dt.date.today()
    ayear =  dt.timedelta(days=365)
    year_ago = (today - ayear).isoformat()
    results = session.query(Measurement.tobs).filter(Measurement.date > year_ago).all()

    return jsonify(results)

@app.route("/api/v1.0/<start>")
def temp_stats(start):
    """ json list of the minimum temperature, the average temperature, 
        and the max temperature for a given start """

    results = session.query(Measurement.tobs).filter(Measurement.date > start).all()
    list_results = [np.min(results), np.max(results), np.mean(results)]

    return jsonify(list_results), 404


@app.route("/api/v1.0/<start>/<end>")
def temp_stats_range(start, end):
    """ Return json list of the minimum temperature, the average temperature, 
        and the max temperature for a given start/end dates """

    results = session.query(Measurement.tobs).filter(Measurement.date > start)\
        .filtes(Measurement.date < end).all()
    list_results = [np.min(results), np.max(results), np.mean(results)]

    return jsonify(list_results), 404

if __name__ == '__main__':
    app.run(debug=True)
