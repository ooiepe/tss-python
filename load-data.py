#!/usr/bin/python
#
# EPE Time Series Service
#   by Sage Lichtenwalner
# Real-time Data Ingestor

import tseries
import argparse
#from datetime import datetime
#from pydap.client import open_url

# Command Line Arguments
parser = argparse.ArgumentParser(description='EPE Time Series Service - Real-time Data Ingestor')
parser.add_argument('-n','--network',
  choices=['ndbc', 'co-ops', 'ooi'],
  help='Network name')
parser.add_argument('-s','--station',
  help='Station id to import')
parser.add_argument('-o','--option',
  choices=['realtime', 'archive'],
  default='realtime',
  help='Type of data to load')
args = parser.parse_args()

# Main Control Loop
if args.network=="ndbc":
  print 'NDBC Real-time Data Ingestor'
  if (args.station != None and args.station != 'all') :
    ts=tseries.Database()
    sensors = ts.find_sensors_by_station(args.network,args.station)
    if sensors:
      #sensors=sensors[0:2]
      for sensor in sensors:
        param = ts.find_parameter_by_id(sensor['parameter_id'])
        print 'Inserting: '+str(sensor['id'])+'-'+param['name']
        data = tseries.ndbc.station_data(args.station,param['name'],args.option)
        if data:
          count = ts.save_data(sensor['id'],data)
          print str(count)+' records inserted'
    else:
      print 'No sensors found for station: ' + args.station

    
#     if station:
#       ts=tseries.Database()
#       station_id = ts.save_station(station)
#       for param in tseries.ndbc.parameters:
#         ts.save_sensor(station_id,param)
#     else:
#       print 'Bad Station: ' + args.station

  elif args.station=="all":
    print 'Processing all'
  else:
    print 'Please specify a valid station or all' 

elif args.network=="co-ops":
  print 'CO-OPS Real-time Data Ingestor'

else:
  print 'Please specify a valid network'

