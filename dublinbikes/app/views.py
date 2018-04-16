from flask import render_template, jsonify, json, g, Flask
from sqlalchemy import create_engine
from app import app
import os
import json
import sys
import re
import sqlite3
from _sqlite3 import Row
import pandas as pd
import requests
import datetime
from datetime import date

#app = Flask(__name__, static_url_path='')
#app.config.from_object('config')
#app.config['SQL_ALCHEMY_URI'] = 'mysql://{dbuser}:{dbpassword1}@{dublinbikes.cww5dmspazsv.eu-west-1.rds.amazonaws.com}/{dublinbikes}'
#db = SQLAlchemy(application)


def connect_to_database():
    engine = create_engine("mysql+mysqldb://dbuser:dbpassword1@dublinbikes.cww5dmspazsv.eu-west-1.rds.amazonaws.com/dublinbikes", echo=True)
    return engine

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.route("/stations")
def get_all_stations():
    engine = get_db()
    #stations = []
    sql = "SELECT number, name, latitude, longitude, bikes_available, stands_available from realtime;"
    #rows = engine.execute("SELECT number, name, latitude, longitude from realtime;")
    rows = engine.execute(sql).fetchall()
    print("found {} stations", len(rows))
    #for row in rows:
        #stations.append(dict(row))
    return jsonify(stations=[dict(row.items()) for row in rows])

@app.route("/weather")
def query_weather():
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Dublin&APPID=094f61b4b2da3c4541e43364bab71b0b')
    r = r.json()
    now = datetime.datetime.now()
    day = datetime.datetime.today().weekday()
    weatherInfo= {'main': r['weather'][0]['main'], 
                     'detail': r['weather'][0]['description'], 
                     'temp': r['main']['temp'],
                     'temp_min': r['main']['temp_min'],
                     'temp_max': r['main']['temp_max'],
                     'wind': r['wind']['speed'],
                     'icon': r['weather'][0]['icon'],
                     'date': now.strftime("%d-%m-%Y"),
                     'day':day}
    print(weatherInfo)
    return jsonify(weatherInfo=weatherInfo)

@app.route("/available/<int:station_id>")
def get_stations(station_id):
    engine = get_db()
    data = []
    rows = engine.execute("SELECT bikes_available FROM realtime WHERE number = {};".format(station_id))

    for row in rows:
        data.append(dict(row))
        
    return jsonify(available=data)
        

@app.route('/dataframe/<int:station_id>/<string:dat>')
def dataframe(station_id,dat):
    day = "'" + dat + "'"
    engine = get_db()
    sql = """select bikes_available, stands_available, time, date from stations where number = {} AND date = {};""".format(station_id,day)
    df = pd.read_sql_query(sql, engine)
    df =df.to_json(orient='index')
    df = jsonify(df)
    return df

@app.route('/historicalInfo/<int:station_id>/<string:dat>')
def historicalInfo(station_id,dat):
    day = "'" + dat + "'" 
    engine = get_db()
    sql = """select bikes_available, stands_available, time, date from stations where number = {} AND date = {};""".format(station_id,day)
    df = pd.read_sql_query(sql, engine)
    df =df.to_json(orient='index')
    df = jsonify(df)
    return df


@app.route('/', methods=['GET'])
def index():
    get_db()
    get_all_stations()
  
    returnDict = {}
    returnDict['user'] = 'User123'
    returnDict['title'] = 'Dublin Bikes'
    return render_template("index1.html", **returnDict)
    # number=number, address=address, lat=lat, long=long

