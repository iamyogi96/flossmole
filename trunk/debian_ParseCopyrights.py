#!/usr/bin/env python
import MySQLdb
import sys
import traceback
import signal
import threading
import re
from debian_Utilities import Debian_Utilities

#Global variables (not sure if we need this)
#isError = False

#Class for main routine
class Debian_ParseCopyrights:
    
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
            self.job = self.util.findJob('copyrightParse')
            if (self.job):
                try:
                    print 'Starting ' + self.job[1]
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
    def __init__(self, util, job_id, projName, debianType, dataSource):
        threading.Thread.__init__(self)
        self.util = util
        self.job_id = job_id
        self.projName = projName
        self.debianType = debianType
        self.datasource = dataSource

    #Parse routine that finds the homepage URLs in the copyright HTML and inserts
    #it in the copyright table
    def run(self):
        try:
            select = '''SELECT copyrighthtml
                FROM debian_project_indexes_stable
                WHERE proj_unixname = %s
                AND datasource_id = %s'''
            cphtml = self.util.execQuery(select, self.projName, self.datasource)[0]
        
            result1 = re.search(r'http://(.*?)>', cphtml)
            result2 = re.search(r'http://(.*?)<', cphtml)
            result3 = re.search(r'http://(.*?)\)', cphtml)
            result4 = re.search(r'http://(.*?),', cphtml)
            result5 = re.search(r'http://(.*?)"', cphtml)
            result6 = re.search(r'http://(.*?)\'', cphtml)
            result7 = re.search(r'http://(.*?)/\.', cphtml)
            result8 = re.search(r'http://(.*?).$', cphtml)
            result9 = re.search(r'http://(.*?);', cphtml)
            result10 = re.search(r'http://(.*?)\s+', cphtml)
            result11 = re.search(r'http://(.*?)$', cphtml)
            if (result1):
                homepage = 'http://' + result1.group(1)
            elif (result2):
                homepage = 'http://' + result2.group(1)
            elif (result3):
                homepage = 'http://' + result3.group(1)
            elif (result4):
                homepage = 'http://' + result4.group(1)
            elif (result5):
                homepage = 'http://' + result5.group(1)
            elif (result6):
                homepage = 'http://' + result6.group(1)
            elif (result7):
                homepage = 'http://' + result7.group(1)
            elif (result8):
                homepage = 'http://' + result8.group(1)
            elif (result9):
                homepage = 'http://' + result9.group(1)
            elif (result10):
                homepage = 'http://' + result10.group(1)
            elif (result11):
                homepage = 'http://' + result11.group(1)
            else:
                homepage = ''
            homepage = homepage.rstrip(' ,)><\'";')
        
            insert = """INSERT INTO debian_copyright_urls( 
                proj_unixname, 
                datasource_id, 
                url, 
                date_collected) 
                VALUES(%s, %s, %s, NOW())"""
            self.util.execQuery(insert, self.projName, self.datasource, homepage)
        except:
            global isError
            isError = True
            self.util.postError(traceback.format_exc(), self.job_id)
#Runs the main class
Debian_ParseCopyrights()