import re
import sys
import os
import sqlalchemy
from sqlalchemy import *
import ConfigParser
import warnings

config = ConfigParser.RawConfigParser()
config.read('udd.conf')
#disables warnings
warnings.filterwarnings('ignore', '.*')
try:
  DB_USER = config.get('udd','user')
  DB_PASS = config.get('udd','pass')
  DB_ADDRESS = config.get('udd','database')
except:
  print 'error reading the config file, please make sure it is set up properly, and is in the working directory'
  sys.exit(1)

try:
  DATASOURCE = int(sys.argv[1])
  FILENAME = sys.argv[2]
  if not os.path.exists(FILENAME):
    raise Error('bad filename')
except:
  print 'error reading command line input, should be datasource followed by path the sql file'
  sys.exit(1)

mysql_db = create_engine('mysql://'+DB_USER+':'+DB_PASS+'@'+DB_ADDRESS+'?charset=utf8&use_unicode=0')
connection = mysql_db.connect()
meta = MetaData()
meta.bind = connection

f = open(FILENAME,'r')
cols = []
name= null
cur=null
for line in f:
  if line[:2] == '\\.':
    name = null
  table = re.match('COPY\s+(\w+)\s+\((.*?)\)\s+FROM\s+stdin;',line)
  if name != null:
     values = line.split('\t')
     ins = cur.insert()
     statements = {'datasource_id': str(DATASOURCE)}
     for i in range(len(cols)):
       if values[i].strip() == '\\N':
         statements[cols[i].strip()] = None
       elif values[i].strip() == 't':
         statements[cols[i].strip()] = '1'
       elif values[i].strip() == 'f':
         statements[cols[i].strip()] = '0'
       else:
         statements[cols[i].strip()] = values[i].strip()
     try:
       ins.execute(statements)
     except:
       print statements
     del(statements)
  if table:
    name = 'udd_'+table.group(1)
    print name
    cur = Table('udd_'+table.group(1), meta, autoload=True)
    cols = table.group(2).split(',')

    for i in range(len(cols)):
      if cols[i].strip() == 'file':
        cols[i] = 'filename'
      elif cols[i].strip() == '"time"':
        cols[i] = 'time'
      elif cols[i].strip() == 'release':
        cols[i] = 'released'
      elif cols[i].strip() == 'key':
        cols[i] = 'key_info'

connection.close()
