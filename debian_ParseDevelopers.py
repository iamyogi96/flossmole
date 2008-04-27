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
class Debian_ParseDevelopers:
    
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
            self.job = self.util.findJob('devParse')
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
    
    #Parse routine that populates the developers table
    def run(self):
        try:
            select = '''SELECT devshtml
                FROM debian_project_indexes_stable
                WHERE proj_unixname = %s
                AND datasource_id = %s'''
            devhtml = self.util.execQuery(select, self.projName, self.datasource)[0]
            
            result = re.search(r'<td class="labelcell">Maintainer</td>\s*<td class="contentcell">\s*<a href="(.*?)">(.*?)</a>\s*<a class="email" href="mailto:(.*?)">', devhtml, re.DOTALL)
            url = result.group(1)
            name = result.group(2)
            email = result.group(3)
            insert = """INSERT INTO debian_project_developers( 
                proj_unixname, 
                datasource_id, 
                name, 
                email, 
                url, 
                role, 
                date_collected) 
                VALUES(%s, %s, %s, %s, %s, 'Maintainer', NOW())"""
            self.util.execQuery(insert, self.projName, self.datasource, name, email, url)
            
            result = re.search(r'Co-Maintainers</a></td>\s*<td class="contentcell">(.*?)</td>', devhtml)
            if (result):
                comaintlist = result.group(1)
                comaints = str.split(r'<br>', comaintlist)
                for comaint in comaints:
                    result = re.search(r'<a href="(.*?)">(.*?)</a>\s*[<a class="email" href="mailto:(.*?)>mail</a>]', comaint)
                    if (result):
                        url = result.group(1)
                        name = result.group(2)
                        email = result.group(3)
                        insert = """INSERT INTO debian_project_developers( 
                            proj_unixname, 
                            datasource_id, 
                            name, 
                            email, 
                            url, 
                            role, 
                            date_collected) 
                            VALUES(%s, %s, %s, %s, %s, 'Co-Maintainer', NOW())"""
                        self.util.execQuery(insert, self.projName, self.datasource, name, email, url)
        except:
            global isError
            isError = True
            self.util.postError(traceback.format_exc(), self.job_id)
#Runs the main class
Debian_ParseDevelopers()