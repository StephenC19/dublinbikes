from flask import render_template, jsonify, json, g, Flask
from sqlalchemy import create_engine
from app import app
import os
import json
import sys
import re
import sqlite3
from _sqlite3 import Row

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

#@app.teardown_appcontext
#def close_connection(exception):
    #db = getattr(g, '_database', None)
    #if db is not None:
        #db.close()
#/
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


@app.route("/available/<int:station_id>")
def get_stations(station_id):
    engine = get_db()
    data = []
    
    rows = engine.execute("SELECT bikes_available FROM realtime WHERE number = {};".format(station_id))

    for row in rows:
        data.append(dict(row))
        
    return jsonify(available=data)
        
@app.route('/station/<int:station_id>')
def station(station_id):
    return 'Retrieving station info for station number: {}'.format(station_id)


@app.route('/', methods=['GET'])
def index():
    get_db()
    get_all_stations()
    #get_stations()
    
    #with app.open_resource('Dublin.json', 'r') as f:
        #mydata = json.load(f)
        #location = []
        #name = []
        #number = []
        #address = []
        #lat = []
        #long = []
        #j=0
        #for i in mydata:
        #    number.append(mydata[j]['number'])
        #    name.append(mydata[j]['name'])
        #    address.append(mydata[j]['address'])
        #   lat.append(mydata[j]['latitude'])
        #    long.append(mydata[j]['longitude'])

        #    j+=1
        #address = json.dumps(address).replace("\'", "\\'")
        #name = json.dumps(name).replace("\'", "\\'")   
        #number = json.dumps(number)
        #lat = json.dumps(lat)
        #long = json.dumps(long)    
    returnDict = {}
    returnDict['user'] = 'User123'
    returnDict['title'] = 'Dublin Bikes'
    return render_template("index1.html", **returnDict)
    # number=number, address=address, lat=lat, long=long

