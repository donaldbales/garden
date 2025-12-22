#!/usr/local/opt/python@3.10/libexec/bin/python
# -*- coding: utf-8 -*-
#
# sunrise_sunset_data.py - Ecospec Instrumenation Package Main Program
# Copyright (C) 2024  Donald J. Bales
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# Last updated by Don Bales on 2025-01-20

import datetime
import ephem
import os
import sys
import time

class SunriseSunsetData:
  def __init__(self):
    log("SunriseSunsetData.__init__()...")
    self.sunrise = None
    self.sunset  = None

  def main(self):
    log("SunriseSunsetData.main()...")
    dt = datetime.datetime(2024, 1, 1, 0, 0, 1)

    # Ten years
    for i in range(0, 3653):
        td = datetime.timedelta(days=i)
        the_day = dt + td
        self.sunrise_time = self.calculate_sunrise(the_day)
        self.sunset_time  = self.calculate_sunset(the_day)
        the_day_str = str(the_day.strftime('%Y-%m-%d'))
        print(the_day_str + '\t' + self.sunrise_time + '\t' + self.sunset_time)

  def calculate_sunrise(self, the_day):
    log("SunriseSunsetData.calculate_sunrise()...")

    today_datetime = the_day
    today_string   = today_datetime.strftime("%Y%m%d")
    #log 'today_datetime: ' + str(type(today_datetime))
    #log 'today_datetime: ' + str(today_datetime)
    #log 'today_string:   ' + today_string

    #Make an observer
    observer      = ephem.Observer()

    #PyEphem takes and returns only UTC times. 15:00 is noon in observerericton
    #observer_datetime = datetime.datetime(2014,10,7,0,0,0)
    #observer_datetime = datetime.datetime(2014,10,8,5,0,0)
    observer_datetime = the_day.astimezone(datetime.timezone.utc)
    observer.date = observer_datetime
    #log 'observer.date:  ' + str(type(observer.date))
    #log 'observer.date:  ' + str(observer.date)

    #Location of garden
    #34.77866, -111.78143
    observer.lon  = str(-111.78143) #Note that lon should be in string format
    observer.lat  = str(34.77866)      #Note that lat should be in string format

    #Elevation of garden (4090 ft) in meters
    observer.elev = 1247

    #To get U.S. Naval Astronomical Almanac values, use these settings
    observer.pressure= 0
    observer.horizon = '-0:34'

    # Get the sunset time so we can compare it against the current time
    sunset_datetime  = ephem.localtime(observer.next_setting(ephem.Sun())) #Sunset
    sunset_string    = sunset_datetime.strftime("%Y%m%d")
    if sunset_string != today_string:
      sunset_datetime  = ephem.localtime(observer.previous_setting(ephem.Sun())) #Sunset

    #log 'if ' + str(sunset_datetime) + ' < ' + str(ephem.localtime(observer.date)) + ":"
    # If the sun has already set, get the next day's settings
    if ephem.localtime(observer.date) > sunset_datetime:
      today_datetime    = today_datetime + datetime.timedelta(days=1)
      today_string      = today_datetime.strftime("%Y%m%d")
      observer_datetime = observer_datetime + datetime.timedelta(days=1)
      observer.date     = observer_datetime

    sunrise_datetime = ephem.localtime(observer.next_rising(ephem.Sun())) #Sunrise
    sunrise_string   = sunrise_datetime.strftime("%Y%m%d")
    if sunrise_string != today_string:
      sunrise_datetime = ephem.localtime(observer.previous_rising(ephem.Sun())) #Sunrise

    sunset_datetime  = ephem.localtime(observer.next_setting(ephem.Sun())) #Sunset
    sunset_string    = sunset_datetime.strftime("%Y%m%d")
    if sunset_string != today_string:
      sunset_datetime  = ephem.localtime(observer.previous_setting(ephem.Sun())) #Sunset

    #log 'sunrise: ' + str(type(sunrise_datetime))
    #log 'sunset: ' + str(type(sunset_datetime))
    #log "sunrise: " + str(sunrise_datetime)
    #log "sunset:  " + str(sunset_datetime)   

    log("Sunrise: " + str(sunrise_datetime.strftime('%Y-%m-%dT%H:%M:%S')))
    #return time.mktime(time.strptime(sunrise_datetime.strftime('%Y-%m-%dT%H:%M:%S'), '%Y-%m-%dT%H:%M:%S'))
    return str(sunrise_datetime.strftime('%Y-%m-%d %H:%M:%S'))

  def calculate_sunset(self, the_day):
    log("SunriseSunsetData.calculate_sunset()...")

    today_datetime = the_day
    today_string   = today_datetime.strftime("%Y%m%d")
    #log 'today_datetime: ' + str(type(today_datetime))
    #log 'today_datetime: ' + str(today_datetime)
    #log 'today_string:   ' + today_string

    #Make an observer
    observer      = ephem.Observer()

    #PyEphem takes and returns only UTC times. 15:00 is noon in observerericton
    #observer_datetime = datetime.datetime(2014,10,7,0,0,0)
    #observer_datetime = datetime.datetime(2014,10,8,5,0,0)
    observer_datetime = the_day.astimezone(datetime.timezone.utc)
    observer.date = observer_datetime
    #log 'observer.date:  ' + str(type(observer.date))
    #log 'observer.date:  ' + str(observer.date)

    #Location of garden
    #34.77866, -111.78143
    observer.lon  = str(-111.78143) #Note that lon should be in string format
    observer.lat  = str(34.77866)      #Note that lat should be in string format

    #Elevation of garden (4090 ft) in meters
    observer.elev = 1247

    #To get U.S. Naval Astronomical Almanac values, use these settings
    observer.pressure= 0
    observer.horizon = '-0:34'

    # Get the sunset time so we can compare it against the current time
    sunset_datetime  = ephem.localtime(observer.next_setting(ephem.Sun())) #Sunset
    sunset_string    = sunset_datetime.strftime("%Y%m%d")
    if sunset_string != today_string:
      sunset_datetime  = ephem.localtime(observer.previous_setting(ephem.Sun())) #Sunset

    #log 'if ' + str(sunset_datetime) + ' < ' + str(ephem.localtime(observer.date)) + ":"
    # If the sun has already set, get the next day's settings
    if ephem.localtime(observer.date) > sunset_datetime:
      today_datetime    = today_datetime + datetime.timedelta(days=1)
      today_string      = today_datetime.strftime("%Y%m%d")
      observer_datetime = observer_datetime + datetime.timedelta(days=1)
      observer.date     = observer_datetime

    sunrise_datetime = ephem.localtime(observer.next_rising(ephem.Sun())) #Sunrise
    sunrise_string   = sunrise_datetime.strftime("%Y%m%d")
    if sunrise_string != today_string:
      sunrise_datetime = ephem.localtime(observer.previous_rising(ephem.Sun())) #Sunrise

    sunset_datetime  = ephem.localtime(observer.next_setting(ephem.Sun())) #Sunset
    sunset_string    = sunset_datetime.strftime("%Y%m%d")
    if sunset_string != today_string:
      sunset_datetime  = ephem.localtime(observer.previous_setting(ephem.Sun())) #Sunset

    #log 'sunrise: ' + str(type(sunrise_datetime))
    #log 'sunset: ' + str(type(sunset_datetime))
    #log "sunrise: " + str(sunrise_datetime)
    #log "sunset:  " + str(sunset_datetime)   

    log("Sunset:  " + str(sunset_datetime.strftime('%Y-%m-%dT%H:%M:%S')))
    #return time.mktime(time.strptime(sunset_datetime.strftime('%Y-%m-%dT%H:%M:%S'), '%Y-%m-%dT%H:%M:%S'))
    return str(sunset_datetime.strftime('%Y-%m-%d %H:%M:%S'))

def log(message):
  formatted = str(datetime.datetime.today()) + " sunrise_sunset_data: " + str(message) 
  logfile = open('./sunrise_sunset_data.log' ,'a')
  logfile.write(formatted + "\n")
  logfile.flush()
  logfile.close()
  #print(formatted)


if __name__ == '__main__':
  program = SunriseSunsetData()
  program.main()
