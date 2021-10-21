#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 10:45:18 2021

@author: drewtammaro
"""


#Locations
loc = [\
  [ 'Anchorage', 'Alaska' ],\
  [ 'Chennai', 'India' ],\
  [ 'Jiangbei', 'China' ],\
  [ 'Kathmandu', 'Nepal' ],\
  [ 'Kothagudem', 'India' ],\
  [ 'Lima', 'Peru' ],\
  [ 'Manhasset', 'New York' ],\
  [ 'Mexico City', 'Mexico' ],\
  [ 'Nanaimo', 'Canada' ],\
  [ 'Peterhead', 'Scotland' ],\
  [ 'Polevskoy', 'Russia' ],\
  [ 'Round Rock', 'Texas' ],\
  [ 'Seoul', 'South Korea' ],\
  [ 'Solihull', 'England' ],\
  [ 'Tel Aviv', 'Israel' ]\
]
    



## Import Modules

import pprint
import requests
import sys
from datetime import datetime
from datetime import timedelta
from datetime import date
import csv

list = []
diff = 0

# Begin writing output CSV
out = open( 'temp.csv', 'w', newline='', encoding='latin' )
writer = csv.writer( out )
writer.writerow( [ 'City','Min 1','Max 1','Min 2','Max 2','Min 3','Max 3','Min 4','Max 4','Min 5','Max 5','Min Avg','Max Avg'] )

for i in loc:
    list.append(i)
    
    # Set sums for averaging
    minsum = 0
    maxsum = 0
    
    # Pull temperatures from Weather Map
    api_key = '0f8b345432ce320014ec4f007eb65c46'
    URL = 'https://api.openweathermap.org/data/2.5/forecast?'
    URL = URL + 'q=' + i[0] + ',' + i[1] + '&appid=' + api_key
    response = requests.get( URL )
    if response.status_code != 200:      # Failure?
        print( 'Error:', response.status_code )
        sys.exit( 0 )
    
    data = response.json()
      #  Get OUR current date
    cur_dt = date.today()
      #  Now, search for the first block that starts tomorrow
    for i in range( 0, len( data[ 'list' ] ) ):
        #  Convert the current block's date text to a datetime object
        dt_str = data[ 'list' ][ i ][ 'dt_txt' ]
        dt_tm = datetime.strptime( dt_str, '%Y-%m-%d %H:%M:%S' )
    
        #  Offset by the timezone offset to get local time, not UTC time
        tz_offset = data[ 'city' ][ 'timezone' ]
        dt_tm = dt_tm + timedelta( seconds=tz_offset )
    
        #  If our day is the same as the block's day, the block is for
        #  today and NOT tomorrow, so keep searching, otherwise break
        #  out of the loop
        #  Print starting blocks
        if cur_dt.day == dt_tm.day:
          print( 'Block', str( i ), 'is still part of today' )
        else:
          startblock = i
          break
    
    # If a full day is left...
    while 40 - startblock > 8:
        
        # Set starting values
        max_temp = 0
        min_temp = 1000
        for j in range(startblock,startblock + 8):
            if response.status_code == 200:      # Success
                data = response.json()
        
                # Pull maximum temp of day, convert Kelvin to Celsius
                printer = pprint.PrettyPrinter( width=80, compact=True )
                temp1 = round(((data[ 'list' ][ j ]['main']['temp_max']) - 273.15),2)
                
                # Pull minimum temp of day, convert Kelvin to Celsius
                temp2 = round(((data[ 'list' ][ j ]['main']['temp_min']) - 273.15),2)
                
                # Set as daily max if greater
                if temp1 != temp2:
                    diff = diff + 1
                if temp1 > max_temp:
                    max_temp = temp1
                else:
                    max_temp = max_temp
                
                # Set as daily min if smaller
                if temp2 < min_temp:
                    min_temp = temp2
                else:
                    min_temp = min_temp
            else:                                # Failure
                print( 'Error:', response.status_code )

        # Add  max/min values to output list/CSV, rounded to two decimal places
        list.append(round(min_temp,2))
        list.append(round(max_temp,2))
        
        # Update totals for averages
        minsum += min_temp
        maxsum += max_temp
        
        # Move to next day and repeat
        startblock = startblock + 8
    
    # Repeat process for last day, will not be full day
    else:
        max_temp = 0
        min_temp = 1000
        for j in range(startblock,startblock + (40 - startblock)):
            if response.status_code == 200:      # Success
                data = response.json()
        
                printer = pprint.PrettyPrinter( width=80, compact=True )
                temp1 = round(((data[ 'list' ][ j ]['main']['temp_max']) - 273.15),2)
                temp2 = round(((data[ 'list' ][ j ]['main']['temp_min']) - 273.15),2)

                if temp1 != temp2:
                    
                    diff = diff + 1
                if temp1 > max_temp:
                    max_temp = temp1
                else:
                    max_temp = max_temp
                    
                if temp2 < min_temp:
                    min_temp = temp2
                else:
                    min_temp = min_temp
            else:                                # Failure
                print( 'Error:', response.status_code )
        
        list.append(round(min_temp,2)) 
        list.append(round(max_temp,2))
        minsum += min_temp
        maxsum += max_temp
    
    # Add five-day averages for min, max to output list
    list.append(round((minsum / 5),2))
    list.append(round((maxsum / 5),2))
   
    # Write output list to CSV
    writer.writerow([list[0][0]+', ' + list[0][1], format(list[1],".2f"), format(list[2],".2f"), format(list[3],".2f"), format(list[4],".2f"), format(list[5],".2f"), format(list[6],".2f"), format(list[7],".2f"), format(list[8],".2f"), format(list[9],".2f"), format(list[10],".2f"), format(list[11],".2f"), format(list[12],".2f")])
    
    # Clear output list for next city
    list.clear()
print(diff)
print(list)


out.close()  








