#!/usr/bin/env python

#This script will fill the job queue with the desired set of Debian projects
#for parsing.

import MySQLdb
import urllib2
import sys
import re
from optparse import OptionParser
from debian_Utilities import Debian_Utilities

STABLEPACKAGESURL = "http://packages.debian.org/stable/allpackages"
TESTINGPACKAGESURL = "http://packages.debian.org/testing/allpackages"
UNSTABLEPACKAGESURL = "http://packages.debian.org/unstable/allpackages"
DBFILENAME = "dbInfo.txt"

class Debian_MakeJobs:
    
    #Main routine
    def __init__(self):
        self.util = Debian_Utilities()
        parser = OptionParser()
        parser.add_option('-g', '--group', action='store', type='string', dest='GROUP')
        parser.add_option('-d', '--datasource', action='store', type='int', dest='DATASOURCE')
        parser.set_default('DATASOURCE', '0')
        parser.set_default('GROUP', 'all')
        (options, args) = parser.parse_args()
        
        if options.GROUP != 'all':
            for project in self.getProjectGroup(options.GROUP):
                self.createJob(self.util, project, options.GROUP, options.DATASOURCE)
        else:
            for project in self.getProjectGroup('stable'):
                self.createJob(self.util, project, 'stable', options.DATASOURCE)
            for project in self.getProjectGroup('testing'):
                self.createJob(self.util, project, 'testing', options.DATASOURCE)
            for project in self.getProjectGroup('unstable'):
                self.createJob(self.util, project, 'unstable', options.DATASOURCE)

    #Returns the list of projects of type "type" where each project is a tuple of
    #the form (project name, project version, project description)
    def getProjectGroup(self, type):
        try:
            if type == 'stable':
                html = urllib2.urlopen(STABLEPACKAGESURL).read()
            elif type == 'testing':
                html = urllib2.urlopen(TESTINGPACKAGESURL).read()
            elif type == 'unstable':
                html = urllib2.urlopen(UNSTABLEPACKAGESURL).read() 
        except:
            print 'Error retreiving ' + type + ' project page HTML - exiting'
            sys.exit()
        
        try:
            projects = re.finditer(r"<dt><a href='(.*?)'\s+id='.*?'>.*?</a>\s+\((.*?)\)\s*</dt>\s*<dd>(.*?)</dd>", html)
        except:
            print 'String matching error when retreiving ' + type + ' projects - exiting'
            sys.exit()
        projectList = []
        for project in projects:
            #Tuple: (projectname, version, description)
            projectList.append((project.group(1), project.group(2), project.group(3)))
        return projectList

    #Creates the jobs for a specific project
    def createJob(self, util, project, deb_type, dataSourceID):
        insert = '''INSERT INTO debian_jobs(
            proj_name,
            debian_type,
            job_type,
            status,
            datasource_id,
            last_modified)
            VALUES(%s, %s, %s, %s, %s, NOW())'''
        
        try:
            util.execQuery(insert, project[0], deb_type, 'htmlRetreival', 'pending', dataSourceID)
            util.execQuery(insert, project[0], deb_type, 'descParse', 'pending', dataSourceID)
            if deb_type == 'stable':
                util.execQuery(insert, project[0], deb_type, 'devParse', 'pending', dataSourceID)
                util.execQuery(insert, project[0], deb_type, 'copyrightParse', 'pending', dataSourceID)
        except:
            print 'Error creating jobs for project ' + project[0]

#Runs the main class
Debian_MakeJobs()
