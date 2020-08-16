import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route('/api/v1.0/precipitation')
def precipitation():
    
    session = Session(engine)
    
    results1 = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()
    
    all_prcp = []
    for date, prcp in results1:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        all_prcp.append(prcp_dict)
        
    return jsonify(all_prcp)

@app.route('/api/v1.0/stations')
def stations():
    
    session = Session(engine)
    
    results2 = session.query(Station.name).all()
    
    session.close()
    
    all_stations = list(np.ravel(results2))
    
    return jsonify(all_stations)

@app.route('/api/v1.0/tobs')
def tobs():
    
    session = Session(engine)
   
    results3 = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281', Measurement.date>='2016-08-18').all()
    
    session.close()
    
    all_tobs = []
    for date, tobs in results3:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['temp'] = tobs
        all_tobs.append(tobs_dict)
    
    return jsonify(all_tobs)

@app.route('/api/v1.0/<start>')
def measurement_date(start):
    
    session = Session(engine)
        
    results_start = session.query(func.max(Measurement.tobs)\
                                .filter(Measurement.date>=start),
                                func.min(Measurement.tobs)\
                                .filter(Measurement.date>=start),
                                func.avg(Measurement.tobs)\
                                .filter(Measurement.date>=start))

    session.close()
    
    start_tobs = []
    for ma,mi,avg in results_start:
        start_dict={}
        start_dict['TMAX'] = ma
        start_dict['TMIN'] = mi
        start_dict['TAVG'] = avg
        start_tobs.append(start_dict)
    
    return jsonify(start_tobs)
 
@app.route('/api/v1.0/<start>/<end>')
def measurement_range(start, end):
    
    session = Session(engine)

    results_end = session.query(func.max(Measurement.tobs)\
                                .filter(Measurement.date>=start).filter(Measurement.date<=end),
                                func.min(Measurement.tobs)\
                                .filter(Measurement.date>=start).filter(Measurement.date<=end),
                                func.avg(Measurement.tobs)\
                                .filter(Measurement.date>=start).filter(Measurement.date<=end))
    
    session.close()
    
    range_tobs = []
    for ma,mi,avg in results_end:
        range_dict={}
        range_dict['TMAX'] = ma
        range_dict['TMIN'] = mi
        range_dict['TAVG'] = avg
        range_tobs.append(range_dict)
    
    return jsonify(range_tobs)
                                

if __name__ == '__main__':
    app.run(debug=True)