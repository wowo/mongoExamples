#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymongo
import re
from urllib import FancyURLopener

class MyOpener(FancyURLopener):
  version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

count = 0
db = pymongo.Connection().geo
for i in range(65, 91):
  html = MyOpener().open('http://pl.wikipedia.org/wiki/Wikipedia:Skarbnica_Wikipedii/Po%C5%82o%C5%BCenie_miejscowo%C5%9Bci/' + chr(i)).read()
  regexp = re.compile("<li>(.*?)(\d+)°(\d+)'N (\d+)°(\d+)'E", re.M)
  search = regexp.findall(html)
  if search:
    for location in search:
      doc = {
        'city': location[0],
        'lat' : location[1] + '.' + location[2],
        'long': location[3] + '.' + location[4],
      }
      if '<a href' in doc['city']:
        replace = re.compile('<a href.*>(.+?)</a>')
        doc['city'] = replace.sub('\\1', doc['city'])
      doc['city'] = doc['city'].rstrip(': ')
      count += 1
      db.locations.insert(doc)
print 'Got %d locations' % count
