# EPE Time Series Service 
#   by Sage Lichtenwalner
# Database Schema
#
# Revised 9/10/2014

db_tables = {}

db_tables['networks'] = (
  """CREATE TABLE IF NOT EXISTS `networks` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(10) NOT NULL,
    `long_name` text NOT NULL,
    `description` text NOT NULL,
    `url` tinytext NOT NULL,
    `created` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    `modified` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    PRIMARY KEY (`id`),
    UNIQUE KEY `name` (`name`)
  ) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1""")

db_tables['parameters'] = (
  """CREATE TABLE IF NOT EXISTS `parameters` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,
    `category` varchar(100) NOT NULL,
    `description` text NOT NULL,
    `units` varchar(20) NOT NULL,
    `cf_url` tinytext NOT NULL,
    `ioos_url` tinytext NOT NULL,
    `created` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    `modified` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    PRIMARY KEY (`id`),
    UNIQUE KEY `name` (`name`)
  ) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1""")

db_tables['stations'] = (
  """CREATE TABLE IF NOT EXISTS `stations` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `network_name` varchar(10) NOT NULL,
    `name` varchar(25) NOT NULL,
    `description` text NOT NULL,
    `location` point NOT NULL,
    `start_time` datetime DEFAULT NULL,
    `end_time` datetime DEFAULT NULL,
    `info_url` varchar(255) NOT NULL,
    `image_url` varchar(255) NOT NULL,
    `created` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    `modified` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    PRIMARY KEY (`id`),
    UNIQUE KEY `unique-station` (`network_name`,`name`)
  ) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1""")
  
db_tables['sensors'] = (
  """CREATE TABLE IF NOT EXISTS `sensors` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `station_id` int(11) NOT NULL,
    `parameter_id` int(11) NOT NULL,
    `depth` decimal(6,2) NOT NULL,
    `erddap_url` varchar(255) NOT NULL,
    `active` tinyint(4) NOT NULL,
    `created` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    `modified` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    PRIMARY KEY (`id`),
    UNIQUE KEY `unique-sensor` (`station_id`,`parameter_id`,`depth`)
  ) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1""")

db_tables['data'] = (
  """CREATE TABLE IF NOT EXISTS `data` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `sensor_id` int(11) NOT NULL,
    `date_time` datetime NOT NULL,
    `value` double NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `sensor-date` (`sensor_id`,`date_time`)
  ) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1""")

