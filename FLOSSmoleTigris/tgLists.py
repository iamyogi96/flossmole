# Carter Kozak
# c4kofony@gmail.com
# ckozak@elon.edu

#collector/parser for Tigris mailing list data

# flossmole.org

# Copyright (C) 2011 Carter Kozak

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sqlalchemy
from sqlalchemy import *
import urllib
import urllib2
import re
import time
import sys 
from datetime import datetime
from dateutil.parser import parse
import ConfigParser
import warnings
warnings.filterwarnings('ignore')

config = ConfigParser.RawConfigParser()
config.read('tg.conf')

try:
  DB_USER = config.get('tigris','user')
  DB_PASS = config.get('tigris','pass')
  DB_ADDRESS = config.get('tigris','address')
  PROJECT_LIST_INDEXES = config.get('tigris','proj_list_indexes')
  PROJ_INDEXES = config.get('tigris','project_indexes')
  PROJECTS = config.get('tigris','projects')
  PROJ_CAT = config.get('tigris','categories')
  DISC_INDEXES = config.get('tigris','disc_indexes')
  PEOPLE = config.get('tigris','people')
  #PROJ_DEV = config.get('tigris','proj_dev')
  DEV_ROLES = config.get('tigris','dev_roles')
  DEV_INDEXES = config.get('tigris','dev_indexes')
  DATASOURCE = config.getint('tigris','datasource')
  DISCUSS = config.get('tigris','discuss')
  MESSAGES = config.get('tigris','messages')
except Exception as e:
  print e
  print 'error reading tg.conf'
  sys.exit(1)

db = create_engine('mysql://'+DB_USER+':'+DB_PASS+'@'+DB_ADDRESS+'?charset=utf8&use_unicode=1')
connection = db.connect()
meta = MetaData()
meta.bind = connection

try:
  proj_list_indexes = Table(PROJECT_LIST_INDEXES, meta, autoload=True)
  project_indexes = Table(PROJ_INDEXES, meta, autoload=True)
  projects = Table(PROJECTS, meta, autoload=True)
  categories = Table(PROJ_CAT, meta, autoload=True)
  people = Table(PEOPLE, meta, autoload=True)
  #proj_dev = Table(PROJ_DEV, meta, autoload=True)
  dev_roles = Table(DEV_ROLES, meta, autoload=True)
  dev_indexes = Table(DEV_INDEXES, meta, autoload=True)
  disc_indexes = Table(DISC_INDEXES, meta, autoload=True)
  discuss = Table(DISCUSS, meta, autoload=True)
  messages = Table(MESSAGES, meta, autoload=True)
except Exception as e:
  print e
  print 'bad table info in tg.conf'
  sys.exit(1)


def downloadList(project, forumid):
  url = 'http://'+str(project)+'.tigris.org/servlets/WebFeed?artifact=messages&dsForumId='+str(forumid)
  #f = urllib.urlopen(url)
  try:
    f = urllib2.urlopen(url)
    mailing_list = f.read()
    f.close()
  
  #posts = re.findall('<item>.*?</item>',mailing_list, re.DOTALL)
    posts = re.findall(r'<item>\s*<title>\s*(.*?)\s*</title>\s*<link>\s*(.*?)\s*</link>\s*<description>\s*(.*?)\s*</description>\s*<pubDate>\s*(.*?)\s*</pubDate>\s*<guid>\s*(.*?)\s*</guid>\s*<dc:creator>\s*(.*?)\s*</dc:creator>\s*<dc:date>\s*(.*?)\s*</dc:date>\s*</item>',mailing_list, re.DOTALL)
    for post in posts:
    #print 'title: '+post[0]
    #print 'link: '+post[1]
    #print 'description: '+post[2]
    #print 'pubDate: '+post[3]
    #print 'guid: '+post[4]
    #print 'creator: '+post[5]
    #print 'date: '+post[6]
      try:
        connection.execute(messages.insert().values(datasource_id = DATASOURCE, title = post[0], link = post[1], description = post[2], pubDate = parse(post[3]), guid = post[4], creator = post[5], postDate = parse(post[6]),postDateStr = post[6], project = project, forumid = forumid))
      except Exception as e:
        pass
  except urllib2.HTTPError, x:
    print 'Ignoring '+str(project)+' : '+str(forumid)+' probably requires login'

def doLists():
  proj_list = connection.execute("SELECT project,forumid FROM "+DISCUSS+" WHERE datasource_id = "+str(DATASOURCE)+";")
  for proj in proj_list:
    downloadList(proj['project'],proj['forumid'])
doLists()
