# -*- coding: utf-8 -*-

"""Main module."""
import requests
import json
import csv
import pandas
import mysql.connector
from pprint import pprint
from datetime import datetime


#Import static data
staticData = json.load(open('Dublin.json'))
apiKey = "066552409dad0809af4e338d67817a8d931d697d"
dubUrl = "https://api.jcdecaux.com/vls/v1/stations/30?contract=Dublin&apiKey=066552409dad0809af4e338d67817a8d931d697d"

        
def query_API(stationNumber):
    #Gets infromation for single station
    r = requests.get('https://api.jcdecaux.com/vls/v1/stations/' + str(stationNumber) + '?contract=Dublin&apiKey=' + apiKey)
    r = r.json() 
    return r

def query_weather():
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Dublin&APPID=094f61b4b2da3c4541e43364bab71b0b')
    r = r.json()
    weatherInfo= {'main': r['weather'][0]['main'], 
                     'detail': r['weather'][0]['description'], 
                     'temp': r['main']['temp'], 
                     'wind': r['wind']['speed'],
                     'icon': r['weather'][0]['icon']}
    return r
    
def stations_list(fileName):
    #Returns list of station numbers read from the static data
    data = json.load(open(fileName))
    stations = []
    for i in data:
        stations.append(i["number"])
        stations.sort()
    return stations
    
def timestamp_to_ISO(timestamp):
    #Converts a timestamp to a readable time
    moment = datetime.fromtimestamp(timestamp / 1000)
    return moment.time().isoformat()
 
def info_csv():
    stations = stations_list('Dublin.json')
    
    #Save information for all stations in a csv
    #-------------------------------------------
    with open('info.csv', 'w') as csvfile:
        fieldnames = ['number', 'name', 'latitude', 'longitude', 'bikes', 'stands', 'time','date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader() 

        for i in stations:
            g = query_API(i) 
            d = datetime.now().date()
            t = datetime.now().time()
            station_info = {'number': g["number"], 
                    'name': g["name"], 
                    'latitude': g["position"]["lat"], 
                    'longitude': g["position"]["lng"], 
                    'bikes': g["available_bikes"], 
                    'stands': g["available_bike_stands"],
                    'time': t,
                    'date': d}
            writer.writerow(station_info)
    #-------------------------------------------
    
def single_station_info(stationNumber):
    #Creates a dictionary of the a single stations information
    g = query_API(stationNumber) 
    d = datetime.now().date()
    t = datetime.now().time()
    station_info = {'number': g["number"], 
                     'name': g["name"], 
                     'latitude': g["position"]["lat"], 
                     'longitude': g["position"]["lng"], 
                     'bikes': g["available_bikes"], 
                     'stands': g["available_bike_stands"],
                     'time': t,
                     'date': d}
    return station_info
        
        
    
class Database:
    
    def __init__(self):
        #Connect to the database
        from mysql.connector import errorcode
        try:
            dhost="dublinbikes.cww5dmspazsv.eu-west-1.rds.amazonaws.com"
            dport=3306
            dbname="dublinbikes"
            duser="dbuser"
            dpassword="dbpassword1"
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
         
        
    def add_station_info(self, statInfo):
        #Adds data for a single station to the database
        query = "INSERT INTO stations (number, name, latitude, longitude, bikes_available, stands_available, time, date) " \
                    "VALUES (%(number)s, %(name)s, %(latitude)s, %(longitude)s, %(bikes)s, %(stands)s, %(time)s, %(date)s) "
        
        self.cur.execute(query, statInfo)
        self.connection.commit()
        
    
    def realtime_info(self, statInfo):
        #Inserts initial information of a single station into the real time table
        query = "INSERT INTO realtime (number, name, latitude, longitude, bikes_available, stands_available, time) " \
                    "VALUES (%(number)s, %(name)s, %(latitude)s, %(longitude)s, %(bikes)s, %(stands)s, %(time)s) "
        
        self.cur.execute(query, statInfo)
        self.connection.commit()
        
    def update_realtime(self, statInfo, i):
        #Refreshes the information in the realtime table
        query = "UPDATE realtime SET bikes_available = %(bikes)s, stands_available = %(stands)s, time = %(time)s WHERE number = " + str(i) 
        self.cur.execute(query, statInfo)
        self.connection.commit(),

        
    def print_db(self):
        #Prints full realtime database
        self.cur.execute("SELECT * FROM realtime ")
        print(self.cur.fetchall())
        
    def print_station_info(self, j):
        #Prints information for a single station
        self.cur.execute("SELECT latitude, longitude, bikes_available, stands_available FROM realtime WHERE number = " + str(j))
        print(self.cur.fetchall())
        
    def return_info(self, j):
        self.cur.execute("SELECT bikes_available, stands_available FROM realtime WHERE number = " + str(j))
        query = self.cur.fetchall()
        info = {'bikes': query[0][0], 'stands': query[0][1]} 
        return info
    
    def close_db(self):
        self.cur.close()
        self.connection.close()
      
#print(stations_list('Dublin.json'))
#print(query_API(55))
#information()