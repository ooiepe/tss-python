#!/usr/bin/python
#
# EPE Time Series Service
#   by Sage Lichtenwalner
# Installation Scripts

import tseries
import argparse

# Command Line Arguments
parser = argparse.ArgumentParser(description='EPE Time Series Service - Installation Scripts')
parser.add_argument('option',
  choices=['database', 'networks', 'parameters'],
  help='Specify an installation option')
args = parser.parse_args()

# Main Control Loop
if args.option=="database":
  ts = tseries.Database()
  ts.install_database()
  ts.close()
elif args.option=="networks":
  ts = tseries.Database()
  ts.load_networks()
  ts.close()
elif args.option=="parameters":
  ts = tseries.Database()
  ts.load_parameters()
  ts.close()
