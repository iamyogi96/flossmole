# -*- coding: utf-8 -*-
import re
import StringIO
import sys
import os
import tarfile
import zipfile
#from pyparsing import dblQuotedString
#from pyparsing import sglQuotedString
import sqlalchemy
from sqlalchemy import *
import shutil
from mpi4py import MPI
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('metric.conf')

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

cachedir = 'metric_cache'+str(rank)+'/'
if not os.path.exists(cachedir):
  os.makedirs(cachedir)

try:
  DB_USER = config.get('metric','user')
  DB_PASS = config.get('metric','pass')
  DB_ADDRESS = config.get('metric','database')
  METRIC = config.get('metric','table')
  DATASOURCE = config.getint('metric','datasource')
except:
  print 'error reading config file'
  sys.exit(1)

#database setup
mysql_db = create_engine('mysql://'+DB_USER+':'+DB_PASS+'@'+DB_ADDRESS+'?charset=utf8&use_unicode=0')
connection = mysql_db.connect()
meta = MetaData()
meta.bind = connection
metrics = Table(METRIC, meta, autoload=True)

def untarFile(filename):
  tf = tarfile.open(filename,'r')
  for item in tf:
    tf.extract(item,path=cachedir)   

def walkSource():
  filestack = []
  files = os.walk(cachedir)
  for x in files:
    for y in x[2]:
      if y[len(y)-2:len(y)] == '.c' or y[len(y)-2:len(y)] == '.h' or y[len(y)-5:len(y)] == '.h.in' or y[len(y)-4:len(y)] == '.cpp' or y[len(y)-4:len(y)] == '.c++': #other extensions?
	try:
          if os.path.getsize(x[0]+ '/' + y) > 8: #no more empty files
	    reader = open(x[0]+ '/' + y,'r')
	    filestack.append(reader.read())
	    reader.close()
	except:
	  print 'failed to open: '+x[0]+'/'+y
  if len(filestack) <1:
    return 'EMPTY'
  return filestack

def stripSource1(source):

  parsed_source = source

  parsed_source=re.sub(r'[^\\]".*[^\\]"','""',parsed_source)
  parsed_source=re.sub(r"[^\\]'.*[^\\]'","''",parsed_source)
#  dblQuotedString.setParseAction(lambda : "")
#  sglQuotedString.setParseAction(lambda : "")

#  for x in dblQuotedString.scanString(parsed_source):
#    parsed_source = parsed_source.replace(parsed_source[x[1]:x[2]],'')

 # for x in sglQuotedString.scanString(parsed_source):
  #  parsed_source = parsed_source.replace(parsed_source[x[1]:x[2]],'')
    
  return parsed_source

def stripSource2(source):
  parsed_source = source
  cstyle = re.compile('/\*.*?\*/',re.DOTALL)
  parsed_source = re.sub(cstyle,'',parsed_source)  
  
  #removes single line comments (c++ style)
  parsed_source = re.sub('//.*','',parsed_source)
  #remove blank lines
  parsed_source = re.sub('\n\s*?\n','\n',parsed_source)
  return parsed_source
  
def stripSource3(source):
  #remove double spaces, and newlines
  return re.sub('\s+',' ',re.sub('\n',' ',source)) #pulls out newlines first, so we dont create new dbl spaces 
						   ## might not need the \n part, \s+ could pull newlines as well

def buildStripped1():
  for source in fs1:
    fs2.append(stripSource1(source))
  return fs2

def buildStripped2():
  for source in fs2:
    fs3.append(stripSource2(source))
  return fs3

def buildStripped3():
  for source in fs3:
    fs4.append(stripSource3(source))
  return fs4

def getNumFiles():
  return len(fs1)

def getLines():
  lines = 0
  for sourcefile in fs2:
    lines += (len(re.findall('\n',sourcefile))+1)
  return lines

def getSourceLines():
  lines = 0
  for sourcefile in fs3:
    lines += (len(re.findall('\n',sourcefile))+1)
  return lines

def getBlankLines():
  numlines = 0
  for sourcefile in fs2:
    lines = re.findall('\n\s*?\n',sourcefile)
    numlines += len(lines)
  return numlines

def getComments():
  comments = 0
  for sourcefile in fs1:
    single = re.findall('//.*?\n',sourcefile)
    if single:
      comments += len(single)
    l = re.compile('/\*.*?\*/',re.DOTALL)
    multiline = re.findall(l,sourcefile)
    for instance in multiline:
      nl = re.findall('\n',instance)
      if nl:
	comments += (len(nl) + 1)
      else:
	comments += 1
  return comments



def getMaxDepth():
  maxdepth = 0  
  for sourcefile in fs4:
    depth = 0
    for char in sourcefile:
      if char == '{':
	depth += 1
      elif char == '}':
	depth -= 1
      if depth > maxdepth:
	maxdepth = depth
  return maxdepth

def getMethods():
  summation = 0
  for sourcefile in fs4:
    x = re.findall('\w+? \w+?\s?\(.*?\)\s?{.*?}',sourcefile)
    summation += len(x)
  return summation

def getStruct():
  summation = 0
  for sourcefile in fs4:
    x = re.findall('struct \w+?\s?{.*?}',sourcefile)
    summation += len(x)
  return summation

def getFanout():
  includes = set()
  for sourcefile in fs4:
    found = re.findall('#include\s?<.*?>',sourcefile)
    for instance in found:
      includes.add(instance)
  return len(includes)

def getNcloc():#non-comment lines of code
  temp = []
  total = 0
  cstyle = re.compile('/\*.*?\*/',re.DOTALL)
  for sourcefile in fs2:
    parsed_source = sourcefile    
    parsed_source = re.sub(cstyle,'',parsed_source)
    parsed_source = re.sub('//.*','',parsed_source)
    temp.append(parsed_source)
  for sourcefile in temp:
    lines = re.findall('\n',sourcefile)
    total += len(lines)
  return total
  
def getTodo():
  summation = 0
  for sourcefile in fs1:
    todo = []
    todo.append(re.findall('TODO',sourcefile))
    todo.append(re.findall('FIX-ME',sourcefile))
    todo.append(re.findall('FIXME',sourcefile))
    todo.append(re.findall('FIX-IT',sourcefile))
    todo.append(re.findall('FIXIT',sourcefile))
    todo.append(re.findall('TO-DO',sourcefile))
    todo.append(re.findall('TODO',sourcefile))
    todo.append(re.findall('XXX',sourcefile))
    todo.append(re.findall('TBD',sourcefile))
    for x in todo:
      summation += len(x)
  return summation  

def getWmc():
  summation = 0
  for sourcefile in fs4:
    a = re.findall('\sif\s?\(',sourcefile)
    b = re.findall('\swhile\s?\(',sourcefile)
    c = re.findall('\sfor\s?\(',sourcefile)
    d = re.findall('\scase\s.*?:',sourcefile)
    e = re.findall('\sdefault\s?:',sourcefile)
    f = re.findall('\sdo\s?{',sourcefile)
    summation += ( len(a)+len(b)+len(c)+len(d)+len(e)+len(f) )
  return summation + num_methods
  
def getBooleanComplex():
  summation = 0
  for sourcefile in fs4:
    x = re.findall('(&&)|(\|\|)|(!)',sourcefile) # && || !
    summation += len(x)
  return summation
    

def getClasses():
  summation = 0
  for sourcefile in fs4:
    x = re.findall(' class .*?{.*?};',sourcefile)
    summation += len(x)
  return summation

proj_list = connection.execute("SELECT project_name,path FROM "+METRIC+" WHERE datasource_id = "+str(DATASOURCE)+" AND dc IS NULL;").fetchall()
#print proj_list[0][1]

n = len(proj_list)/comm.Get_size()
ilo = rank*n
ihi = (rank+1)*n-1
if rank+1 == comm.Get_size():
  ihi = len(proj_list)-1
    
for i in range(ilo,ihi+1):
  shutil.rmtree(cachedir)
  if not os.path.exists(cachedir):
    os.makedirs(cachedir)
  
  num_files = 0
  num_comments = 0
  num_lines = 0
  ncss = 0
  #num_blank = 0
  max_bracket_depth = 0
  num_todo = 0
  num_methods = 0
  fanout = 0
  ncloc = 0
  noc = 0
  fs1 = []
  fs2 = []
  fs3 = []
  fs4 = []
  print proj_list[i][0] + "   " +proj_list[i][1] 
  untarFile(proj_list[i][1]) #index i, 1 is path (0 being name)
  print 'untar done'
  fs1 = walkSource()
  
  print 'Source walked'

  if fs1 == 'EMPTY':
    connection.execute(metrics.update().where(metrics.c.datasource_id == DATASOURCE).where(metrics.c.project_name == proj_list[i][0]).values(dc=-1,last_updated = func.now()))
    print 'empty project'
    continue

  print 'not empty'

  fs2 = buildStripped1()
  print 'stripped 1'
  fs3 = buildStripped2()
  print 'stripped 2'
  fs4 = buildStripped3()
  print 'stripped 3'
  num_files = getNumFiles()
  num_lines = getLines()
  num_comments = getComments()
  ncss = getSourceLines()
  ncloc = getNcloc()
  #num_blank = getBlankLines()
  #max_bracket_depth = getMaxDepth()
  num_todo = getTodo()
  num_methods = getMethods()
  num_struct = getStruct() ## add into database
  fanout = getFanout()
  wmc = getWmc() #must be done AFTER getMethods
  bool_cmp = getBooleanComplex()
  classes = getClasses()
  
  connection.execute(metrics.update().where(metrics.c.datasource_id == DATASOURCE).where(metrics.c.project_name == proj_list[i][0]).values(todo_count = num_todo,dc = float(num_comments)/float(num_lines),cloc = num_comments,loc = num_lines,ncloc = ncloc,ncss = ncss,nom = num_methods,bool_exp = bool_cmp, fanout = fanout, wmc = wmc,files = num_files,noc = classes,last_updated = func.now()))

shutil.rmtree(cachedir)
