import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as datetime

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect= True)

Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def ClimateData():
    return(
        f"Welcome to the Climate Data"
        f"Here's the available routes:"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/start"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)

    dt_string = '8/23/2017'
    recent_time = datetime.strptime(dt_string, "%m/%d/%Y")

    dt1_string = '8/23/2016'
    begin_time = datetime.strptime(dt1_string, '%m/%d/%Y')

    prcp = session.query(func.avg(Measurement.prcp), Measurement.date).\
    filter(Measurement.date <= recent_time).\
    filter(Measurement.date >= begin_time).group_by(Measurement.date).order_by(Measurement.date).all()
    prcp
    
    prcp_df = pd.DataFrame(prcp, columns = ['prcp', 'Date'])

    session.close()

    rain = []
    for date, prcp in prcp_df:
        rain_dict = {}
        rain_dict['date'] = date
        rain_dict['prcp'] = prcp
        rain.append(rain_dict)
    return jsonify(rain)


if __name__ == '__main__':
    app.run(debug=True)