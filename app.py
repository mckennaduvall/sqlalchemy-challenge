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


	




#define the main behavior
if __name__ == "__main__":
	app.run(debug=True)
	