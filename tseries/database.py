# EPE Time Series Service
# by Sage Lichtenwalner
#
# Time Series Database Class

import MySQLdb
import json
import time

class Database(object):
  """EPE Time Series database processing routines"""
  
  def __init__(self):
    """Class and database initialization"""
    print "-- Initializing tseries.Database class"
    from config import ts_config
    self.ts_config = ts_config
    self.db = MySQLdb.connect(
      host=ts_config['db_host'], 
      user = ts_config['db_user'], 
      passwd = ts_config['db_pass'], 
      db = ts_config['db_dbname'], 
      unix_socket = ts_config['db_socket'])
    self.cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)

  def close(self):
    """Close database connection"""
    self.db.close()

  def install_database(self):
    """Database installation"""
    from db_schema import db_tables
    for name, ddl in db_tables.iteritems():
      print("Creating table {} ".format(name))
      self.cursor.execute(ddl)
    print "Database installation complete"

  #---------------------------
  #  NETWORK FUNCTIONS       

  def find_network(self, name):
    """Find a network by name"""
    sql = """SELECT name FROM networks WHERE name=%s"""
    self.cursor.execute(sql,[name])
    if self.cursor.rowcount > 0:
      res = self.cursor.fetchone()
      return res['name']
    else:
      return False
    
  def save_network(self,data):
    """Save a network to the database"""
    if self.find_network(data['name']) == False:
      sql = """INSERT INTO networks 
        (name,long_name,description,url,created)
        VALUES (%s, %s, %s, %s, %s)"""
      self.cursor.execute(sql, [data['name'],data['long_name'],data['description'],data['url'],time.strftime('%Y-%m-%d %H:%M:%S')] )
      print "Created Network: " +data['name']
    else:
      sql = """UPDATE networks 
        SET name=%s, long_name=%s, description=%s, url=%s, modified=%s
        WHERE name=%s"""
      self.cursor.execute(sql, [ data['name'],data['long_name'],data['description'],data['url'],time.strftime('%Y-%m-%d %H:%M:%S'),data['name'] ] )
      #self.db.escape_string(val)
      print "Updated Network: " +data['name']

  def load_networks(self):
    """Load networks datafile into the database"""
    networks = json.loads(open('data/networks.json').read())  
    for row in networks['networks'] :
      self.save_network(row)

  #---------------------
  #  PARAMETER FUNCTIONS       

  def find_parameter(self, parameter_name):
    """Find a parameter by name"""
    sql = """SELECT id,name FROM parameters WHERE name=%s"""
    self.cursor.execute(sql,[parameter_name])
    if self.cursor.rowcount > 0:
      res = self.cursor.fetchone()
      return res['id']
    else:
      return False            

  def find_parameter_by_id(self, pid):
    """Find a parameter by id"""
    sql = """SELECT id,name FROM parameters WHERE id=%s"""
    self.cursor.execute(sql,[pid])
    if self.cursor.rowcount > 0:
      return self.cursor.fetchone()
    else:
      return False            
                    
  def save_parameter(self,data):
    """Save a parameter to the database"""
    parameter_id = self.find_parameter(data['name'])
    if parameter_id == False:
      sql = """INSERT INTO parameters 
        (name,category,description,units,cf_url,ioos_url,created)
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
      self.cursor.execute(sql, [data['name'],data['category'],data['description'],data['units'],data['cf_url'],data['ioos_url'],time.strftime('%Y-%m-%d %H:%M:%S')] )
      print "Created Parameter: " +data['name']
    else:
      sql = """UPDATE parameters 
        SET name=%s, category=%s, description=%s, units=%s, cf_url=%s, ioos_url=%s, modified=%s
        WHERE id=%s"""
      self.cursor.execute(sql, [data['name'],data['category'],data['description'],data['units'],data['cf_url'],data['ioos_url'],time.strftime('%Y-%m-%d %H:%M:%S'),parameter_id ] )
      #self.db.escape_string(val)
      print "Updated Parameter: " +data['name']

  def load_parameters(self):
    """Load parameters datafile into the database"""
    params = json.loads(open('data/parameters.json').read())  
    for row in params['parameters'] :
      self.save_parameter(row)

  #---------------------
  #  STATION FUNCTIONS       

  def find_station(self, network, station):
    """Find a station by network and name"""
    sql = """SELECT id FROM stations WHERE network_name=%s AND name=%s"""
    self.cursor.execute(sql,[network,station])
    if self.cursor.rowcount > 0:
      res = self.cursor.fetchone()
      return res['id']
    else:
      return False            
  
  def save_station(self,data):
    """Save a station to the database"""
    station_id = self.find_station(data['network_name'],data['name'])
    if  station_id == False:
      sql = """INSERT INTO stations 
        (network_name, name, description, location, start_time, end_time, info_url, image_url, created)  
        VALUES (%s, %s, %s, GeomFromText(%s), %s, %s, %s, %s, %s)"""
      self.cursor.execute(sql, [data['network_name'],
        data['name'],
        data['description'],
        "POINT("+str(data['longitude'])+" "+str(data['latitude'])+")",
        data['start_time2'],
        "9999-01-01" if data['active']==1 else data['end_time2'],  
        data['info_url'],
        data['image_url'],
        time.strftime('%Y-%m-%d %H:%M:%S')] )
      print "Created Station: " +data['network_name'] + "-" + data['name']
      return self.cursor.lastrowid
    else:
      sql = """UPDATE stations 
        SET description=%s, location=GeomFromText(%s), start_time=%s, end_time=%s, info_url=%s, image_url=%s, modified=%s
        WHERE id=%s"""
      self.cursor.execute(sql, [data['description'],
        "POINT("+str(data['longitude'])+" "+str(data['latitude'])+")",
        data['start_time2'],
        "9999-01-01" if data['active']==1 else data['end_time2'],  
        data['info_url'],
        data['image_url'],
        time.strftime('%Y-%m-%d %H:%M:%S'),
        station_id] )
      print "Updated Station: " +data['network_name'] + "-" + data['name']
      return station_id

  #---------------------
  #  SENSOR FUNCTIONS       

  def find_sensor(self, station_id,parameter_id,depth='0'):
    """Find a sensor by station_id,parameter_id and depth (defaults to 0)"""
    sql = """SELECT id FROM sensors WHERE station_id=%s AND parameter_id=%s AND depth=%s"""
    #print sql % (station_id,parameter_id,depth)
    self.cursor.execute(sql,[station_id,parameter_id,depth])
    if self.cursor.rowcount > 0:
      res = self.cursor.fetchone()
      return res['id']
    else:
      return False            

  def save_sensor(self,station_id,parameter_id,depth='0',erddap_url='',active='1'):
    """Save a sensor to the database"""
    sensor_id = self.find_sensor(station_id,parameter_id,depth)
    if  sensor_id == False:
      sql = """INSERT INTO sensors 
        (station_id,parameter_id,depth,erddap_url,active,created)  
        VALUES (%s, %s, %s, %s, %s, %s)"""
      self.cursor.execute(sql, [station_id,parameter_id,depth,erddap_url,active,time.strftime('%Y-%m-%d %H:%M:%S')] )
      print "Created Sensor: " +str(station_id) + "-" + str(parameter_id)
    else:
      sql = """UPDATE sensors 
        SET erddap_url=%s, active=%s, modified=%s
        WHERE id=%s"""
      self.cursor.execute(sql, [ erddap_url, active, time.strftime('%Y-%m-%d %H:%M:%S'),sensor_id] )
      print "Updated Sensor: " +str(station_id) + "-" + str(parameter_id)

  def find_sensors_by_station(self, network, station, active=1):
    """Find the sensors for a specified network/station"""
    station_id = self.find_station(network, station)
    if station_id:
      sql = """SELECT id,parameter_id FROM sensors WHERE station_id=%s"""
      if active:
        sql += """ AND active=1"""
      self.cursor.execute(sql,[station_id])
      if self.cursor.rowcount > 0:
        return self.cursor.fetchall()
      else:
        return False            
    else:
      return False
  

  #---------------------
  #  DATA FUNCTIONS       

  def save_data(self,sensor_id,data):
    """Save data to the database"""
    sql = """INSERT INTO data
        (sensor_id,date_time,value)  
        VALUES (%s, %s, %s)"""
    count = 0
    for x,y in zip(data['dtime'],data['value']):
      #print x,y
      try:
        self.cursor.execute(sql, [sensor_id,x,y] )
        count = count+1
      except:
        pass
        #print 'Insert failed: %s, %s, %s' % (sensor_id,x,y) 
    return count




