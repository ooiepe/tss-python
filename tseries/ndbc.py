# EPE Time Series Service
# by Sage Lichtenwalner
#
#  NDBC Data Access Library

from datetime import datetime,time,timedelta
import numpy as np

parameters={ # Format - EPE-Common:NDBC-DODS
  'air_pressure':'air_pressure', 
  'air_temperature':'air_temperature', 
  'depth':'water_level',
  'water_temperature':'sea_surface_temperature', 
  'significant_wave_height':'wave_height', 
  'peak_wave_period':'dominant_wpd', 
  'mean_wave_period':'average_wpd', 
  'wave_to_direction':'mean_wave_dir', 
  'wind_from_direction':'wind_dir', 
  'wind_speed':'wind_spd', 
  'wind_gust':'gust', 
  'dew_point_temperature':'dewpt_temperature', 
  'visibility':'visibility'
}


def station_list():
  url = 'http://dods.ndbc.noaa.gov/thredds/catalog/data/stdmet/catalog.xml'
  #url = 'http://dods.ndbc.noaa.gov/thredds/catalog/data/ocean/catalog.xml' #Ocean Data
  from xml.dom import minidom
  import urllib2
  usock = urllib2.urlopen(url)
  xmldoc = minidom.parse(usock)
  usock.close()
  stations=[]
  stations_xml = xmldoc.getElementsByTagName('catalogRef')
  #stations_xml = stations_xml[0:20]
  for station_xml in stations_xml:
      stitle = station_xml.getAttribute('xlink:title')
      stations.append(stitle)
      #print stitle
  return stations


def station_info(station_id):
  from pydap.client import open_url
  url1 = 'http://dods.ndbc.noaa.gov/thredds/dodsC/data/stdmet/'+station_id+'/'+station_id+'h9999.nc'
  #url1 = 'http://dods.ndbc.noaa.gov/thredds/dodsC/data/ocean/'+station_id+'/'+station_id+'o9999.nc' #Ocean Dta
  url2 = 'http://dods.ndbc.noaa.gov/thredds/dodsC/data/stdmet/'+station_id+'/'+station_id+'.ncml'
  #url2=''
  try:
    dataset = open_url(url1)
  except:
    try:
      dataset = open_url(url2)
    except:
      print 'OPENDAP url not found: ' + station_id  
      return False
  return station_info_details(station_id,dataset)      


def station_info_details(station_id,dataset):
  station = {
    'network_name':'ndbc',
    'name':station_id,
    'description':dataset.attributes['NC_GLOBAL']['comment'],
    'latitude':dataset.latitude[0][0],
    'longitude':dataset.longitude[0][0],
    'start_time':dataset.time[0][0],
    'end_time':dataset.time[-1][0],
    'start_time2':datetime.utcfromtimestamp(dataset.time[0][0]).strftime("%Y-%m-%d %H:%M:%S"), #.isoformat(),
    'end_time2':datetime.utcfromtimestamp(dataset.time[-1][0]).strftime("%Y-%m-%d %H:%M:%S"),
    'info_url':'http://www.ndbc.noaa.gov/station_page.php?station='+station_id,
    'image_url':'http://www.ndbc.noaa.gov/images/stations/'+station_id+'.jpg',
    'active': 1 if datetime.utcfromtimestamp(dataset.time[-1][0]) >= datetime.now()-timedelta(30) else 0
  }
  return station


def station_data(station_id,param,option='realtime'):
  from pydap.client import open_url
  if option=='realtime':
    url = 'http://dods.ndbc.noaa.gov/thredds/dodsC/data/stdmet/'+station_id+'/'+station_id+'h9999.nc'
  elif option=='archive':
    url = 'http://dods.ndbc.noaa.gov/thredds/dodsC/data/stdmet/'+station_id+'/'+station_id+'.ncml'
  try:
    dataset = open_url(url)
  except:
    print 'OPENDAP url not found: ' + station_id  
    return False
  else:
    t = dataset.time[:,0,0]  #.asType('datetime64[s]')
    t2=[]
    t2[:] = [convert_date(x) for x in t]
    t2 = np.array(t2)
    y = dataset[parameters[param]].array[:,0,0][:,0,0]  #y = y[:,0,0]; 
    # Remove bad points   
    fillvalue = dataset[parameters[param]].attributes['_FillValue']
    t2_clean = t2[y!=fillvalue]
    y_clean = y[y!=fillvalue]
    return {'dtime':t2_clean,'value':y_clean}  


def convert_date(epoch):
  return (datetime(1970,1,1)+timedelta(0,float(epoch))).strftime("%Y-%m-%d %H:%M:%S")

