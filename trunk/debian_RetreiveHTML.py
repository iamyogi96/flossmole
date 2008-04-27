#!/usr/bin/env python
import MySQLdb
import sys
import traceback
import signal
import threading
import urllib2
import re
from debian_Utilities import Debian_Utilities

#Debian URL constants
STABLEURLBASE = 'http://packages.debian.org/stable/'
TESTINGURLBASE = 'http://packages.debian.org/testing/'
UNSTABLEURLBASE = 'http://packages.debian.org/unstable/'

#Class for main routine
class Debian_RetreiveHTML:
    
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
            self.job = self.util.findJob('htmlRetreival')
            if (self.job):
                try:
                    print 'Starting ' + self.job[1]
                    self.parse_Thread = Parse_Thread(self.util, self.job[0], self.job[1], self.job[2], self.job[3])
                    self.parse_Thread.start()
                    self.parse_Thread.join()
                    if isError == False:
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
    
    #Parse routine that populates the html fields in the proper
    #debian_project_indexes_<group> table
    def run(self):
        try:
            if self.debianType == 'stable':
                indexhtml = urllib2.urlopen(STABLEURLBASE + self.projName).read()
            elif self.debianType == 'testing':
                table = 'debian_project_indexes_testing'
                indexhtml = urllib2.urlopen(TESTINGURLBASE + self.projName).read()
            elif self.debianType == 'unstable':
                table = 'debian_project_indexes_unstable'
                indexhtml = urllib2.urlopen(UNSTABLEURLBASE + self.projName).read()
            
            #We only grab this stuff for the stable distribution
            if self.debianType == 'stable':
                clURL = re.search(r'<a href="(.*?)">Debian Changelog</a>', indexhtml).group(1)
                cpURL = re.search(r'<a href="(.*?)">Copyright File</a>', indexhtml).group(1)
                bugURL = r'http://bugs.debian.org/' + self.projName
                devURL = re.search(r'<a href="(.*?)">Developer Information', indexhtml).group(1)
                devhtml = urllib2.urlopen(devURL).read()
                bughtml = urllib2.urlopen(bugURL).read()
                cphtml = urllib2.urlopen(cpURL).read()
                clhtml = urllib2.urlopen(clURL).read()
            
            #This info only exists in the debian_project_indexes_stable table
            if self.debianType == 'stable':
                insert = '''INSERT INTO debian_project_indexes_stable (
                    proj_unixname, 
                    datasource_id, 
                    indexhtml, 
                    bugshtml, 
                    devshtml, 
                    copyrighthtml, 
                    changeloghtml, 
                    date_collected) 
                    VALUES(%s, %s, %s, %s, %s, %s, %s, NOW())'''
                self.util.execQuery(insert, self.projName, self.datasource, indexhtml, bughtml, devhtml, cphtml, clhtml)
            
            #In the other two tables we only grab the index HTML
            else:
                insert = 'INSERT INTO ' + table + ''' (
                    proj_unixname,
                    datasource_id,
                    indexhtml,
                    date_collected)
                    VALUES(%s, %s, %s, NOW())'''
                self.util.execQuery(insert, self.projName, self.datasource, indexhtml)
        except:
            global isError
            isError = True
            self.util.postError(traceback.format_exc(), self.job_id)

#Runs the main class
Debian_RetreiveHTML()
