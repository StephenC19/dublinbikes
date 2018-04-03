# -*- coding: utf-8 -*-

"""Main module."""
import requests
import json
import csv
import pandas
import mysql.connector
from pprint import pprint
from datetime import datetime




staticData = json.load(open('Dublin.json'))
apiKey = "066552409dad0809af4e338d67817a8d931d697d"
dubUrl = "https://api.jcdecaux.com/vls/v1/stations/30?contract=Dublin&apiKey=066552409dad0809af4e338d67817a8d931d697d"

        
def query_API(stationNumber):
    r = requests.get('https://api.jcdecaux.com/vls/v1/stations/' + str(stationNumber) + '?contract=Dublin&apiKey=' + apiKey)
    r = r.json() 
    return r

def stations_list(fileName):
    data = json.load(open(fileName))
    stations = []
    for i in data:
        stations.append(i["number"])
        stations.sort()
    return stations

def timestamp_to_ISO(timestamp):
    moment = datetime.fromtimestamp(timestamp / 1000)
    return moment.time().isoformat()
 
def info_csv():
    stations = stations_list('Dublin.json')
    
    #Save information for all stations in a csv
    #-------------------------------------------
    with open('info.csv', 'w') as csvfile:
        fieldnames = ['number', 'name', 'latitude', 'longitude', 'bikes', 'stands']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader() 

        for i in stations:
            g = query_API(i) 
            station_info = {'number': g["number"], 
                    'name': g["name"], 
                    'latitude': g["position"]["lat"], 
                    'longitude': g["position"]["lng"], 
                    'bikes': g["available_bikes"], 
                    'stands': g["available_bike_stands"]}
            writer.writerow(station_info)
    #-------------------------------------------
    
def single_station_info(stationNumber):
    g = query_API(stationNumber) 
    station_info = {'number': g["number"], 
                    'name': g["name"], 
                    'latitude': g["position"]["lat"], 
                    'longitude': g["position"]["lng"], 
                    'bikes': g["available_bikes"], 
                    'stands': g["available_bike_stands"]}
    
    
    return station_info
        
    
class Database:
    

    def __init__(self):
        
        from mysql.connector import errorcode
        try:
            dhost="dublinbikes.cww5dmspazsv.eu-west-1.rds.amazonaws.com"
            dport=3306
            dbname="dublinbikes"
            duser="dbuser"
            dpassword="comp30670"
            cnx = mysql.connector.connect(user = duser, password = dpassword, 
                                      host = dhost, database=dbname)
            self.connection = cnx
            self.cur = cnx.cursor()
            print("connected")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
#             else:
#                 cnx.close()
#             
         
        
    def add_station_info(self, statInfo):
        query = "INSERT INTO stations (number, name, latitude, longitude, bikes_available, stands_available) " \
                    "VALUES (%(number)s, %(name)s, %(latitude)s, %(longitude)s, %(bikes)s, %(stands)s) "
        
        self.cur.execute(query, statInfo)
        self.connection.commit()
        print("info added")
        
        
    def close_db(self):
        self.cur.close()
        self.connection.close()
    def test_thing(self):
        return "thing"
      
#print(stations_list('Dublin.json'))
#print(query_API(55))
#information()