#!/usr/bin/env python
import MySQLdb
import sys
import re
import traceback
import signal
import threading
from debian_Utilities import Debian_Utilities

#Global variables (not sure if we need this)
#isError = False

#Class for main routine
class Debian_ParseDescriptions:
    
    #Signal handler for clean exiting (SIGINT)
    def sigHandler(self, signum, frame):
        try:
            self.parse_Thread.join()
            self.util.updateStatus('complete', self.job[0])
            print 'Clean exit'
        except:
            self.util.postError(traceback.format_exc(), self.job[0])
        raise SystemExit
    
    #Main routine
    def __init__(self):
        self.util = Debian_Utilities()
        signal.signal(signal.SIGINT, self.sigHandler)
        while(True):
            global isError
            isError = False
            self.job = None
            self.job = self.util.findJob('descParse')
            if (self.job):
                try:
                    print 'Starting ' + self.job[1]
                    self.util.updateStatus('in progress', self.job[0])
                    self.parse_Thread = Parse_Thread(self.util, self.job[0], self.job[1], self.job[2], self.job[3])
                    self.parse_Thread.start()
                    self.parse_Thread.join()
                    if not isError:
                        self.util.updateStatus('complete', self.job[0])
                    print 'Finishing ' + self.job[1]
                except SystemExit:
                    sys.exit()
                except:
                    self.util.postError(traceback.format_exc(), self.job[0])

#Threaded class that does the actual work
class Parse_Thread(threading.Thread):
    def __init__(self, util, job_id, projName, debianType, datasource):
        threading.Thread.__init__(self)
        self.util = util
        self.job_id = job_id
        self.projName = projName
        self.debianType = debianType
        self.datasource = datasource
        
    #Parse routine that gets the project description, long name, version, and any
    #URLs included in the description
    def run(self):
        try:
            if self.debianType == 'stable':
                table = 'debian_project_indexes_stable'
            elif self.debianType == 'testing':
                table = 'debian_project_indexes_testing'
            elif self.debianType == 'unstable':
                table = 'debian_project_indexes_unstable'
            select = 'SELECT indexhtml FROM ' + table + ''' 
                WHERE proj_unixname = %s
                AND datasource_id = %s'''
            indexhtml = self.util.execQuery(select, self.projName, self.datasource)[0]
            version = re.search(r'<h1>Package:.*?\((.*?)\)\s*</h1>', indexhtml, re.DOTALL).group(1)
            result = re.search(r'<div id="pdesc"\s*>\s*<h2>(.*?)</h2>\s*<p>(.*?)</div>', indexhtml, re.DOTALL)
            longname = result.group(1)
            description = result.group(2)
            result1 = re.search(r'Homepage: <a href="(.*?)"', description)
            result2 = re.search(r'http://(.*?)"', description)
            result3 = re.search(r'http://(.*?)\s+', description)
            result4 = re.search(r'<a href="(.*?)"', description)
            if (result1):
                homepage = result1.group(1)
            elif (result2):
                homepage = r'http://' + result2.group(1)
            elif (result3):
                homepage = r'http://' + result3.group(1)
            elif (result4):
                homepage = result4.group(1)
            else:
                homepage = ''
            insert = '''INSERT INTO debian_projects
                (proj_unixname,
                datasource_id,
                type,
                proj_longname,
                description,
                descr_homepage,
                parentpath,
                version,
                date_collected)
                VALUES(%s, %s, %s, %s, %s, %s, '', %s, NOW())''' #parentpath no longer in use
            self.util.execQuery(insert, self.projName, self.datasource, self.debianType, longname, description, homepage, version)
        except:
            global isError
            isError = True
            print traceback.format_exc()
            self.util.postError(traceback.format_exc(), self.job_id)
#Runs the main class
Debian_ParseDescriptions()