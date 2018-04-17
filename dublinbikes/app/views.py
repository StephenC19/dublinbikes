"""
Flask file to create web page using information read from a database
"""
from flask import render_template, jsonify, json, g, Flask
from sqlalchemy import create_engine
from app import app
import pandas as pd
import requests
import datetime
from datetime import date


def connect_to_database():
    """Connects to amazon RDS"""
    engine = create_engine("mysql+mysqldb://dbuser:dbpassword1@dublinbikes.cww5dmspazsv.eu-west-1.rds.amazonaws.com/dublinbikes", echo=True)
    return engine

def get_db():
    """Connects to the database if not already connected"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.route("/stations")
def get_all_stations():
    """Querying the database for real time information for all stations. Returns JSON object"""
    engine = get_db()
    sql = "SELECT number, name, latitude, longitude, bikes_available, stands_available from realtime;"
    rows = engine.execute(sql).fetchall()
    return jsonify(stations=[dict(row.items()) for row in rows])

@app.route("/weather")
def query_weather():
    """Queries Open Weather API for current weather information of Dublin City. Parses input and returns dictionary
    of relevant weather information as well current date and time"""
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Dublin&APPID=094f61b4b2da3c4541e43364bab71b0b')
    r = r.json()
    now = datetime.datetime.now()
    weatherInfo= {'main': r['weather'][0]['main'], 
                     'detail': r['weather'][0]['description'], 
                     'temp': r['main']['temp'],
                     'temp_min': r['main']['temp_min'],
                     'temp_max': r['main']['temp_max'],
                     'wind': r['wind']['speed'],
                     'icon': r['weather'][0]['icon'],
                     'date': now.strftime("%d-%m-%Y")}
    return jsonify(weatherInfo=weatherInfo)   

@app.route('/chartDataframe/<int:station_id>/<string:date>')
def chartDataframe(station_id,date):
    """Queries database for historical information of station occupancy, taking in station number and the date as parameters.
    Returns json object of the necessary information to plot info chart"""

    day = "'" + date + "'"
    engine = get_db()
    sql = """select bikes_available, stands_available, time, date from stations where number = {} AND date = {};""".format(station_id,day)
    df = pd.read_sql_query(sql, engine)
    df =df.to_json(orient='index')
    df = jsonify(df)
    return df


@app.route('/', methods=['GET'])
def index():
    """Loads index.html"""
    get_db()
    get_all_stations()
    return render_template("index1.html")

