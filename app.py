# Import all dependencies: 
################################################# 

import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import request

from flask import Flask, jsonify, render_template 

# Create connection to Hawaii.sqlite file
#################################################

connection_string = "rhbomegpaemmdu:dfb3901ad0e550f6aec9f2bf1b1b7eed52a6321eed339d95ce702e36c5963181@ec2-54-83-82-187.compute-1.amazonaws.com:5432/d2eke12h3f7nqb"
engine = create_engine(f'postgresql://{connection_string}')

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the measurement and station tables in the database
# print(Base.metadata.tables.keys())
print(Base.metadata.tables.keys())
ADP = Base.metadata.tables['ADP_Data']
# print(ADP)
DEF = Base.metadata.tables['DEF_Data']
K = Base.metadata.tables['K_Data']
Position_Dropdown = Base.metadata.tables['Position_dropdown']
QB = Base.metadata.tables['QB_Data']
RB = Base.metadata.tables['RB_Data']
TE = Base.metadata.tables['TE_Data']
WR = Base.metadata.tables['WR_Data']
Highlights = Base.metadata.tables['Highlights_Data']
BoxPlot = Base.metadata.tables['BoxPlot']

# Initialize Flask
#################################################
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False   

# Create Flask Routes 

# Create root route
@app.route("/")
def welcome(): 
    return render_template("index.html")

@app.route("/about.html")
def about():
    return render_template("about.html") 

@app.route("/index.html")
def home(): 
    return render_template("index.html") 
    
@app.route("/predictions.html")
def predictions(): 
    return render_template("predictions.html")

@app.route("/api/v1.0/Highlights")
def highlights_data():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation (prcp)and date (date) data"""
    
    # Create new variable to store results from query to Measurement table for prcp and date columns
    adp_query_results = session.query(Highlights.c.Name,Highlights.c.Team, Highlights.c.Position,Highlights.c.AverageDraftPosition,Highlights.c.AverageDraftPositionPPR, Highlights.c.ByeWeek,Highlights.c.LastSeasonFantasyPoints,Highlights.c.ProjectedFantasyPoints).all()

    # Close session
    session.close()

    # # Create a dictionary from the row data and append to a list of position_query_values
    # Below steps explain how all loops in all Flask Routes for JSON data will work
    #     # 1. Create an empty list of position query values 
    #     # 2. Create for loop to iterate through query results (position_query_results) 
    #     # 4. Append values from precipitation_dict to your original empty list position_query_values 
    #     # 5. Return JSON format of your new list that now contains the dictionary of position values to your browser
    
    highlights_query_values = []
    for name, team, position,averagedraftposition,averagedraftpositionppr, byeweek, lastseasonfantasypoints, projectedfantasypoints in adp_query_results:
        highlights_values_dict = {}
        highlights_values_dict['Name'] = name
        highlights_values_dict['Team'] = team
        highlights_values_dict['Position'] = position
        highlights_values_dict['AverageDraftPosition'] = averagedraftposition
        highlights_values_dict['AverageDraftPositionPPR'] =averagedraftpositionppr
        highlights_values_dict['ByeWeek'] = byeweek
        highlights_values_dict['LastSeasonFantasyPoints'] = lastseasonfantasypoints
        highlights_values_dict['ProjectedFantasyPoints'] = projectedfantasypoints
        highlights_query_values.append(highlights_values_dict) 
    return jsonify(highlights_query_values) 

#Create all distinct routes to return JSONIFIED Data for each position full stats and dropdown data

@app.route("/api/v1.0/ADP_Data")
def adp_data():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation (prcp)and date (date) data"""
    
    # Create new variable to store results from query to Measurement table for prcp and date columns
    adp_query_results = session.query(ADP.c.Name,ADP.c.Team, ADP.c.Position,ADP.c.AverageDraftPosition,ADP.c.AverageDraftPositionPPR, ADP.c.ByeWeek,ADP.c.LastSeasonFantasyPoints,ADP.c.ProjectedFantasyPoints).all()

    # Close session
    session.close()

    # # Create a dictionary from the row data and append to a list of position_query_values
    # Below steps explain how all loops in all Flask Routes for JSON data will work
    #     # 1. Create an empty list of position query values 
    #     # 2. Create for loop to iterate through query results (position_query_results) 
    #     # 4. Append values from precipitation_dict to your original empty list position_query_values 
    #     # 5. Return JSON format of your new list that now contains the dictionary of position values to your browser
    
    adp_query_values = []
    for name, team, position,averagedraftposition,averagedraftpositionppr, byeweek, lastseasonfantasypoints, projectedfantasypoints in adp_query_results:
        adp_values_dict = {}
        adp_values_dict['Name'] = name
        adp_values_dict['Team'] = team
        adp_values_dict['Position'] = position
        adp_values_dict['AverageDraftPosition'] = averagedraftposition
        adp_values_dict['AverageDraftPositionPPR'] =averagedraftpositionppr
        adp_values_dict['ByeWeek'] = byeweek
        adp_values_dict['LastSeasonFantasyPoints'] = lastseasonfantasypoints
        adp_values_dict['ProjectedFantasyPoints'] = projectedfantasypoints
        adp_query_values.append(adp_values_dict) 
    return jsonify(adp_query_values)  

@app.route("/api/v1.0/Projected_Data")
def projected_data():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation (prcp)and date (date) data"""
    
    # Create new variable to store results from query to Measurement table for prcp and date columns
    projected_query_results = session.query(BoxPlot.c.NAME,BoxPlot.c.POSITION,BoxPlot.c.PROJECTED_POINTS).all()
    print(position_query_results)
    # Close session
    session.close()

    # # Create a dictionary from the row data and append to a list of position_query_values
    # Below steps explain how all loops in all Flask Routes for JSON data will work
    #     # 1. Create an empty list of position query values 
    #     # 2. Create for loop to iterate through query results (position_query_results) 
    #     # 4. Append values from precipitation_dict to your original empty list position_query_values 
    #     # 5. Return JSON format of your new list that now contains the dictionary of position values to your browser
    
    projected_query_values = []
    for name, position,projectedfantasypoints in projected_query_results:
        adp_values_dict = {}
        adp_values_dict['NAME'] = name
        adp_values_dict['POSITION'] = position
        adp_values_dict['PROJECTED_POINTS'] = projectedfantasypoints
        projected_query_values.append(adp_values_dict) 
    return jsonify(projected_query_values)



@app.route("/api/v1.0/position")
def position_drop_down_data():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation (prcp)and date (date) data"""
    
    # Create new variable to store results from query to Measurement table for prcp and date columns
    position_query_results = session.query(Position_Dropdown.c.Position).all()

    print(position_query_results)
    # Close session
    session.close()

    # # Create a dictionary from the row data and append to a list of position_query_values
    # Below steps explain how all loops in all Flask Routes for JSON data will work
    #     # 1. Create an empty list of position query values 
    #     # 2. Create for loop to iterate through query results (position_query_results) 
    #     # 4. Append values from precipitation_dict to your original empty list position_query_values 
    #     # 5. Return JSON format of your new list that now contains the dictionary of position values to your browser
    
    position_query_values = []
    for Position in position_query_results:
        print(Position)
        position_dict = {}
        position_dict["Position"] = Position[0]
        position_query_values.append(position_dict)

    return jsonify(position_query_values) 

# Create a route that returns a JSON list of DEF Player Stats from the database
# @app.route("/api/v1.0/DEF")
def DEF_Data(): 

    session = Session(engine)

#     """Return a list of all columns from the DEF table in the database""" 
    def_query_results = session.query(DEF.c.Name, DEF.c.Team, DEF.c.Position, DEF.c.AverageDraftPosition, DEF.c.AverageDraftPositionPPR,DEF.c.ByeWeek, DEF.c.LastSeasonFantasyPoints,DEF.c.ProjectedFantasyPoints).all()

#     session.close()  
    
    DEF_Data_values = []
    for name, team, position,averagedraftposition,averagedraftpositionppr, byeweek, lastseasonfantasypoints, projectedfantasypoints in def_query_results:
        # print(name, team, position,averagedraftposition,averagedraftpositionppr, byeweek, lastseasonfantasypoints, projectedfantasypoints)
        def_values_dict = {}
        def_values_dict['Name'] = name
        def_values_dict['Team'] = team
        def_values_dict['Position'] = position
        def_values_dict['AverageDraftPosition'] = averagedraftposition
        def_values_dict['AverageDraftPositionPPR'] =averagedraftpositionppr
        def_values_dict['ByeWeek'] = byeweek
        def_values_dict['LastSeasonFantasyPoints'] = lastseasonfantasypoints
        def_values_dict['ProjectedFantasyPoints'] = projectedfantasypoints
        DEF_Data_values.append(def_values_dict)
    return jsonify (DEF_Data_values)  

@app.route("/api/v1.0/K")
def K_Data(): 

    session = Session(engine)

    """Return a list of all columns from the K table from the database""" 
    def_query_results = session.query(K.c.Name, K.c.Team, K.c.Position, K.c.AverageDraftPosition, K.c.AverageDraftPositionPPR,K.c.ByeWeek, K.c.LastSeasonFantasyPoints,K.c.ProjectedFantasyPoints).all()

    session.close()  
    
    K_Data_values = []
    for name, team, position,averagedraftposition,averagedraftpositionppr, byeweek, lastseasonfantasypoints, projectedfantasypoints in def_query_results:
        K_values_dict = {}
        K_values_dict['Name'] = name
        K_values_dict['Team'] = team
        K_values_dict['Position'] = position
        K_values_dict['AverageDraftPosition'] = averagedraftposition
        K_values_dict['AverageDraftPositionPPR'] =averagedraftpositionppr
        K_values_dict['ByeWeek'] = byeweek
        K_values_dict['LastSeasonFantasyPoints'] = lastseasonfantasypoints
        K_values_dict['ProjectedFantasyPoints'] = projectedfantasypoints
        K_Data_values.append(K_values_dict)
    return jsonify (K_Data_values)  

@app.route("/api/v1.0/QB")
def QB_Data(): 

    session = Session(engine)

    """Return a list of all columns from the QB table from the database""" 
    def_query_results = session.query(QB.c.Name, QB.c.Team, QB.c.Position, QB.c.AverageDraftPosition, QB.c.AverageDraftPositionPPR,QB.c.ByeWeek, QB.c.LastSeasonFantasyPoints,QB.c.ProjectedFantasyPoints).all()

    session.close()  
    
    QB_Data_values = []
    for name, team, position,averagedraftposition,averagedraftpositionppr, byeweek, lastseasonfantasypoints, projectedfantasypoints in def_query_results:
        QB_values_dict = {}
        QB_values_dict['Name'] = name
        QB_values_dict['Team'] = team
        QB_values_dict['Position'] = position
        QB_values_dict['AverageDraftPosition'] = averagedraftposition
        QB_values_dict['AverageDraftPositionPPR'] =averagedraftpositionppr
        QB_values_dict['ByeWeek'] = byeweek
        QB_values_dict['LastSeasonFantasyPoints'] = lastseasonfantasypoints
        QB_values_dict['ProjectedFantasyPoints'] = projectedfantasypoints
        QB_Data_values.append(QB_values_dict)
    print(jsonify(QB_Data_values))
    return jsonify (QB_Data_values)  

@app.route("/api/v1.0/RB")
def RB_Data(): 

    session = Session(engine)

    """Return a list of all columns from the RB table from the database""" 
    def_query_results = session.query(RB.c.Name, RB.c.Team, RB.c.Position, RB.c.AverageDraftPosition, RB.c.AverageDraftPositionPPR,RB.c.ByeWeek, RB.c.LastSeasonFantasyPoints,RB.c.ProjectedFantasyPoints).all()

    session.close()  
    
    RB_Data_values = []
    for name, team, position,averagedraftposition,averagedraftpositionppr, byeweek, lastseasonfantasypoints, projectedfantasypoints in def_query_results:
        RB_values_dict = {}
        RB_values_dict['Name'] = name
        RB_values_dict['Team'] = team
        RB_values_dict['Position'] = position
        RB_values_dict['AverageDraftPosition'] = averagedraftposition
        RB_values_dict['AverageDraftPositionPPR'] =averagedraftpositionppr
        RB_values_dict['ByeWeek'] = byeweek
        RB_values_dict['LastSeasonFantasyPoints'] = lastseasonfantasypoints
        RB_values_dict['ProjectedFantasyPoints'] = projectedfantasypoints
        RB_Data_values.append(RB_values_dict)
    return jsonify (RB_Data_values)  

@app.route("/api/v1.0/WR")
def WR_Data(): 

    session = Session(engine)

    """Return a list of all columns from the WR table from the database""" 

   
    def_query_results = session.query(WR.c.Name, WR.c.Team, WR.c.Position, WR.c.AverageDraftPosition, WR.c.AverageDraftPositionPPR,WR.c.ByeWeek, WR.c.LastSeasonFantasyPoints,WR.c.ProjectedFantasyPoints).all()

    session.close()  
    
    WR_Data_values = []
    for name, team, position,averagedraftposition,averagedraftpositionppr, byeweek, lastseasonfantasypoints, projectedfantasypoints in def_query_results:
        WR_values_dict = {}
        WR_values_dict['Name'] = name
        WR_values_dict['Team'] = team
        WR_values_dict['Position'] = position
        WR_values_dict['AverageDraftPosition'] = averagedraftposition
        WR_values_dict['AverageDraftPositionPPR'] =averagedraftpositionppr
        WR_values_dict['ByeWeek'] = byeweek
        WR_values_dict['LastSeasonFantasyPoints'] = lastseasonfantasypoints
        WR_values_dict['ProjectedFantasyPoints'] = projectedfantasypoints
        WR_Data_values.append(WR_values_dict)
    return jsonify (WR_Data_values)  

@app.route("/api/v1.0/TE")
def TE_Data(): 

    session = Session(engine)

    """Return a list of all columns from the TE table from the database""" 

    def_query_results = session.query(TE.c.Name, TE.c.Team, TE.c.Position, TE.c.AverageDraftPosition, TE.c.AverageDraftPositionPPR,TE.c.ByeWeek, TE.c.LastSeasonFantasyPoints,TE.c.ProjectedFantasyPoints).all()

    session.close()  
    
    TE_Data_values = []
    for name, team, position,averagedraftposition,averagedraftpositionppr, byeweek, lastseasonfantasypoints, projectedfantasypoints in def_query_results:
        TE_values_dict = {}
        TE_values_dict['Name'] = name
        TE_values_dict['Team'] = team
        TE_values_dict['Position'] = position
        TE_values_dict['AverageDraftPosition'] = averagedraftposition
        TE_values_dict['AverageDraftPositionPPR'] =averagedraftpositionppr
        TE_values_dict['ByeWeek'] = byeweek
        TE_values_dict['LastSeasonFantasyPoints'] = lastseasonfantasypoints
        TE_values_dict['ProjectedFantasyPoints'] = projectedfantasypoints
        TE_Data_values.append(TE_values_dict)
    return jsonify (TE_Data_values)  

@app.route("/api/v1.0/Highlight")
def Highlight_Data(): 

    session = Session(engine)

    """Return a list of all columns from the TE table from the database""" 

    def_query_results = session.query( func.min(QB.c.AverageDraftPosition), QB.c.Name, QB.c.Team, QB.c.Position, QB.c.AverageDraftPosition, QB.c.AverageDraftPositionPPR,QB.c.ByeWeek, QB.c.LastSeasonFantasyPoints,QB.c.ProjectedFantasyPoints).all()

    session.close()  
    
    TE_Data_values = []
    for name, team, position,averagedraftposition,averagedraftpositionppr, byeweek, lastseasonfantasypoints, projectedfantasypoints in def_query_results:
        TE_values_dict = {}
        TE_values_dict['Name'] = name
        TE_values_dict['Team'] = team
        TE_values_dict['Position'] = position
        TE_values_dict['AverageDraftPosition'] = averagedraftposition
        TE_values_dict['AverageDraftPositionPPR'] =averagedraftpositionppr
        TE_values_dict['ByeWeek'] = byeweek
        TE_values_dict['LastSeasonFantasyPoints'] = lastseasonfantasypoints
        TE_values_dict['ProjectedFantasyPoints'] = projectedfantasypoints
        TE_Data_values.append(TE_values_dict)
    return jsonify (TE_Data_values) 


if __name__ == '__main__':
    app.run(debug=True) 
