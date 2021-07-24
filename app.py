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
Highlights = Base.classes.Highlights_Data
BoxPlot = Base.classes.BoxPlot
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

@app.route("/api/v1.0/Highlights")
def highlights_data():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation (prcp)and date (date) data"""
    
    # Create new variable to store results from query to Measurement table for prcp and date columns
    adp_query_results = session.query(Highlights.Name,Highlights.Team, Highlights.Position,Highlights.AverageDraftPosition,Highlights.AverageDraftPositionPPR, Highlights.ByeWeek,Highlights.LastSeasonFantasyPoints,Highlights.ProjectedFantasyPoints).all()

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
    adp_query_results = session.query(ADP.Name,ADP.Team, ADP.Position,ADP.AverageDraftPosition,ADP.AverageDraftPositionPPR, ADP.ByeWeek,ADP.LastSeasonFantasyPoints,ADP.ProjectedFantasyPoints).all()

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
    projected_query_results = session.query(BoxPlot.NAME,BoxPlot.POSITION,BoxPlot.PROJECTED_POINTS).all()

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
    position_query_results = session.query(Position_Dropdown.Position).all()

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
    def_query_results = session.query(DEF.Name, DEF.Team, DEF.Position, DEF.AverageDraftPosition, DEF.AverageDraftPositionPPR,DEF.ByeWeek, DEF.LastSeasonFantasyPoints,DEF.ProjectedFantasyPoints).all()

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
    def_query_results = session.query(K.Name, K.Team, K.Position, K.AverageDraftPosition, K.AverageDraftPositionPPR,K.ByeWeek, K.LastSeasonFantasyPoints,K.ProjectedFantasyPoints).all()

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
    def_query_results = session.query(QB.Name, QB.Team, QB.Position, QB.AverageDraftPosition, QB.AverageDraftPositionPPR,QB.ByeWeek, QB.LastSeasonFantasyPoints,QB.ProjectedFantasyPoints).all()

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
    def_query_results = session.query(RB.Name, RB.Team, RB.Position, RB.AverageDraftPosition, RB.AverageDraftPositionPPR,RB.ByeWeek, RB.LastSeasonFantasyPoints,RB.ProjectedFantasyPoints).all()

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

   
    def_query_results = session.query(WR.Name, WR.Team, WR.Position, WR.AverageDraftPosition, WR.AverageDraftPositionPPR,WR.ByeWeek, WR.LastSeasonFantasyPoints,WR.ProjectedFantasyPoints).all()

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

    def_query_results = session.query(TE.Name, TE.Team, TE.Position, TE.AverageDraftPosition, TE.AverageDraftPositionPPR,TE.ByeWeek, TE.LastSeasonFantasyPoints,TE.ProjectedFantasyPoints).all()

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

    def_query_results = session.query( func.min(QB.AverageDraftPosition), QB.Name, QB.Team, QB.Position, QB.AverageDraftPosition, QB.AverageDraftPositionPPR,QB.ByeWeek, QB.LastSeasonFantasyPoints,QB.ProjectedFantasyPoints).all()

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
