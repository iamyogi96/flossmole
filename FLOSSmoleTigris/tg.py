import sqlalchemy
from sqlalchemy import *
import urllib
import re
import time
import sys

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
except Exception as e:
  print e
  print 'bad table info in tg.conf'
  sys.exit(1)


def getProjectPage():
  if 0 < len(connection.execute("SELECT html FROM "+PROJECT_LIST_INDEXES+" WHERE datasource_id = "+str(DATASOURCE)+";").fetchall()):
    return

  try:
    project_page = urllib.urlopen('http://www.tigris.org/servlets/ProjectList?type=Projects&&field=ProjectName&matchValue=&matchType=contains&mode=Filtered&pageNum=1&itemsPerPage=500000')
    project_indexes = project_page.read()
    project_page.close()

    connection.execute(proj_list_indexes.insert().values(datasource_id = DATASOURCE, last_updated= func.now(), html = project_indexes))

  except Exception as e:
      print type(e)
      print 'error getting projects list, trying again in 30 sec'
      time.sleep(30)
      getProjectPage()

def getProjectList():
  if 0 < int(connection.execute("SELECT count(*) FROM "+PROJ_INDEXES+" WHERE datasource_id = "+str(DATASOURCE)+";").fetchone()[0]):
    return

  project_page = connection.execute("SELECT html FROM "+PROJECT_LIST_INDEXES+" WHERE datasource_id = "+str(DATASOURCE)+";").fetchone()

  proj_list = re.findall(r'<tr class="[ab]">\s+?<td><a href="http://.+?tigris.org/">(.+?)</a>\s+?</td>\s+?<td>(.*?)</td>\s+?<td>\s+?(.+?)\s+?</td>\s+?</tr>',project_page['html'])

  for each in proj_list:
    for category in re.findall('">(.*?)</a>', each[2]):
      #print category
      try:
        connection.execute(categories.insert().values(datasource_id = DATASOURCE, project = each[0].strip(), category = category.strip(), last_updated = func.now()))
      except Exception as e:
        #print e
        pass
    try:
      connection.execute(projects.insert().values(datasource_id = DATASOURCE, unixname = each[0].strip(), description = each[1].strip(), last_updated = func.now()))
    except Exception as e:
      #print e
      pass
  #print each[0] #name
  #print each[1] #description


def getProjPage(name):
  try:
    temp_page = urllib.urlopen('http://'+name+'.tigris.org/')
    result = temp_page.read()
    temp_page.close()
    return result
  except Exception as e:
    print e
    print 'Something went wrong fetching project page for '+str(name)+'.\nWaiting 30 sec and trying again.'
    time.sleep(30)
    return getProjPage(name)

def getProjectIndexes():
  projects_list = connection.execute("SELECT p.unixname FROM "+PROJECTS+" p LEFT OUTER JOIN "+PROJ_INDEXES+" i ON p.unixname = i.unixname AND p.datasource_id = i.datasource_id WHERE p.datasource_id = "+str(DATASOURCE)+" AND i.html is null;")
  for each in projects_list:
    time.sleep(1)
    try:
      connection.execute(project_indexes.insert().values(datasource_id = DATASOURCE, unixname = each[0], last_updated = func.now(), html = getProjPage(each[0])))
    except Exception as e:
      print e

def getDevPage(name):  
  try:
    temp_page = urllib.urlopen('http://'+name+'.tigris.org/servlets/ProjectMemberList')
    result = temp_page.read()
    temp_page.close()
    return result
  except Exception as e:
    print e
    print 'Something went wrong fetching dev page for '+str(name)+'.\nWaiting 30 sec and trying again.'
    time.sleep(30)
    return getDevPage(name)

def getProjectDevs():
  projects_list = connection.execute("SELECT p.unixname FROM "+PROJECTS+" p LEFT OUTER JOIN "+DEV_INDEXES+" i ON p.unixname = i.project AND p.datasource_id = i.datasource_id WHERE p.datasource_id = "+str(DATASOURCE)+" AND i.html is null;")
  for each in projects_list:
    time.sleep(1)
    try:
      connection.execute(dev_indexes.insert().values(datasource_id = DATASOURCE, last_updated = func.now(), project = each[0], html = getDevPage(each[0])))
    except Exception as e:
      print e

def getDiscPage(name):  
  try:
    temp_page = urllib.urlopen('http://'+name+'.tigris.org/ds/viewForums.do')
    result = temp_page.read()
    temp_page.close()
    return result
  except Exception as e:
    print e
    print 'Something went wrong fetching discuss page for '+str(name)+'.\nWaiting 30 sec and trying again.'
    time.sleep(30)
    return getDiscPage(name)

def getProjectDiscuss():
  projects_list = connection.execute("SELECT p.unixname FROM "+PROJECTS+" p LEFT OUTER JOIN "+DISC_INDEXES+" i ON p.unixname = i.project AND p.datasource_id = i.datasource_id WHERE p.datasource_id = "+str(DATASOURCE)+" AND i.html is null;")
  for each in projects_list:
    time.sleep(1)
    try:
      connection.execute(disc_indexes.insert().values(datasource_id = DATASOURCE, last_updated = func.now(), project = each[0], html = getDiscPage(each[0])))
    except Exception as e:
      print e




getProjectPage()
getProjectList()
getProjectIndexes()
getProjectDevs()
getProjectDiscuss()
