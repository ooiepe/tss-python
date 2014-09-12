# EPE Time-Series Service - Python Library

The EPE Time-Series Service provides an easy way to access station information and time-series data from a number of popular oceanographic web services through a common web API.  It was developed to support the educational visualization tools of the Ocean Observatories Initiative (OOI) [Ocean Education Portal](http://education.oceanobservatories.org).  

This library provides the backend functions necessary to setup and populate the time-series database.  The source code for the web API is available at https://github.com/ooiepe/tss-php

## Installation

1. Make sure you have the following Python libraries: MySQLdb, numpy, pydap
4. Copy `tseries/config-default.py` to `tseries/config.py` and add your database info
2. Install the database: 
  `python install.py install`
2. Load the networks and parameter lists into the database: 
  `python install.py networks`
  `python install.py parameters`
3. Add some stations:
  `python load-station.py -n ndbc -s 44025`
4. Ingest some data: 
  `python load-data.py -n ndbc -s 44025 -o archive`

