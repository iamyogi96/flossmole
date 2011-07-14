import urllib
import re
import time
import sys
import gzip
import sqlalchemy
from sqlalchemy import *
import codecs

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
except exception as e:
  print e
  print 'error reading al.conf'
  sys.exit(1)

db = create_engine('mysql://'+DB_USER+':'+DB_PASS+'@'+DB_ADDRESS+'?charset=utf8&use_unicode=1')
connection = db.connect()
meta = MetaData()
meta.bind = connection

messages = Table(MESSAGES, meta, autoload=True)
msg_refs = Table(MSG_REFS, meta, autoload=True)
mailing_lists = Table(MAILING_LISTS, meta, autoload=True)
#projects = Table(MESSAGES, meta, autoload=True)
project_indexes = Table(PROJECT_INDEXES, meta, autoload=True)
mailing_list_indexes = Table(MAILING_LIST_INDEXES, meta, autoload=True)
message_indexes = Table(MESSAGES_INDEXES, meta, autoload=True)
#
#more tables
#

'''def uploadMsg(project,mlist,url,msg):
  ins = {}
  fr = re.search(r'From: (.*?)\n',msg)
  date = re.search(r'Date: (.*?)\n',msg)
  msg_id = re.search(r'Message-ID: (.*?)\n',msg)
  sub = re.search(r'Subject: (.*?)\n',msg)
  body = re.search(r'Message-ID: .*?\n(.*)',msg,re.DOTALL)
  reply = re.search(r'In-Reply-To: (.*?)\n',msg)
  ref = re.findall(r'References: (.*?)\n',msg)
  for reference in ref:
########meh
    try:
      connection.execute(msg_refs.insert().values(datasource_id = DATASOURCE, mailing_list = mlist, message_id = msg_id.group(1).strip(), reference = reference))
    except Exception as e:
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
    ins['date_sent'] = date.group(1).strip()
  if msg_id:
    ins['message_id'] = msg_id.group(1).strip()
  if sub:
    ins['subject'] = sub.group(1).strip()
  if body:
    ins['body'] = body.group(1).strip()
  ins['mailing_list'] = mlist
  ins['datasource_id'] = DATASOURCE
  ins['url'] = url
  try:
    connection.execute(messages.insert().values(ins))
  except Exception as e:
    print e
    time.sleep(5)
'''
def downloadTar(mlist,project,url):

#### select distinct url from al_messages where mlist = mlist and datasource_id = datasource;
###  if url isn't in the select, we're all good yo.

  url_list = connection.execute("SELECT count(url) FROM "+MESSAGES_INDEXES+" WHERE mailing_list = '"+mlist+"' AND datasource_id = "+str(DATASOURCE)+" AND url = '"+url+"';")
  if url_list.fetchone()['count(url)'] == 0:
    try:
      f = urllib.urlopen(url)
      g = open('tmp.txt.gz','w')
      g.write(f.read())
      f.close()
      g.close()
      gz = gzip.open('tmp.txt.gz','rb')
      mail = gz.read()
      gz.close()
    except Exception as e:
      print e
      print 'sleeping for 30 seconds before another attempt'
      time.sleep(30)
      downloadTar(mlist,project,url)
    try:
      connection.execute(message_indexes.insert().values(datasource_id = DATASOURCE, mailing_list = mlist, list_index = mail, url = url))
    except Exception as e:
      #print e
      #print 'sleeping for 30 seconds before another attempt'
      pass
      #time.sleep(30)
  ######got it!
#    m = re.compile(r'\nFrom\s+\S+\s+at\s+\S+\s+\S+\s+\S+\s+\d+\s+\d{2}:\d{2}:\d{2} \d+')
#    for msg in m.split(mail.strip()):
#      uploadMsg(project,mlist,url,msg.strip())
  url_list.close()
############

def parseListUrl(mlist,project,url):
  f = urllib.urlopen(url)
  page = f.read()
  f.close()

  tars = re.findall('<td><A href="(.*?.txt.gz)">\[ Gzip\'d Text .*? \]</a></td>',page)
  count = 0
  for tar in tars:
    #this way we never pull the latest (current month)
    #it is incomplete.
    if count > 0:
      downloadTar(mlist,project,url+tar)
    count += 1

def getMailingLists(project):
  try:
    #gets project page
    f = urllib.urlopen('https://alioth.debian.org/projects/'+str(project))
    page = f.read()
    f.close()
    #picks out mailing list link
    groupid = re.search(r'<a href="/mail/\?group\_id=(.+?)"',page)
    if not groupid:
      return
    #gets list of mailing lists
    f = urllib.urlopen('https://alioth.debian.org/mail/?group_id='+str(groupid.group(1)))
    page = f.read()
    f.close()
    try:
      connection.execute(mailing_list_indexes.insert().values(datasource_id = DATASOURCE, html = page, project = project))
    except Exception as e:
      print e
      print 'something happened, sleeping 5 seconds'
      time.sleep(5)
    lists = re.findall(r'<a href="(http://lists.alioth.debian.org/pipermail/(.+?)/)">',page)
    for mail in lists:
      parseListUrl(mail[1],project,mail[0])
  except Exception as e:
    print e
    print 'sleeping 30 seconds and attempting again'
    time.sleep(30)
    getMailingLists(project)


current = 1
total = 1
while int(current) <= int(total):
  print 'on page '+str(current)+' of '+str(total)
  try:
    f = urllib.urlopen('https://alioth.debian.org/softwaremap/full_list.php?page='+str(current))
    page = f.read()
    f.close()
  except Exception as e:
    print e
    print 'something failed, sleeping 30 sec'
    time.sleep(30)
    continue
  try:
    connection.execute(project_indexes.insert().values(datasource_id = DATASOURCE, page = current, html = page))
  except Exception as e:
    print e
    print 'something failed'
    time.sleep(5)
  maximum = re.search('&lt;(\d+)&gt;</a> </span><hr />',page)
  try:
    total = int(maximum.group(1))
  except:
    pass


  projects = re.findall('about="https://alioth.debian.org/projects/(.+?)/"',page)
  #print len(projects)
  for project in projects:
    getMailingLists(project)
  
  #otherwise we want to try again
  print 'num projects: '+str(len(projects))
  if len(projects) > 0:
    current += 1
  #print str(current) + ' / ' + str(total)
