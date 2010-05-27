#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb
import pymongo
import re
import sys
from urllib import FancyURLopener

class MyOpener(FancyURLopener):
  version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

if 'mongo' not in sys.argv  and 'mysql' not in sys.argv:
  print 'Please provide database to which import locations (mongo or mysql)'
  sys.exit()

count = 0
db = pymongo.Connection().geo
mysql = MySQLdb.connect(host = 'localhost', user = 'devel',  passwd = 'devel', db = 'geo').cursor()
for i in range(65, 91):
  html = MyOpener().open('http://pl.wikipedia.org/wiki/Wikipedia:Skarbnica_Wikipedii/Po%C5%82o%C5%BCenie_miejscowo%C5%9Bci/' + chr(i)).read()
  regexp = re.compile("<li>(.*?)(\d+)°(\d+)'N (\d+)°(\d+)'E", re.M)
  search = regexp.findall(html)
  if search:
    for location in search:
      doc = {
        'city': location[0].rstrip(': '),
        'loc' : {
          'lat' : float(location[1] + '.' + location[2]),
          'long': float(location[3] + '.' + location[4]),
        }
      }
      if '<a href' in doc['city']:
        replace = re.compile('<a href.*>(.+?)</a>')
        doc['city'] = replace.sub('\\1', doc['city'])
      count += 1
      if 'mongo' in sys.argv:
        db.locations.insert(doc)
      elif 'mysql' in sys.argv:
        mysql.execute("INSERT INTO locations (name, lat, `long`) VALUES ('%s', %s, %s)" % (doc['city'].replace("'", "\\'"), doc['loc']['lat'], doc['loc']['long']))
print 'Got %d locations' % count
