import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

Base = automap_base()

Base.prepare(autoload_with=engine)


engine = create_engine("sqlite:///..//Resources//hawaii.sqlite")

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation from the last year"""
    prcp_year = session.query(measurement.date, measurement.prcp).filter(measurement.date >= '2016-08-23').all()

    session.close()

    # Convert list of tuples into normal list
    all_prcp = list(np.ravel(prcp_year))

    return jsonify(all_prcp)


@app.route("/api/v1.0/station")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the total number of stations
    
    query_station_count = session.query(station).count()
    
   

    return jsonify(query_station_count)

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
     # Query 
    active_station =  session.query(measurement.date, measurement.tobs).\
    filter(measurement.date >= 2016-8-23).\
    filter(measurement.station == 'USC00519281').\
    order_by(measurement.date).all()
    
    session.close()
    
    return_jsonify(active_station)
    
@app.route("/api/v1.0/start")
def start():
    
    session = Session(engine)
    user_date = input("Enter a start date in YYYY-MM-DD format: ")
    user_date_end = input("Enter an end date in YYYY-MM-DD format: ")

    session.query(measurement.date, measurement.tobs).\
    filter(measurement.date >= user_date).\
    filter(measurement.station == 'USC00519281').\
    order_by(measurement.date).all()
    
    query_high = session.query(measurement.station, func.max(measurement.tobs)).filter(measurement.station == 'USC00519281').all()
    query_low = session.query(measurement.station, func.min(measurement.tobs)).filter(measurement.station == 'USC00519281').all()
    query_avg = session.query(measurement.station, func.avg(measurement.tobs)).filter(measurement.station == 'USC00519281').all()
    start_date = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date >= 2016-8-23).\
    filter(measurement.station == 'USC00519281').\
    order_by(measurement.date).all()
    response = [query_high, query_low, query_avg] 
    session.close()
    
    return_jsonify(response)
    
@app.route("/api/v1.0/start/end")
def start_end():
    
    session = Session(engine)
    user_date = input("Enter a start date in YYYY-MM-DD format: ")
    user_date_end = input("Enter an end date in YYYY-MM-DD format: ")

    session.query(measurement.date, measurement.tobs).\
    filter(measurement.date >= user_date).\
    filter(measurement.date <= user_date_end).\
    filter(measurement.station == 'USC00519281').\
    order_by(measurement.date).all()
    
    query_high = session.query(measurement.station, func.max(measurement.tobs)).filter(measurement.station == 'USC00519281').all()
    query_low = session.query(measurement.station, func.min(measurement.tobs)).filter(measurement.station == 'USC00519281').all()
    query_avg = session.query(measurement.station, func.avg(measurement.tobs)).filter(measurement.station == 'USC00519281').all()
    start_date = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date >= 2016-8-23).\
    filter(measurement.station == 'USC00519281').\
    order_by(measurement.date).all()
    response = [query_high, query_low, query_avg] 
    session.close()
    
    return_jsonify(response)



if __name__ == '__main__':
    app.run()
