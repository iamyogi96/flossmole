import sqlalchemy
from sqlalchemy import *
import urllib
import re
import time
import sys 
from datetime import datetime
from dateutil.parser import parse
import ConfigParser

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
  PROJ_DEV = config.get('tigris','proj_dev')
  DEV_ROLES = config.get('tigris','dev_roles')
  DEV_INDEXES = config.get('tigris','dev_indexes')
  DATASOURCE = config.getint('tigris','datasource')
  DISCUSS = config.get('tigris','discuss')
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
  proj_dev = Table(PROJ_DEV, meta, autoload=True)
  dev_roles = Table(DEV_ROLES, meta, autoload=True)
  dev_indexes = Table(DEV_INDEXES, meta, autoload=True)
  disc_indexes = Table(DISC_INDEXES, meta, autoload=True)
  discuss = Table(DISCUSS, meta, autoload=True)
except Exception as e:
  print e
  print 'bad table info in tg.conf'
  sys.exit(1)

def parseProject(name):
  proj = connection.execute('SELECT html FROM '+PROJ_INDEXES+' WHERE datasource_id = '+str(DATASOURCE)+' AND unixname = "'+name+'";')
  html = proj.fetchone()[0]
  proj.close()
  #summary = re.search('<tr>\s+<th>Summary</th>\s+<td>(.*?)</td>\s+</tr>',html)
  #print summary.group(1)
  #categories = re.search('<tr>\s+<th>\s+Categor\S+\s+</th>\s+<td>\s+(.*?)\s+</td>\s+</tr>',html)
  #if categories:
    #hat = re.findall('org/">(.*?)</a>',categories.group(1))
    #for cat in hat:
      #pass
      #try:
      #  connection.execute(categories.insert().values(datasource_id = DATASOURCE))
      #except Exception as e:
      #  print e

  license = re.search('<tr>\s+<th>License</th>\s+<td>\s+.*?">(.*?)</a>\s+</td>\s+</tr>',html)
  if license:
    #print license.group(1)
    try:
      connection.execute(projects.update().where(projects.c.datasource_id==DATASOURCE).where(projects.c.unixname==name).values(last_updated = func.now, license = license.group(1)))
    except Exception as e:
      print e

  #owns = re.search('<tr>\s+<th>Owner[(]s[)]</th>\s+<td>\s+?(.*?)\s+?</td>\s+</tr>',html)
  #if owns:
  #  o = re.findall('">(.*?)</a>',owns.group(1))
  #  for each in o:
  #    #print each
  #    try:
  #      connection.execute(project_owners.insert().values(project = name, datasource_id = DATASOURCE, last_updated = func.now(), owner = each))
  #    except Exception as e:
  #      print e
      


def parseDevs(name):
  proj = connection.execute('SELECT html,project FROM '+DEV_INDEXES+' WHERE datasource_id = '+str(DATASOURCE)+' AND project = "'+name+'";')
  html = proj.fetchone()
  proj.close()
  peoples = re.findall('<tr class="[ab]">\s+<td>\s*(.*?)\s*</td>\s+<td>\s*(.*?)\s*</td>\s+<td>\s+(.*?)\s+</td>\s+</tr>',html[0],re.DOTALL)
  #people = re.findall('<tr class="[ab]">(.*?)</tr>',html,re.DOTALL)
  for each in peoples:
    #print each[0] #username
    #print each[1] #full name
    try:
      connection.execute(people.insert().values(datasource_id = DATASOURCE, username = each[0], full_name = each[1], last_updated = func.now()))
    except Exception as e:
      print e
      print 'problem inserting people'
    for role in each[2].split(','):
      #print role.strip()
      try:
        connection.execute(dev_roles.insert().values(datasource_id = DATASOURCE, last_updated = func.now(), project = html[1], username = each[0], role = role.strip()))
      except Exception as e:
        print e
        print 'problem inserting roles'

def parseLists(name):
  proj = connection.execute('SELECT html,project FROM '+DISC_INDEXES+' WHERE datasource_id = '+str(DATASOURCE)+' AND project = "'+name+'";')
  html = proj.fetchone()
  proj.close()

  lol = re.findall('<tr class="[ab]">\s*(.*?)\s*</tr>',html[0],re.DOTALL) #lol: list of lists
  for l in lol:
    last_updated = None
    last_post = re.search('<span class="nowrap">\s*(\d{4}.*?)\s*</span>',l)
    try:
      last_updated = parse(last_post.group(1))
    except:
      pass
    title = re.search("<a href='viewForumSummary.do[?]dsForumId=(\S+)'>\s+(.*?)\s+</a>",l)
    #print title.group(1)

    desc = re.search('<p class="attrdesc">\s*(.*?)\s*</p>',l,re.DOTALL)
    #print desc.group(1)
    try:
      connection.execute(discuss.insert().values(datasource_id = DATASOURCE, last_updated = func.now(), discussion = title.group(2), description = desc.group(1), last_comment = last_updated, forumid = title.group(1), project = html[1]))
    except Exception as e:
      print e

def parseProjects():
  project_list = connection.execute("SELECT unixname FROM "+PROJ_INDEXES+" WHERE datasource_id = "+str(DATASOURCE)+";")
  for each in project_list:
    #parseProject(each[0])
    #parseDevs(each[0])
    parseLists(each[0])

parseProjects()
