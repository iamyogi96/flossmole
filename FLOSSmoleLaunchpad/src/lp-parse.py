# -*- coding: utf-8 -*-
#
#Carter Kozak
#c4kofony@gmail.com
#ckozak@elon.edu
#
#flossmole.org
#
#Launchpad Parser, parses data collected from launchpad.net
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


import sqlalchemy
import re
import StringIO
import sys
from sqlalchemy import *
import ConfigParser
#from warnings import filterwarnings
#filterwarnings('ignore')
CONFIG_FILE = 'lp-parse.conf'

config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)
for section in config.sections():
	if section == 'launchpad-parse':
	    for option in config.options(section):		
		if option == 'db_user':
		    DB_USER = config.get(section,option)
		elif option == 'db_pass':
		    DB_PASS = config.get(section,option)
		elif option == 'db_address':
		    DB_ADDRESS = config.get(section,option)
		elif option == 'projects': #probably dont need this
		    PROJECTS = config.get(section,option)
		elif option == 'proj_indexes':
		    PROJ_INDEXES = config.get(section,option)
		elif option == 'datasource':
		    DATASOURCE = config.get(section,option)
		elif option == 'devs':
		    DEVELOPERS = config.get(section,option)
		elif option == 'developer_projects':
		    DEV_PROJ = config.get(section,option)
		elif option == 'project_uses':
		    PROJECT_USES = config.get(section,option)
		elif option == 'project_licenses':
		    PROJECT_LICENSES = config.get(section,option)
		elif option == 'proj_indexes':
		    PROJ_INDEXES = config.get(section,option)
		elif option == 'dev_indexes':
		    DEV_INDEXES = config.get(section,option)
		elif option == 'project_lang':
		    PROJECT_LANGUAGES = config.get(section,option)
		elif option == 'dev_irc':
		    DEVELOPER_IRC = config.get(section,option)
		elif option == 'dev_wiki':
		    DEVELOPER_WIKI = config.get(section,option)
		elif option == 'dev_lang':
		    DEVELOPER_LANG = config.get(section,option)
		elif option == 'group':
		    GROUPS = config.get(section,option)
		elif option == 'group_indexes':
		    GROUP_INDEXES = config.get(section,option)
		    
mysql_db = create_engine('mysql://'+DB_USER+':'+DB_PASS+'@'+DB_ADDRESS)
connection = mysql_db.connect()
meta = MetaData()
meta.bind = connection
indexes = Table(PROJ_INDEXES, meta, autoload=True)
project = Table(PROJECTS, meta, autoload=True)
devs = Table(DEVELOPERS, meta, autoload=True)
#proj_info = Table(PROJECT_INFO, meta, autoload=True)
dev_projects = Table(DEV_PROJ, meta, autoload=True)
uses = Table(PROJECT_USES, meta, autoload=True)
licenses = Table(PROJECT_LICENSES, meta, autoload=True)
dev_index = Table(DEV_INDEXES, meta, autoload=True)
proj_lang = Table(PROJECT_LANGUAGES, meta, autoload=True)
dev_lang = Table(DEVELOPER_LANG, meta, autoload=True)
dev_irc = Table(DEVELOPER_IRC, meta, autoload=True)
dev_wiki = Table(DEVELOPER_WIKI, meta, autoload=True)
group = Table(GROUPS, meta, autoload=True)
g_indexes = Table(GROUP_INDEXES, meta, autoload=True)

def getRdfInfo(rdf):
  
#  name = re.findall('<lp:name>.*?</lp:name>',str(rdf))
##  if len(name) > 0:
#    #print name[0][9:len(name[0])-10]
#    try:
#      connection.execute(project.insert().values(datasource_id=DATASOURCE,project_name = name[0][9:len(name[0])-10]))
#    except sqlalchemy.exc.IntegrityError:
#      pass
  dname = re.findall('<lp:displayName>.*?</lp:displayName>',str(rdf))
  if len(dname) > 0:
    #print dname[0][16:len(dname[0])-17]
    try:
      connection.execute(project.update().where(project.c.project_name == rdf['project_name']).where(project.c.datasource_id == DATASOURCE).values(display_name = dname[0][16:len(dname[0])-17]))
    except sqlalchemy.exc.IntegrityError:
      pass
  title = re.findall('<lp:title>.*?</lp:title>',str(rdf))
  if len(title)>0:
    #print title[0][10:len(title[0])-11]
    try:
      connection.execute(project.update().where(project.c.project_name == rdf['project_name']).where(project.c.datasource_id == DATASOURCE).values(project_title = title[0][10:len(title[0])-11]))
    except sqlalchemy.exc.IntegrityError:
      pass
  sdesc = re.findall('<lp:shortDescription>.*?</lp:shortDescription>',str(rdf))
  if len(sdesc)>0:
    #print sdesc[0][21:len(sdesc[0])-22]
    try:
      connection.execute(project.update().where(project.c.project_name == rdf['project_name']).where(project.c.datasource_id == DATASOURCE).values(short_description = sdesc[0][21:len(sdesc[0])-22]))
    except sqlalchemy.exc.IntegrityError:
      pass
  desc = re.findall('<lp:description>.*?</lp:description>',str(rdf))
  if len(desc)>0:
    #print desc[0][16:len(desc[0])-17]
    try:
      connection.execute(project.update().where(project.c.project_name == rdf['project_name']).where(project.c.datasource_id == DATASOURCE).values(description = desc[0][16:len(desc[0])-17]))
    except sqlalchemy.exc.IntegrityError:
      pass
  create = re.findall('<lp:creationDate>.*?</lp:creationDate>',str(rdf))
  if len(create) > 0:
    #print create[0][17:len(create[0])-18]
    try:
      connection.execute(project.update().where(project.c.project_name == rdf['project_name']).where(project.c.datasource_id == DATASOURCE).values(created = create[0][17:len(create[0])-18]))
    except sqlalchemy.exc.IntegrityError:
      pass
  status = re.findall('<lp:status>.*?</lp:status>',str(rdf))
  if len(status) > 0:
    #print status[0][11:len(status[0])-12]
    try:
      connection.execute(project.update().where(project.c.project_name == rdf['project_name']).where(project.c.datasource_id == DATASOURCE).values(project_status = status[0][11:len(status[0])-12]))
    except sqlalchemy.exc.IntegrityError:
      pass
  lang = re.findall('<lp:programmingLanguage>.*?</lp:programmingLanguage>',str(rdf))
  if lang:
    languages = lang[0][24:len(lang[0])-25].split(',')
    for x in languages:
    #print lang[0][24:len(lang[0])-25]
      try:
	connection.execute(proj_lang.insert().values(language = x,datasource_id = DATASOURCE,project_name = rdf['project_name'],last_updated = func.now()))
      except sqlalchemy.exc.IntegrityError:
	pass
  wiki = re.findall('<lp:wiki rdf:resource=".*?"/>',str(rdf))
  if(len(wiki)>0):
    try:
      connection.execute(project.update().where(project.c.project_name == rdf['project_name']).where(project.c.datasource_id == DATASOURCE).values(wiki = wiki[0][23:len(wiki[0])-3]))
    except sqlalchemy.exc.IntegrityError:
      pass
  #add wiki column
  home = re.findall('<lp:homepage rdf:resource=".*?"/>',str(rdf))
  if(len(home)>0):
    try:
      connection.execute(project.update().where(project.c.project_name == rdf['project_name']).where(project.c.datasource_id == DATASOURCE).values(homepage = home[0][27:len(home[0])-3]))
    except sqlalchemy.exc.IntegrityError:
      pass
  #add homepage column
  screenshot = re.findall('<lp:screenshot>.*?</lp:screenshot>',str(rdf))
  if(len(screenshot)>0):
    try:
      connection.execute(project.update().where(project.c.project_name == rdf['project_name']).where(project.c.datasource_id == DATASOURCE).values(screenshot = screenshot[0][15:len(screenshot[0])-16]))
    except sqlalchemy.exc.IntegrityError:
      pass
  #add screenshot column
  
def getHtmlInfo(html):
  


  l = re.compile('<dt>Licenses:</dt>.*?</dd>',re.DOTALL)
  license = re.search(l,html['html'])
  if license:
    l = re.compile('<dd>.*?</dd>',re.DOTALL)
    license2 = re.search(l,license.group(0))
    lic3 = re.sub('\s+',' ',license2.group(0)[4:len(license2.group(0))-5].strip().replace('\n','')).split(', ')
    for x in lic3:
      try:
	connection.execute(licenses.insert().values(datasource_id=DATASOURCE,project_name = html['project_name'],license=x,last_updated = func.now()))
      except  sqlalchemy.exc.IntegrityError:
	pass
    
  focus = re.search('<dt>Development focus:</dt>\n                <dd>\n                  <p>\n                  <a href=".*?">.*?</a>&nbsp;',html['html'])
  if focus:
    focus2 = re.search('">.*?</',focus.group(0))
    #print focus2.group(0)[2:len(focus2.group(0))-2]
    try:
      connection.execute(project.update().where(project.c.project_name == html['project_name']).where(project.c.datasource_id == DATASOURCE).values(focus = focus2.group(0)[2:len(focus2.group(0))-2]))
    except sqlalchemy.exc.IntegrityError:
      pass
  
  l = re.compile('<dt>Uses Launchpad for:</dt>\n                  <dd>.*?</dd>',re.DOTALL)
  use = re.search(l,html['html'])
  if use:
    alluses = re.findall('">.*?</a>',use.group(0)[29:len(use.group(0))-6].strip())
    for x in alluses:
      try:
	connection.execute(uses.insert().values(datasource_id = DATASOURCE,project_name = html['project_name'],uses = x[2:len(x)-4],last_updated = func.now()))
      except sqlalchemy.exc.IntegrityError:
	pass

def getDevInfo(contrib):
  
  realname = re.findall('<title>.*? in Launchpad</title>',contrib['html'])
  if realname:
    real = realname.pop()
    #print real[7:len(real)-21]
    try:
      connection.execute(devs.update().where(devs.c.dev_loginname == contrib['dev_loginname']).where(devs.c.datasource_id == DATASOURCE).values(realname = real[7:len(real)-21]))
    except sqlalchemy.exc.IntegrityError:
      pass
  
  signer = re.findall('<span id="ubuntu_coc_signer">\S*?</span>',contrib['html'])
  if signer:
    sign = signer.pop()
    #print sign[29:len(sign)-7]
    try:
      connection.execute(devs.update().where(devs.c.dev_loginname == contrib['dev_loginname']).where(devs.c.datasource_id == DATASOURCE).values(coc_signer = sign[29:len(sign)-7]))
    except sqlalchemy.exc.IntegrityError:
      pass
  
  karma = re.findall('href="https://launchpad.net/~\S*/\+karma">\d+?</a>',contrib['html'])
  if karma:
    k = karma.pop()
    #print k[38+len(contrib['dev_loginname']):len(k)-4]
    try:
      connection.execute(devs.update().where(devs.c.dev_loginname == contrib['dev_loginname']).where(devs.c.datasource_id == DATASOURCE).values(karma = int(k[38+len(contrib['dev_loginname']):len(k)-4])))
    except sqlalchemy.exc.IntegrityError:
      pass

  time = re.findall('<dt>Time zone:\n        \n      </dt>\n      <dd>.*?</dd>',contrib['html'])
  if time:
    tz = time.pop()
    #print tz[46:len(tz)-5]
    try:
      connection.execute(devs.update().where(devs.c.dev_loginname == contrib['dev_loginname']).where(devs.c.datasource_id == DATASOURCE).values(timezone = tz[46:len(tz)-5]))
    except sqlalchemy.exc.IntegrityError:
      pass
  
  #'<dt>Languages:\n        \n      </dt>\n      <dd>\n        Arabic, English, English (United Kingdom)\n      </dd>'
  l = re.compile('<dt>Languages:.*?</dd>',re.DOTALL)
  lang = re.findall(l,contrib['html'])
  if lang:
    language = lang.pop()[14:].replace('</dt>','').replace('<dd>','').replace('</dd>','').replace('\n','').strip()
    result = language.split(', ')
    for x in result:
      try:
	connection.execute(dev_lang.insert().values(dev_loginname = contrib['dev_loginname'], datasource_id = DATASOURCE, language = x, last_updated = func.now()))
      except sqlalchemy.exc.IntegrityError:
	pass
 
  join = re.findall('<dd id="member-since">\S*?</dd>',contrib['html'])
  if join:
    j=join.pop()
    #print j[22:len(j)-5]
    try:
      connection.execute(devs.update().where(devs.c.dev_loginname == contrib['dev_loginname']).where(devs.c.datasource_id == DATASOURCE).values(join_date = j[22:len(j)-5]))
    except sqlalchemy.exc.IntegrityError:
      pass

  desc = re.findall('<div class="description"><p>.*?</p></div>',contrib['html'])
  if desc:
    description = desc.pop()
    #print description[28:len(description)-10]
    try:
      connection.execute(devs.update().where(devs.c.dev_loginname == contrib['dev_loginname']).where(devs.c.datasource_id == DATASOURCE).values(description = description[28:len(description)-10]))
    except sqlalchemy.exc.IntegrityError:
      pass


  l = re.compile('<dt>Wiki:\n        \n      </dt>\n      <dd>.*?</dd>',re.DOTALL) #search for the href 44,l-5
  wiki0 = re.findall(l,contrib['html'])
  if wiki0:  
    wiki1 = re.findall('<a href="\S*?"',wiki0.pop())
    for x in wiki1:
      #print x[9:len(x)-1]
      try:
	connection.execute(dev_wiki.insert().values(dev_loginname = contrib['dev_loginname'], datasource_id = DATASOURCE, wiki = x[9:len(x)-1], last_updated = func.now()))
      except sqlalchemy.exc.IntegrityError:
	pass
      
      
  l = re.compile('<dt>IRC:.*?</dl>',re.DOTALL)
  irc0 = re.findall(l,contrib['html'])
  if irc0:
    l = re.compile('<dd>.*?</dd>',re.DOTALL)
    irclist = re.findall(l,irc0.pop())
    for x in irclist:
      pieces = re.findall('<strong>.*?</strong>',x)
      #print pieces[0][8:len(pieces[0])-9] #user
      #print pieces[1][8:len(pieces[1])-9] #server
      try:
	connection.execute(dev_irc.insert().values(dev_loginname = contrib['dev_loginname'], datasource_id = DATASOURCE, username = pieces[0][8:len(pieces[0])-9],server = pieces[1][8:len(pieces[1])-9],last_updated = func.now()))
      except sqlalchemy.exc.IntegrityError:
	pass

def getGroupInfo(html):
  
  #owner
  x = re.findall('<dt>Owner:</dt>\n        <dd>\n          <a href="/~\S*?"',html['html'])
  if x:
    #print x[0][50:len(x[0])-1]
    try:
      connection.execute(group.update().where(group.c.group_loginname == html['group_loginname']).where(group.c.datasource_id == DATASOURCE).values(last_updated = func.now(),group_owner = x[0][50:len(x[0])-1]))
    except sqlalchemy.exc.IntegrityError:
      pass
  
  #created
  created = re.findall('<span id="created-date"\n                title=".*?"',html['html'])
  if created:
    #print created[0][47:len(created[0])-1]
    try:
      connection.execute(group.update().where(group.c.group_loginname == html['group_loginname']).where(group.c.datasource_id == DATASOURCE).values(last_updated = func.now(),create_date = created[0][47:len(created[0])-1]))
    except sqlalchemy.exc.IntegrityError:
      pass
  
  #subscription policy
  sub = re.findall('<dt>Subscription policy:</dt>\n        <dd>\n          .*?\n',html['html'])
  if sub:
    #print sub[0][53:len(sub[0])-1]
    try:
      connection.execute(group.update().where(group.c.group_loginname == html['group_loginname']).where(group.c.datasource_id == DATASOURCE).values(last_updated = func.now(),subscription = sub[0][53:len(sub[0])-1]))
    except sqlalchemy.exc.IntegrityError:
      pass
  
  #active members
  members = re.findall('id="approved-member-count">\n          \d*?\n',html['html'])
  if members:
    #print members[0][38:len(members[0])-1]
    try:
      connection.execute(group.update().where(group.c.group_loginname == html['group_loginname']).where(group.c.datasource_id == DATASOURCE).values(last_updated = func.now(),active_count = int(members[0][38:len(members[0])-1])))
    except sqlalchemy.exc.IntegrityError:
      pass
  
  #description
  result='' 
  l = re.compile('description"><p>.*?</p>',re.DOTALL)
  desc = re.findall(l,html['html'])
  for x in desc:
    result += x[16:len(x)-4].replace('<br />',' ')
  if len(result)>0:
    #print result
    try:
      connection.execute(group.update().where(group.c.group_loginname == html['group_loginname']).where(group.c.datasource_id == DATASOURCE).values(last_updated = func.now(),description = result))
    except sqlalchemy.exc.IntegrityError:
      pass
 
#realname

  name = re.findall('<title>.*? in Launchpad</title>',html['html'])
  if name:
    #print name[0][7:len(name[0])-21]
    try:
      connection.execute(group.update().where(group.c.group_loginname == html['group_loginname']).where(group.c.datasource_id == DATASOURCE).values(last_updated = func.now(),realname = name[0][7:len(name[0])-21]))
    except sqlalchemy.exc.IntegrityError:
      pass

 
 
 
 #add owner to group
 #subscription
 #created
 #active_count
 #description
 
def parseRdf():
  #uses lots of mem...
  namelist = connection.execute("SELECT project_name from "+PROJ_INDEXES+" where rdf is not null and datasource_id = "+str(DATASOURCE)+";")
  for y in namelist:
    rdflist = connection.execute("SELECT project_name,rdf from "+PROJ_INDEXES+" where rdf IS NOT NULL AND datasource_id = "+str(DATASOURCE)+" and project_name = '"+y['project_name']+"';")
    for x in rdflist:
      getRdfInfo(x)

def parseDev():
  namelist = connection.execute("SELECT dev_loginname from "+DEV_INDEXES+" where html is not null and datasource_id = "+str(DATASOURCE)+";")
  for y in namelist:
    devlist = connection.execute("SELECT dev_loginname,html from "+DEV_INDEXES+" where html IS NOT NULL AND datasource_id = "+str(DATASOURCE)+" and dev_loginname = '"+y['dev_loginname']+"';")
    for x in devlist:
      getDevInfo(x)

def parseGrp():
  namelist = connection.execute("SELECT group_loginname from "+GROUP_INDEXES+" where html is not null and datasource_id = "+str(DATASOURCE)+";")
  for y in namelist:
    grouplist = connection.execute("SELECT group_loginname,html from "+GROUP_INDEXES+" where html is not null and datasource_id = "+str(DATASOURCE)+" and group_loginname = '"+y['group_loginname']+"';")
    for x in grouplist:
      getGroupInfo(x)

#parseHtml()
#parseRdf()
#parseDev()
parseGrp()

connection.close()