#dependencies
from flask import Flask, jsonify
import numpy as np
import datetime as dt


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect


engine =create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(engine, reflect=True)

# Save references to each table
Measurement = base.classes.measurement 
Station = base.classes.station


#find most recent date in data set
session = Session(engine)

max_date = session.query(func.max(Measurement.date)).all()

first_date = session.query(func.min(Measurement.date)).all()

query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

session.close()


#create an app 
app = Flask(__name__)


#flask routes
@app.route("/")
def home():
	return (f"List of available routes:<br/>"
		f"<br/>"
		f"/api/v1.0/precipitation<br/>"
		f"/api/v1.0/stations<br/>"
		f"/api/v1.0/tobs<br/>"
		f"/api/v1.0/first_date<br/>"
		f"/api/v1.0/<start>/<end><br/>"
		)


@app.route("/api/v1.0/precipitation")
def precipitation():

	session = Session(engine)
	sel = [Measurement.date, Measurement.prcp]
	result = session.query(*sel).all()
	session.close()

	precipitation = []

	for date, prcp in result:
		prcp_dict = {}
		prcp_dict["Date"] = date
		prcp_dict["Precipitation"] = prcp
		precipitation.append(prcp_dict)

	return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():

	session = Session(engine)
	sel = [Station.name]
	result = session.query(*sel).all()
	session.close()

	stations = []

	for name in result:
		stations.append(name)

	return jsonify(stations)

      
@app.route("/api/v1.0/tobs")
def tobs():
	session = Session(engine)
	sel = [Measurement.tobs, Measurement.date]
	result = session.query(*sel).filter(Measurement.date >= query_date)
	session.close()

	temp_observations = []

	for tobs, date in result:
		temp_observations_dict = {}
		temp_observations_dict["Date"] = date
		temp_observations_dict["Temperature"] = tobs
		temp_observations.append(temp_observations_dict)

	return jsonify(temp_observations)


@app.route("/api/v1.0/start/")
def start():
	session = Session(engine)
	sel = [Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs, func.avg(Measurement.tobs))]
	result = session.query(*sel).filter(Measurement.tobs >= first_date)
	session.close()

	temperatures = []

	for date, tobs in result:

		temp_dict = {}
		temp_dict["Date"] = first_date
		temp_dict["Minimum Temp"] = result[1]
		temp_dict["Maximum Temp"] = result[2]
		temp_dict["Average Temp"] = result[3]
		temperatures.append(temp_dict)

	return jsonify(temperatures)

	session.close()



#define the main behavior
if __name__ == "__main__":
	app.run(debug=True)
	