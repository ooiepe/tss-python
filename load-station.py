#!/usr/bin/python
#
# EPE Time Series Service
#   by Sage Lichtenwalner
# Station Loader

import tseries
import argparse
#import csv
#from datetime import datetime

# Command Line Arguments
parser = argparse.ArgumentParser(description='EPE Time Series Service - Station Loader')
parser.add_argument('-n','--network',
  choices=['ndbc', 'co-ops', 'ooi'],
  help='Network name')
parser.add_argument('-s','--station',
  help='Station id to import')
parser.add_argument('-f','--filename',
  help='File of stations to import')
args = parser.parse_args()

# Main Control Loop
if args.network=="ndbc":
  print 'NDBC Station Import'
  if args.station != None:
    station = tseries.ndbc.station_info(args.station)
    if station:
      ts=tseries.Database()
      station_id = ts.save_station(station)
      for param in tseries.ndbc.parameters:
        pid = ts.find_parameter(param)
        ts.save_sensor(station_id,pid)
    else:
      print 'Bad Station: ' + args.station
    



#   stations = tseries.ndbc.station_list()
#   with open(args.filename,'wb') as csvfile:
#     writer = csv.writer(csvfile)
#     for station in stations:
#       sta = tseries.ndbc.station_info(station)
#       if sta:
#         active = 1 if datetime.utcfromtimestamp(sta['end_time']).year >= datetime.now().year else 0
#         if (args.option=='active' and active==1) or (args.option=='all'):
#           writer.writerow([ station,sta['latitude'],sta['longitude'],sta['start_time2'],sta['end_time2'],sta['longname'],active ])

elif args.network=="co-ops":
  print 'CO-OPS Station Import'

else:
  print 'Please specify a valid network'

