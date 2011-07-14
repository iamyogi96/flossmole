import urllib
import re
import time
import sys
import gzip
import sqlalchemy
from sqlalchemy import *
from sqlalchemy import exc
import codecs

from datetime import datetime
from dateutil.parser import parse


import warnings
warnings.filterwarnings('ignore')

import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('al.conf')

try:
  #config.get('alioth','username')
  DB_USER = config.get('alioth','user')
  DB_PASS = config.get('alioth','pass')
  DB_ADDRESS = config.get('alioth','address')

  MESSAGES = config.get('alioth','messages')
  MSG_REFS = config.get('alioth','msg_refs')
  MAILING_LISTS = config.get('alioth','mailing_lists')
  PROJECTS = config.get('alioth','projects')
  PROJECT_INDEXES = config.get('alioth','project_indexes')
  MAILING_LIST_INDEXES = config.get('alioth','mailing_list_indexes')
  MESSAGES_INDEXES = config.get('alioth','messages_indexes')
  DATASOURCE = config.getint('alioth','datasource')
    
  AUDIENCE = config.get('alioth','audience')
  OS = config.get('alioth','os')
  STATUS = config.get('alioth','status')
  LICENSE = config.get('alioth','license')
  ENVIRONMENT = config.get('alioth','environment')
  TOPIC = config.get('alioth','topic')
  LANGUAGE = config.get('alioth','language')
except exception as e:
  print e
  print 'error reading al.conf'
  sys.exit(1)


def uploadMsg(mlist, url,msg):


  ins = {}
  fr = re.search(r'From: (.*?)\n',msg)
  date = re.search(r'Date: (.*?)\n',msg)
  msg_id = re.search(r'Message-ID: <(.*?)>',msg)
  sub = re.search(r'Subject: (.*?)\n\S+?:',msg,re.DOTALL)
  body = re.search(r'\nMessage-ID: .*?\n(.*)',msg,re.DOTALL)
  reply = re.search(r'\nIn-Reply-To: <(.*?)>',msg)
  ref = re.findall(r'\nReferences: (.*?)\n\S+?:',msg,re.DOTALL)
  for reference in ref:
    really = re.findall('<(.*?)>',reference)
    for each in really:
    ########meh
      try:
        #pass
        if msg_id:
          connection.execute(msg_refs.insert().values(datasource_id = DATASOURCE, mailing_list = mlist, message_id = msg_id.group(1).strip(), reference = each))
      except exc.IntegrityError as i:
        #print i
        pass
      except Exception as e:
        print msg[:1000]
        print ' '
        print 'something happened with references, sleepint for 5 sec'
        print '\n'
        print e
        time.sleep(5)
    if reply:
      ins['reply_to'] = reply.group(1).strip()
    if fr:
      ins['sender'] = fr.group(1).strip()
    else:
      return #no point in continuing if it's not a real message
      #ins['mailing_list'] = mlist
      #ins['datasource_id'] = DATASOURCE
      #ins['url'] = url
    if date:
      try:
        ins['date_sent'] = parse(date.group(1).strip())
      except:
        pass
    if msg_id:
      ins['message_id'] = msg_id.group(1).strip()
    if sub:
      ins['subject'] = sub.group(1).strip()
    if body:
      ins['body'] = body.group(1).strip()
    try:

      ins['mailing_list'] = mlist
      ins['datasource_id'] = DATASOURCE
      ins['url'] = url
    except:
      return
    try:
      #pass
      connection.execute(messages.insert().values(ins))
    except exc.IntegrityError as i:
      #print i
      pass
    except Exception as e:
      print msg[:1000]
      print ' '
      print 'something happened with messages, sleeping for 5'
      print '\n'
      time.sleep(5)

def parseMessages():
  msgs_list = connection.execute('SELECT distinct i.url FROM `'+MESSAGES_INDEXES+'` i left outer join `'+MESSAGES+'` m on i.url = m.url WHERE m.url IS NULL;')
  for url in msgs_list:
    current = connection.execute('SELECT url,mailing_list,list_index FROM `'+MESSAGES_INDEXES+'` WHERE url = "'+url[0]+'";').fetchone()

    #print current['list_index']
   
    ##r'From treina at styllusconsultoria.com.br  Wed Feb 23 19:40:37 2011'
    m = re.compile(r'From.*?\d{2}:\d{2}:\d{2} \d{4}')
    #m = re.compile(r'From\s+\S+\s+at\s+\S+\s+\S+\s+\S+\s+\d+\s+\d{2}:\d{2}:\d{2} \d+')
    for msg in m.split(current['list_index']):
      #print msg
      #time.sleep(3)
      uploadMsg(current['mailing_list'],current['url'],msg.strip())

def parseMailingLists():
  projects = connection.execute('SELECT project FROM '+MAILING_LIST_INDEXES+' WHERE datasource_id = '+str(DATASOURCE)+';')
  for each in projects:
    current = connection.execute('SELECT project,html FROM '+MAILING_LIST_INDEXES+' WHERE datasource_id = '+str(DATASOURCE)+' AND project = "'+each['project']+'";').fetchone()
    project = current['project']
    html = current['html'][current['html'].find('<tbody>'):current['html'].find('</tbody>')]
    lists = re.findall('<a href="http://lists.alioth.debian.org/pipermail/.*?/">(.*?)</a></strong></td><td>(.*?)</td>',html)
    for l in lists:
      #list name (teh word 'Archives' is parsed out), list desc
      try:
        connection.execute(mailing_lists.insert().values(datasource_id = DATASOURCE, mailing_list = l[0][:len(l[0])-9], description = l[1], project = project))
      except Exception as e:
        print e
        time.sleep(5)
      #print l[0][:len(l[0])-9]+' :: '+l[1]

def parseProject(html):
  d = re.search(r'<span property="doap:name">(.*?)</span>',html)
  if d:
    display_name = d.group(1)
  else:
    diplay_name = None

  s = re.search(r'<span property="doap:short_desc">(.*?)</span>',html)
  if s:
    short_desc = s.group(1)
  else:
    short_desc = None

  r = re.search(r'<br />Register Date: <strong>(.*?)</strong>',html)
  if r:
    try:
      registered = parse(r.group(1))
    except:
      registered = None
  else:
    registered = None

  u = re.search(r'<div typeof="doap:Project sioc:Space" about="https://alioth.debian.org/projects/(\S+)/">',html)
  if u:
    unixname = u.group(1)
  else:
    unixname = None

  try:
    connection.execute(projects.insert().values(datasource_id = DATASOURCE, display_name = display_name, unixname = unixname, short_desc = short_desc, registered = registered))
  except exc.IntegrityError as i:
    pass
  except Exception as e:
    print e
    time.sleep(5)

  lists = re.findall('<li>.*?</li>',html)
  for li in lists:
    items = re.findall(r'[0-9]">(.*?)</a>', li)
    ins = {}
    table = None
    ins['datasource_id'] = DATASOURCE
    ins['unixname'] = unixname
    if items[0] == 'Intended Audience':
      ins['audience'] = items[len(items)-1]
      table = al_audience
    elif items[0] == 'Operating System':
      ins['os'] = items[len(items)-1]
      table = al_os
    elif items[0] == 'Development Status':
      ins['status'] = items[len(items)-1]
      table = al_status
    elif items[0] == 'License':
      ins['license'] = items[len(items)-1]
      table = al_license
    elif items[0] == 'Environment':
      ins['environment'] = items[len(items)-1]
      table = al_environment
    elif items[0] == 'Topic':
      ins['topic'] = items[len(items)-1]
      table = al_topic
    elif items[0] == 'Programming Language':
      ins['language'] = items[len(items)-1]
      table = al_language

    try:
      connection.execute(table.insert().values(ins))
    except Exception as e:
      #print e
      pass
      #time.sleep(5)

    #print items[0] + ' ' + items[len(items)-1]
    #for item in items:
      #string += item+'::'
    #print string[:len(string)-2]
  
  #print 'name '+str(display_name)
  #print 'unixname '+str(unixname)
  #print 'reg: '+str(registered)
  #print 'desc '+str(short_desc)
  #print '\n'

db = create_engine('mysql://'+DB_USER+':'+DB_PASS+'@'+DB_ADDRESS+'?charset=utf8&use_unicode=1')
connection = db.connect()
meta = MetaData()
meta.bind = connection

messages = Table(MESSAGES, meta, autoload=True)
msg_refs = Table(MSG_REFS, meta, autoload=True)
mailing_lists = Table(MAILING_LISTS, meta, autoload=True)
projects = Table(PROJECTS, meta, autoload=True)
project_indexes = Table(PROJECT_INDEXES, meta, autoload=True)
mailing_list_indexes = Table(MAILING_LIST_INDEXES, meta, autoload=True)
message_indexes = Table(MESSAGES_INDEXES, meta, autoload=True)

al_audience = Table(AUDIENCE, meta, autoload=True)
al_os = Table(OS, meta, autoload=True)
al_status = Table(STATUS, meta, autoload=True)
al_license = Table(LICENSE, meta, autoload=True)
al_environment = Table(ENVIRONMENT, meta, autoload=True)
al_topic = Table(TOPIC, meta, autoload=True)
al_language = Table(LANGUAGE, meta, autoload=True)

#
#more tables
#

print 'Parsing mailing list messages, this will take a while.'
parseMessages()
print 'Parsing mailing lists, shouldn\'t take long'
parseMailingLists()
print 'Parsing projects (final step)'

proj_list = connection.execute('SELECT id FROM '+PROJECT_INDEXES+' WHERE datasource_id = '+str(DATASOURCE)+';')
for proj in proj_list:
  h = connection.execute('SELECT html FROM '+PROJECT_INDEXES+' WHERE id = '+str(proj['id'])+';')
  html = h.fetchone()['html']
  h.close()
  
  #proj_page = proj['html']
  x = re.findall(r'<div typeof="doap:Project sioc:Space".*?</strong></td></tr></table></div>',html,re.DOTALL)
  for each in x:
    parseProject(each)

