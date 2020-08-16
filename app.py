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
    
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()
    
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        all_prcp.append(prcp_dict)
        
    return jsonify(all_prcp)

@app.route('/api/v1.0/stations')
def stations():
    
    session = Session(engine)
    
    results = session.query(Station.station, Station.name).all()
    
    session.close()
    
    all_stations = list(np.ravel(results))
    
    return jsonify(all_stations)

@app.route('/api/v1.0/tobs')
def tobs():
    
    session = Session(engine)
   
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281', Measurement.date>='2016-08-18').all()
    
    session.close()
    
    all_tobs = list(np.ravel(results))
    
    return jsonify(all_tobs)

@app.route('/api/v1.0/<start>')
def measurement_date(start):
    
    session = Session(engine)
    
    print(request.args['start'])
    
    if 'start' in request.args:
        start = request.args['start']
    else:
        return "Error: No start date provided. Please provide a date (YYYY-MM-DD)."
    
    results = session.query(func.max(Measurement.tobs).label('TMAX')\
                                .filter(Measurement.date>=start),
                                func.min(Measurement.tobs).label('TMIN')\
                                .filter(Measurement.date>=start),
                                func.avg(Measurement.tobs).label('TAVG')\
                                .filter(Measurement.date>=start))

    session.close()
    
    start_tobs = list(np.ravel(results))
    
    return jsonify(start_tobs)
 
@app.route('/api/v1.0/<start>/<end>')
def measurement_date_range(start, end):
    
    session = Session(engine)
    
    print(request.args['start'])
    print(request.args['end'])
    
    if 'start' in request.args:
        start = request.args['start']
    else:
        return "Error: No start date provided. Please provide a date (YYYY-MM-DD)."
                                
    if 'end' in request.args:
        end = request.args['end']
    else:
        return "Error: No end date provided. Please provide a date (YYYY-MM-DD)."

    results = session.query(func.max(Measurement.tobs).label('TMAX')\
                                .filter(Measurement.date>=start).filter(Measurement.date<=end),
                                func.min(Measurement.tobs).label('TMIN')\
                                .filter(Measurement.date>=start).filter(Measurement.date<=end),
                                func.avg(Measurement.tobs).label('TAVG')\
                                .filter(Measurement.date>=start).filter(Measurement.date<=end))
    
    session.close()
    
    range_tobs = list(np.ravel(results))
    
    return jsonify(range_tobs)
                                

if __name__ == '__main__':
    app.run(debug=True)