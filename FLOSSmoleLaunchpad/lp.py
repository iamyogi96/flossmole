# -*- coding: utf-8 -*-
#
#Carter Kozak
#c4kofony@gmail.com
#ckozak@elon.edu
#
#flossmole.org
#

#Launchpad Collector, collects data from launchpad.net and stores it in a database
#Copyright (C) 2010  Carter Kozak

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.


import urllib
import sqlalchemy
import re
import StringIO
import sys
from sqlalchemy import *
import ConfigParser
import time
import os

NAMES_MODE = False
DEBUG_MODE = False
CREATE_CONFIG = False



#cmd line args
for arg in sys.argv:
  if arg == '--debug':
    DEBUG_MODE = True
  elif arg == '-d':
    DEBUG_MODE = True
  elif arg == '--names':
    NAMES_MODE = True
  elif arg == '--config':
    CREATE_CONFIG = True

CONFIG_FILE = 'lp.conf'
current_job = ''

#reading config from file
config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)
for section in config.sections():
	if section == 'launchpad':
	    for option in config.options(section):		
		if option == 'db_user':
		    DB_USER = config.get(section,option)
		elif option == 'db_pass':
		    DB_PASS = config.get(section,option)
		elif option == 'db_address':
		    DB_ADDRESS = config.get(section,option)
		elif option == 'projects':
		    PROJECTS = config.get(section,option)
		elif option == 'proj_indexes':
		    PROJ_INDEXES = config.get(section,option)
		elif option == 'jobs':
		    JOBS = config.get(section,option)
		elif option == 'datasource':
		    DATASOURCE = config.get(section,option)
		elif option == 'devs':
		    DEVELOPERS = config.get(section,option)
		elif option == 'developer_projects':
		    DEV_PROJ = config.get(section,option)
		elif option == 'dev_indexes':
		    DEV_INDEXES = config.get(section,option)
		elif option == 'groups':
		    GROUPS = config.get(section,option)
		elif option == 'group_indexes':
		    GROUP_INDEXES = config.get(section,option)
		elif option == 'group_devs':
		    GROUP_DEVS = config.get(section,option)
		elif option == 'group_projects':
		    GROUP_PROJECTS = config.get(section,option)
		    

#database setup
mysql_db = create_engine('mysql://'+DB_USER+':'+DB_PASS+'@'+DB_ADDRESS)
connection = mysql_db.connect()
meta = MetaData()
meta.bind = connection
indexes = Table(PROJ_INDEXES, meta, autoload=True)
jobs = Table(JOBS, meta, autoload=True)
project = Table(PROJECTS, meta, autoload=True)
dev_projects = Table(DEV_PROJ, meta, autoload=True)
devs = Table(DEVELOPERS, meta, autoload=True)
dev_index = Table(DEV_INDEXES, meta, autoload=True)

group = Table(GROUPS, meta, autoload=True)
g_indexes = Table(GROUP_INDEXES, meta, autoload=True)
g_devs = Table(GROUP_DEVS, meta, autoload=True)
g_projects = Table(GROUP_PROJECTS, meta, autoload=True)


def writeConfig():
  
    config = ConfigParser.ConfigParser()
    config.add_section("launchpad")
    config.set("launchpad", "DB_USER", "username")
    config.set("launchpad", "DB_PASS", "pass")
    config.set("launchpad", "DB_ADDRESS", "db_address/dbname")
    config.set("launchpad", "PROJECTS", "projects_table")
    config.set("launchpad", "PROJ_INDEXES", "indexes_table")
    config.set("launchpad", "JOBS", "jobs_table")
    config.set("launchpad", "DEVS", "developer_information")
    config.set("launchpad", "DEVELOPER_PROJECTS", "dev/jobs_table")
    config.set("launchpad", "DEV_INDEXES", "developer_indexes_table")
    config.set("launchpad", "DATASOURCE", 001)
    config.set("launchpad", "GROUPS", "groups_table")
    config.set("launchpad", "GROUP_INDEXES", "group_index_table")
    config.set("launchpad", "GROUP_DEVS", "group_developer_junction")
    config.set("launchpad", "GROUP_PROJECTS", "group_projects_junction")
    confFile = open('lp.conf','w')
    config.write(confFile)

def startJob(job):
    
    try:
      connection.execute(jobs.insert().values(datasource_id=DATASOURCE,jobName = job,startTime=func.now()))
    except sqlalchemy.exc.IntegrityError:
      pass
    
def endJob(job):
    connection.execute(jobs.update().where(jobs.c.jobName == job).where(jobs.c.datasource_id == DATASOURCE).values(endTime=func.now()))

def getCurrentJob():
    current = connection.execute('SELECT jobName FROM '+JOBS +' WHERE datasource_id = '+DATASOURCE+' AND endTime = (SELECT max(endTime) from '+JOBS+' WHERE datasource_id = '+DATASOURCE+');')   
    parsed = current.fetchone()
    current.close()
    try:
      previous = parsed['jobName']
    except TypeError:
      previous = ''
    if previous == '':
      return ''
    elif previous == 'get names':
      return 'move project indexes'
    elif previous == 'move project indexes':
      return 'get html'
    elif previous == 'get html':
      return 'get rdf'
    elif previous == 'get rdf':
      return 'get contrib'
    elif previous == 'get contrib':
      return 'get devs'
    elif previous == 'get devs':
      return 'move dev indexes'
    elif previous == 'move dev indexes':
      return 'get dev pages'
    elif previous == 'get dev pages':
      return 'move group indexes'
    elif previous == 'move group indexes':
      return 'get group pages'
    elif previous == 'get group pages':
      return 'done'

def getNumProjects():
    reader = urllib.urlopen("https://launchpad.net/projects/+all") #should have the correct number of proj, whereas /projects normally has less...
    site = reader.read()
    reader.close    
    return int(site[site.find("<strong class=\"registry-stat\">")+30:site.find("</strong>\n    projects registered in Launchpad.")])

def getNames():
    startJob(current_job)
    
    if DEBUG_MODE:
      batchSize = 1
    else:
      batchSize = 300 #max 300
    
    startIndex = 0
    errorc = 0
    counter = 0
    done = False
    
    
    while not done:
        reader = urllib.urlopen("https://launchpad.net/projects/+all?start="+str(startIndex)+"&batch="+str(batchSize))
        site = reader.read()
        reader.close
        if site.find("&rarr;\n          <strong>"+str(getNumProjects())+"</strong>") > -1:
	  done = True
	if site.find('<h1 class="exception">Timeout error</h1>') == -1:	  
	  sitedit = site[site.find("<table class=\"listing\" id=\"product-listing\">")+44:site.find("</table>\n    <table style=\"width: 100%;\" class=\"lower-batch-nav\">")]
	  g = re.findall('href="/[^~]\S*"',sitedit)
	  for x in g:
	      #
	      counter = counter + 1
	      try:
		  connection.execute(project.insert().values(project_name= x[7:len(x)-1],datasource_id=DATASOURCE,last_updated=func.now()))
	      except sqlalchemy.exc.IntegrityError:
		  errorc = errorc + 1
	  startIndex += batchSize
	  if counter == 0 | DEBUG_MODE:
	    done = True
	counter = 0
        time.sleep(2)
    
    
def getPage(name,num):
    time.sleep(2)
    reader = urllib.urlopen('https://launchpad.net/'+str(name))
    htmlPage = reader.read()
    reader.close
    if htmlPage.find('<h1 class="exception">Timeout error</h1>') > -1:
	del htmlpage
	if num < 31:
	  getPage(name,num+1)
	 
    else:
	try:
	    connection.execute(indexes.update().where(indexes.c.project_name == name).where(indexes.c.datasource_id == DATASOURCE).values(last_updated=func.now(),html = htmlPage))
	except sqlalchemy.exc.IntegrityError:
	    print 'something bad happened getting main page on: ' + name
    
    
    
def getRdf(name,num):
    time.sleep(2)
    reader = urllib.urlopen('https://launchpad.net/'+str(name)+'/+rdf')
    rdfPage = reader.read()
    reader.close
    if rdfPage.find('<h1 class="exception">Timeout error</h1>') > -1:
	del rdfPage
	print 'TIMED OUT: https://launchpad.net/'+str(name)+'/+rdf'
	if num < 31:
	  getRdf(name,num+1)
    else:
	try:
	    connection.execute(indexes.update().where(indexes.c.project_name == name).where(indexes.c.datasource_id == DATASOURCE).values(last_updated=func.now(),rdf = rdfPage))
	except sqlalchemy.exc.IntegrityError:
	    print 'something bad happened getting rdf on: ' + name
    

def getDevPage(name, num):
    time.sleep(2)
    reader = urllib.urlopen('https://launchpad.net/~'+str(name))
    devPage = reader.read()
    reader.close
    if devPage.find('<h1 class="exception">Timeout error</h1>') > -1:
	del devPage
	print 'TIMED OUT: https://launchpad.net/~'+str(name)
	if num < 31:
	  getDevPage(name,num+1)
    else:
	try:
	    connection.execute(dev_index.update().where(dev_index.c.dev_loginname == name).where(dev_index.c.datasource_id == DATASOURCE).values(html = devPage,last_updated=func.now()))
	except sqlalchemy.exc.IntegrityError:
	    print 'something bad happened getting dev page on: ' + name

def getGroupPage(name,num):
    time.sleep(2)
    reader = urllib.urlopen('https://launchpad.net/~'+str(name))
    gPage = reader.read()
    reader.close
    if gPage.find('<h1 class="exception">Timeout error</h1>') > -1:
	del gPage
	print 'TIMED OUT: https://launchpad.net/~'+str(name)
	if num < 31:
	  getGroupPage(name,num+1)
    else:
	try:
	    connection.execute(g_indexes.update().where(g_indexes.c.group_loginname == name).where(g_indexes.c.datasource_id == DATASOURCE).values(html = gPage,last_updated=func.now()))
	except sqlalchemy.exc.IntegrityError:
	    print 'something bad happened getting group page on: ' + name
 
def moveProjectsIndexes():
    startJob(current_job)
    
    result = connection.execute("SELECT project_name FROM "+PROJECTS+" WHERE datasource_id = "+str(DATASOURCE)+";")
    for x in result:
	try:
	    connection.execute(indexes.insert().values(project_name = str(x)[2:len(x)-4],datasource_id=DATASOURCE,last_updated=func.now()))
	except sqlalchemy.exc.IntegrityError:
	    print 'moving indexes failed, probably nothing to wory about'
    endJob(current_job)

def moveDevIndexes():
    startJob(current_job)
    result = connection.execute("SELECT dev_loginname FROM "+DEVELOPERS+" WHERE datasource_id = "+str(DATASOURCE)+";")
    for x in result:
	try:
	    connection.execute(dev_index.insert().values(dev_loginname = str(x)[2:len(x)-4],datasource_id=DATASOURCE,last_updated=func.now()))
	except sqlalchemy.exc.IntegrityError:
	    print 'moving indexes failed, probably nothing to wory about'
    endJob(current_job)

def moveGroupIndexes():
    startJob(current_job)
    result = connection.execute("SELECT group_loginname FROM "+GROUPS+" WHERE datasource_id = "+str(DATASOURCE)+";")
    for x in result:
	try:
	    connection.execute(g_indexes.insert().values(group_loginname = str(x)[2:len(x)-4],datasource_id=DATASOURCE,last_updated=func.now()))
	except sqlalchemy.exc.IntegrityError:
	    print 'moving indexes failed, probably nothing to wory about'
    endJob(current_job)

def populateHtml():
    startJob(current_job)
  
    result = connection.execute("SELECT project_name FROM "+PROJ_INDEXES+" WHERE datasource_id = "+str(DATASOURCE)+" AND html is null;")
    
    for x in result:
        getPage(str(x)[2:len(x)-4],0)
    endJob(current_job)
    
def populateRdf():
    startJob(current_job)
 
    result = connection.execute("SELECT project_name FROM "+PROJ_INDEXES+" WHERE datasource_id = "+str(DATASOURCE)+" AND rdf is null;")
    
    for x in result:
        getRdf(str(x)[2:len(x)-4],0)
    endJob(current_job)

def populateDevs():
    startJob(current_job)
    
    result = connection.execute("SELECT dev_loginname from "+DEV_INDEXES+" WHERE datasource_id = "+str(DATASOURCE)+" AND html is null;")

    for x in result:
      getDevPage(str(x)[2:len(x)-4],0)
    endJob(current_job)
    
def populateGroups():
    startJob(current_job)
    
    result = connection.execute("SELECT group_loginname from "+GROUP_INDEXES+" WHERE datasource_id = "+str(DATASOURCE)+" AND html is null;")

    for x in result:
      getGroupPage(str(x)[2:len(x)-4],0)
    endJob(current_job)


def getDevs():
        
    rdflist = connection.execute("SELECT project_name,rdf from "+PROJ_INDEXES+" where rdf IS NOT NULL AND datasource_id = "+DATASOURCE+";")
    for x in rdflist:
      dev = re.findall('<foaf:Person>\n        <foaf:name>.*?</foaf:name>\n        <foaf:nick>.*?</foaf:nick>',x['rdf'])
      grouplist = re.findall('<foaf:Group>\n        <foaf:name>.*?</foaf:name>\n        <foaf:nick>.*?</foaf:nick>',x['rdf'])
      for y in dev:
	try:
	  connection.execute(devs.insert().values(datasource_id=DATASOURCE,dev_loginname = pullNick(y)[11:len(pullNick(y))-12],last_updated=func.now()))
	except sqlalchemy.exc.IntegrityError:
	  pass
	try:
	  connection.execute(dev_projects.insert().values(datasource_id=DATASOURCE,dev_loginname = pullNick(y)[11:len(pullNick(y))-12],project_name = x['project_name'],last_updated=func.now()))
	except sqlalchemy.exc.IntegrityError:
	  pass
      for k in grouplist:
	try:
	  connection.execute(group.insert().values(datasource_id=DATASOURCE,group_loginname = pullNick(k)[11:len(pullNick(k))-12],last_updated=func.now()))
	except sqlalchemy.exc.IntegrityError:
	  pass
	try:
	  connection.execute(g_projects.insert().values(datasource_id=DATASOURCE,group_loginname = pullNick(k)[11:len(pullNick(k))-12],project_name = x['project_name'],last_updated=func.now()))
	except sqlalchemy.exc.IntegrityError:
	  pass

def getTopContrib():
 startJob(current_job)
 contrib_list = connection.execute("SELECT project_name FROM "+PROJ_INDEXES+" WHERE datasource_id = "+DATASOURCE+" AND contrib_html is null;")
 for x in contrib_list:
   reader = urllib.urlopen('https://launchpad.net/'+x['project_name']+'/+topcontributors')
   try:
     connection.execute(indexes.update().where(indexes.c.project_name == x['project_name']).where(indexes.c.datasource_id==DATASOURCE).values(contrib_html = reader.read()))
   except sqlalchemy.exc.IntegrityError:
     pass
 endJob(current_job)

def getMoreDevs():
  plist = connection.execute("SELECT project_name FROM "+PROJ_INDEXES+" WHERE datasource_id = "+DATASOURCE+" AND contrib_html is not null;")
  for x in plist:
    contrib = connection.execute("SELECT contrib_html FROM "+PROJ_INDEXES+" where datasource_id = "+DATASOURCE+" AND project_name = '"+x['project_name']+"';")
    for y in contrib:
      result = re.findall('href="/~\S*?/\+karma',y['contrib_html'])
      for z in result:
	try:
	  connection.execute(devs.insert().values(dev_loginname = z[8:len(z)-7]),datasource_id = DATASOURCE,last_updated = func.now())
	except sqlalchemy.exc.IntegrityError:
	  pass
	try:
	  connection.execute(dev_index.insert().values(dev_loginname = z[8:len(z)-7],datasource_id = DATASOURCE,last_updated = func.now(),project_name = x['project_name']))
	except sqlalchemy.exc.IntegrityError:
	  pass

def pullNick(nick):
  result = re.findall('<foaf:nick>.*?</foaf:nick>',nick)
  return result.pop() 
  
if CREATE_CONFIG:
  writeConfig()
  sys.exit()

output = open('output.txt','w')
output.write('program running')
output.close()

current_job = getCurrentJob();
if current_job == '':
#    startJob('launchpad_run')
    current_job = 'get names'  
    #BEWARE: a little hacky
    while getNumProjects() > int(str(list(connection.execute("SELECT count(project_name) FROM "+PROJECTS+" WHERE datasource_id = "+str(DATASOURCE)+";")))[2:len(str(list(connection.execute("SELECT count(project_name) FROM "+PROJECTS+" WHERE datasource_id = "+str(DATASOURCE)+";"))))-4]):
      getNames()
      if(DEBUG_MODE):
	break
    if NAMES_MODE:
      endJob(current_job)
      connection.close()
      os.remove('output.txt')
      sys.exit()
    endJob(current_job)
    current_job = 'move project indexes'
if current_job == 'move project indexes':
    moveProjectsIndexes()
    current_job = 'get html'
if current_job == 'get html':
    populateHtml()
    current_job = 'get rdf'
if current_job == 'get rdf':
    populateRdf()
    current_job = 'get contrib'
if current_job == 'get contrib':
    getTopContrib()
    current_job = 'get devs'
if current_job == 'get devs':
    startJob(current_job)
    getDevs()
    getMoreDevs()
    endJob(current_job)
    current_job = 'move dev indexes'
if current_job == 'move dev indexes':
    moveDevIndexes()
    current_job = 'get dev pages'
if current_job == 'get dev pages':
    populateDevs()
    current_job = 'move group indexes'
if current_job == 'move group indexes':
    moveGroupIndexes()
    current_job = 'get group pages'
if current_job == 'get group pages':
    populateGroups()
print 'Done :-)'
os.remove('output.txt')
#endJob('launchpad_run')

connection.close()