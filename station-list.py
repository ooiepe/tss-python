#!/usr/bin/python
#
# EPE Time Series Service
#   by Sage Lichtenwalner
# Station Listing Export

import tseries
import argparse
import csv
#from datetime import datetime

# Command Line Arguments
parser = argparse.ArgumentParser(description='EPE Time Series Service - Station Listing Export')
parser.add_argument('-n','--network',
  choices=['ndbc', 'co-ops', 'ooi'],
  help='Network name')
parser.add_argument('-o','--option',
  choices=['active', 'all', 'simple'],
  default='active',
  help='Specify whether you want to output all stations or only active stations')
parser.add_argument('-f','--filename',
  default='stations.csv',
  help='Filename to export CSV data to')
args = parser.parse_args()

# Main Control Loop
if args.network=="ndbc":
  print 'NDBC Station Export'
  stations = tseries.ndbc.station_list()
  with open(args.filename,'wb') as csvfile:
    writer = csv.writer(csvfile)      
    for station in stations:
      if (args.option=='simple'):
        writer.writerow([ 'ndbc', station ])
      else:
        sta = tseries.ndbc.station_info(station)
        if sta:
          #active = 1 if datetime.utcfromtimestamp(sta['end_time']).year >= datetime.now().year else 0
          if (args.option=='active' and sta['active']==1) or (args.option=='all'):
            writer.writerow([ 'ndbc', station, sta['latitude'], sta['longitude'], sta['start_time2'], 
              sta['end_time2'], sta['description'], sta['active'] ])

elif args.network=="co-ops":
  print 'Co-ops export'

else:
  print 'Please specify a valid network'

