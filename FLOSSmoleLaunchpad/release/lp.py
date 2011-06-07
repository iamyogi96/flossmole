import sys
import os
import time
import lpSetup
from dbSetup import dbConnect
launchpad = lpSetup.lpObj()
from project_list import *
from sqlalchemy.sql import func
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('lp.conf')


try:
  PROJECTS = config.get('launchpad','projects')
  LICENSES = config.get('launchpad','licenses')
  BUG_TAGS = config.get('launchpad','bug_tags')
  LANGUAGES = config.get('launchpad','languages')
  MILESTONES = config.get('launchpad','milestones')
  RELEASES = config.get('launchpad','releases')
  SERIES_TABLE = config.get('launchpad','series_table')
  DATASOURCE = config.getint('launchpad','datasource')

  db=dbConnect(config.get('launchpad','db_user'),config.get('launchpad','db_pass'),config.get('launchpad','db_address'))
except Exception as e:
  print e
  print 'error reading lp.conf'
  sys.exit(1)


projects = db.getTable(PROJECTS)
licenses = db.getTable(LICENSES)
bug_tags = db.getTable(BUG_TAGS)
languages = db.getTable(LANGUAGES)
milestones = db.getTable(MILESTONES)
releases = db.getTable(RELEASES)
series_table = db.getTable(SERIES_TABLE)

if len(db.connection.execute("SELECT name FROM "+PROJECTS+" WHERE datasource_id = "+str(DATASOURCE)+";").fetchall()) < len(launchpad.projects)-100: #the 100 allows for growth over a couple hours/days.
  i = projects.insert()
  resultList = getLpProjList()
  for project_name in resultList:
    try:
      db.connection.execute(projects.insert().values(name=project_name,last_updated=func.now(),datasource_id=DATASOURCE))
    except Exception as e:
      print e
      time.sleep(2)

names = db.connection.execute("SELECT name FROM "+PROJECTS+" WHERE datasource_id = "+str(DATASOURCE)+" AND display_name IS NULL;")
for result in names:
  print result['name']

  for license in launchpad.projects[result['name']].licenses:
    try:
      db.connection.execute(licenses.insert().values(name=result['name'],datasource_id = DATASOURCE,last_updated = func.now(),license = license))    
    except Exception as e:
      print e
      time.sleep(5)

  for bug_tag in launchpad.projects[result['name']].official_bug_tags:
    try:
      db.connection.execute(bug_tags.insert().values(name=result['name'],datasource_id = DATASOURCE,last_updated = func.now(),official_bug_tag = bug_tag))    
    except Exception as e:       
      print e
      time.sleep(5)

  if launchpad.projects[result['name']].programming_language:
    langs = launchpad.projects[result['name']].programming_language.split(',')
    for language in langs:
      try:
        db.connection.execute(languages.insert().values(name=result['name'],datasource_id = DATASOURCE,last_updated = func.now(),programming_language = language.strip()))    
      except Exception as e:                
        print e        
        time.sleep(5)

  for milestone in launchpad.projects[result['name']].all_milestones.entries:
    try:
      db.connection.execute(milestones.insert().values(datasource_id = DATASOURCE,last_updated = func.now(),name=milestone['name'], title=milestone['title'], summary = milestone['summary'],code_name = milestone['code_name'], date_targeted = milestone['date_targeted'],is_active = milestone['is_active'],project_name = result['name']))
      #official_bug_tags?  meh...
    except Exception as e:
      print e
      time.sleep(5)

  for release in launchpad.projects[result['name']].releases.entries:
    try:
      db.connection.execute(releases.insert().values(datasource_id = DATASOURCE,last_updated = func.now(),display_name = release['display_name'],title = release['title'],milestone=launchpad.projects[result['name']].getMilestone(name=release['milestone_link'][release['milestone_link'].find('+milestone/')+11:]).name, version = release['version'], project_name = result['name'], release_notes = release['release_notes'],changelog = release['changelog'], date_created = release['date_created'], date_released = release['date_released']))
    except Exception as e:
      print e
      time.sleep(5)

  
  for series in launchpad.projects[result['name']].series.entries:
    try:
      db.connection.execute(series_table.insert().values(datasource_id = DATASOURCE, last_updated = func.now(), bug_reported_acknowledgement = series['bug_reported_acknowledgement'],display_name = series['display_name'], title = series['title'], status = series['status'], date_created = series['date_created'], active = series['active'], name = series['name'], summary = series['summary'], bug_reporting_guidelines = series['bug_reporting_guidelines'], project_name = result['name']))
    except Exception as e:
      print e
      time.sleep(5)

  #major project data insert
  try:
    db.connection.execute(projects.update().where(projects.c.datasource_id == DATASOURCE).where(projects.c.name == result['name']).values(getProjectInfo(result['name'],launchpad),last_updated = func.now()))
  except Exception as e:
    print e
    time.sleep(5)

