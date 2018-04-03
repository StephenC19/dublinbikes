# -*- coding: utf-8 -*-

"""Console script for dublinbikes."""
import sys
sys.path.append('.')
import click
import dublinbikes


@click.command()
def main(args=None):
    """Console script for dublinbikes."""
    
   
    import mysql.connector
    from mysql.connector import errorcode
    
    dubStationInfo = dublinbikes.Database()
    stationList = dublinbikes.stations_list('Dublin.json')
    for i in stationList:
        k = dublinbikes.single_station_info(i)
        dubStationInfo.add_station_info(k)
    dublinbikes.close_db()
    
    
"""
    try:
        
        
        
        #add_info = ("INSERT INTO stations"
         #      "(testrow) "
          #     "VALUES (500)")
        #statInfo = {'number': "500"}
        cursor = cnx.cursor()
       # cursor.execute(add_info, statInfo)
        #query = "INSERT INTO stations (number, name) " \
        #        "VALUES (%s, %s)"
        #thing = ('400', 'Stephen')
        query = "INSERT INTO stations (number, name, latitude, longitude, bikes_available, stands_available) " \
                    "VALUES (%(number)s, %(name)s, %(latitude)s, %(longitude)s, %(bikes)s, %(stands)s) "
        cursor.execute(query, k)
        cursor.execute("SELECT * FROM stations")
        print(cursor.fetchall())
        cnx.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()
 """ 
   
if __name__ == "__main__":
    sys.exit(main())  
