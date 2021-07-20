# Import all dependencies: 
################################################# 

import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import request

from flask import Flask, jsonify 

# Create connection to Hawaii.sqlite file
#################################################

connection_string = "postgres:postgres@localhost:5432/NFL_Fantasy_Data"
engine = create_engine(f'postgresql://{connection_string}')

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# # Save references to the measurement and station tables in the database
print(Base.classes.keys())
ADP = Base.classes.ADP_Data
DEF = Base.classes.DEF_Data
K = Base.classes.K_Data
Position_Dropdown = Base.classes.Position_dropdown
QB = Base.classes.QB_Data
RB = Base.classes.RB_Data
TE = Base.classes.TE_Data
WR = Base.classes.WR_Data
# Initialize Flask
#################################################
app = Flask(__name__)

# Create Flask Routes 

# Create root route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (

        f"/api/v1.0/position<br/>"
        f"/api/v1.0/ADP_Data<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"Note: to access values between a start and end date enter both dates using format: YYYY-mm-dd/YYYY-mm-dd"
    )

# Create a route that queries precipiation levels and dates and returns a dictionary using date as key and precipation as value
@app.route("/api/v1.0/position")
def position_drop_down():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation (prcp)and date (date) data"""
    
    # Create new variable to store results from query to Measurement table for prcp and date columns
    # position_query_results = session.query(Position_Dropdown.Position).all()

    # # Close session
    # session.close()

    # # Create a dictionary from the row data and append to a list of all_passengers
    #     # 1. Create an empty list of precipitation query values 
    #     # 2. Create for loop to iterate through query results (precipitation_query_results) 
    #     # 3. Create dictionary with key "precipitation" set to prcp from precipitation_query_results and key "date" to date from precipitation_query_results
    #     # 4. Append values from precipitation_dict to your original empty list precipitation_query_values 
    #     # 5. Return JSON format of your new list that now contains the dictionary of prcp and date values to your browser
    
    # position_query_values = []
    # for Position in position_query_results:
    #     position_dict = {}
    #     position_dict["Position"] = Position
    #     position_query_values.append(position_dict)

    # return jsonify(position_query_values) 

# Create a route that returns a JSON list of stations from the database
@app.route("/api/v1.0/ADP_Data")
def All_data(): 

    session = Session(engine)

    """Return a list of stations from the database""" 
    adp_query_results = session.query(ADP.Name,ADP.Position).all()

    session.close()  
    
    ADP_Data_values = []
    for name, position in adp_query_results:
        adp_values_dict = {}
        adp_values_dict['Name'] = name
        adp_values_dict['Position'] = position
        ADP_Data_values.append(adp_values_dict)
    return jsonify (ADP_Data_values) 

# # Create a route that queries the dates and temp observed for the most active station for the last year of data and returns a JSON list of the temps observed for the last year
# @app.route("/api/v1.0/tobs") 
# def tobs():
#     session = Session(engine)
    
#     """Return a list of dates and temps observed for the most active station for the last year of data from the database""" 
#     # Create query to find the last date in the database
    
#     last_year_query_results = session.query(Measurement.date).\
#         order_by(Measurement.date.desc()).first() 

#     print(last_year_query_results)
#     # last_year_date returns row ('2017-08-23',), use this to create a date time object to find start query date 
    
#     # check to see if last year was correctly returned by creating dictionary to return last year value to browser in JSON format
#     last_year_query_values = []
#     for date in last_year_query_results:
#         last_year_dict = {}
#         last_year_dict["date"] = date
#         last_year_query_values.append(last_year_dict) 
#     print(last_year_query_values)
#     # returns: [{'date': '2017-08-23'}]

#     # Create query_start_date by finding the difference between date time object of "2017-08-23" - 365 days
#     query_start_date = dt.date(2017, 8, 23)-dt.timedelta(days =365) 
#     print(query_start_date) 
#     # returns: 2016-08-23 

#     # Create query to find most active station in the database 

#     active_station= session.query(Measurement.station, func.count(Measurement.station)).\
#         order_by(func.count(Measurement.station).desc()).\
#         group_by(Measurement.station).first()
#     most_active_station = active_station[0] 

#     session.close() 
#      # active_station returns: ('USC00519281', 2772), index to get the first position to isolate most active station number
#     print(most_active_station)
#     # returns: USC00519281  

#     # Create a query to find dates and tobs for the most active station (USC00519281) within the last year (> 2016-08-23)

#     dates_tobs_last_year_query_results = session.query(Measurement.date, Measurement.tobs, Measurement.station).\
#         filter(Measurement.date > query_start_date).\
#         filter(Measurement.station == most_active_station) 
    

#     # Create a list of dates,tobs,and stations that will be appended with dictionary values for date, tobs, and station number queried above
#     dates_tobs_last_year_query_values = []
#     for date, tobs, station in dates_tobs_last_year_query_results:
#         dates_tobs_dict = {}
#         dates_tobs_dict["date"] = date
#         dates_tobs_dict["tobs"] = tobs
#         dates_tobs_dict["station"] = station
#         dates_tobs_last_year_query_values.append(dates_tobs_dict)
        
#     return jsonify(dates_tobs_last_year_query_values) 

# # Create a route that when given the start date only, returns the minimum, average, and maximum temperature observed for all dates greater than or equal to the start date entered by a user

# @app.route("/api/v1.0/<start>/<end>")
# # Define function, set "start" date entered by user as parameter for start_date decorator 
# def start_date(start):
#     session = Session(engine) 

#     """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date."""

#     # Create query for minimum, average, and max tobs where query date is greater than or equal to the date the user submits in URL
#     start_date_tobs_results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
#         filter(Measurement.date >= start).all()
    
#     session.close() 

#     # Create a list of min,max,and average temps that will be appended with dictionary values for min, max, and avg tobs queried above
#     start_date_tobs_values =[]
#     for min, avg, max in start_date_tobs_results:
#         start_date_tobs_dict = {}
#         start_date_tobs_dict["min"] = min
#         start_date_tobs_dict["average"] = avg
#         start_date_tobs_dict["max"] = max
#         start_date_tobs_values.append(start_date_tobs_dict)
    
#     return jsonify(start_date_tobs_values)

# # Create a route that when given the start date only, returns the minimum, average, and maximum temperature observed for all dates greater than or equal to the start date entered by a user

# @app.route("/api/v1.0/<start>/<end>")

# # Define function, set start and end dates entered by user as parameters for start_end_date decorator
# def Start_end_date(start, end):
#     session = Session(engine)

#     """Return a list of min, avg and max tobs between start and end dates entered"""
    
#     # Create query for minimum, average, and max tobs where query date is greater than or equal to the start date and less than or equal to end date user submits in URL

#     start_end_date_tobs_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#         filter(Measurement.date >= start).\
#         filter(Measurement.date <= end).all()

#     session.close()
  
#     # Create a list of min,max,and average temps that will be appended with dictionary values for min, max, and avg tobs queried above
#     start_end_tobs_date_values = []
#     for min, avg, max in start_end_date_tobs_results:
#         start_end_tobs_date_dict = {}
#         start_end_tobs_date_dict["min_temp"] = min
#         start_end_tobs_date_dict["avg_temp"] = avg
#         start_end_tobs_date_dict["max_temp"] = max
#         start_end_tobs_date_values.append(start_end_tobs_date_dict) 
    

#     return jsonify(start_end_tobs_date_values)
   
if __name__ == '__main__':
    app.run(debug=True) 
