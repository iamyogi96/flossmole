'''
Created on Jun 9, 2009

@author: Steven Norris

This module runs the jobs from github.com.

RUN INSTRUCTIONS
Run from command line using this format
[Interpret] GitHubSpider.py [DatasourceID] [Test mode True/False]

Test mode is based on string comparison so make sure capitalization and spelling are exact.
'''

from GitHubutils import GitHubutils
from HTMLParser import HTMLParser
import httplib
import re
import time
import MySQLdb
import traceback
import sys
import GitHubParsers

BASE_SITE='github.com'


def main(argv):
    XML_projects_pages="http://github.com/api/v2/xml/repos/show/"
    
    try:
        datasource_id=argv[1]
        test=argv[2]
    except:
       print("Format arguments thusly: [program] [datasource_id] [True/False(TestMode)]")
       sys.exit()
       
    try:
        #checks for test mode
        if(test=='True'):
            print('TEST MODE ACTIVATED')
            utils=GitHubutils("dbInfoTest.txt")
        else:
            utils=GitHubutils("dbInfo.txt")
    except:
        print("Please create the dbInfo.txt and dbInfoTest.txt files. Check ReadMe for formatting.")
        sys.exit()
        
    #collects the xml for each project
    
    print("Gathering XML.")
    job=utils.get_job(datasource_id,'XMLgathering')
    if(utils.error):
        sys.exit()
    while(job):
        try:
            project_name=job[0]
            developer_name=job[1]
            print('Collecting for '+project_name+' and '+developer_name+'.')
            XML_page=utils.get_page(XML_projects_pages+developer_name+'/'+project_name)
            
            #if project exists
            if(XML_page):
                XML_page=str(XML_page)
                insert='''INSERT INTO gh_projects (datasource_id,project_name,developer_name,XML,last_modified)
                VALUES(%s,%s,%s,%s,NOW())'''
                utils.db_insert(insert,datasource_id,project_name,developer_name,XML_page)
            
            #if project does not exist
            else:
                insert='''INSERT INTO gh_projects (datasource_id,projects_name, developer_name,XML,last_modified)
                VALUES (%s,%s,%s,NULL,NOW())'''
                utils.db_insert(insert,datasource_id,project_name,developer_name)
            
            #sleeps, checks for errors, and gets new job
            time.sleep(2)
            utils.change_status('Parsing',datasource_id,project_name,developer_name)
            job=utils.get_job(datasource_id,'XMLgathering')
            if(utils.error):
                sys.exit()
        
        #if failure occurs, posts an error and finds a new job 
        except:
            print("!!!!WARNING!!!! gathering has failed.")
            utils.post_error(traceback.format_exc(),datasource_id,project_name,developer_name)
            job=utils.get_job(datasource_id,'XMLgathering')
            if(utils.error):
                sys.exit()
        
    #does parsing for all parsing jobs            
    print("\nParsing")
    job=utils.get_job(datasource_id,'Parsing')
    if(utils.error):
        sys.exit()
    while(job):
        try:
            
            #runs parsers
            print('Parsing for '+job[0]+' by '+job[1])
            xml=utils.gather_xml(job[0],job[1],datasource_id)
            description=GitHubParsers.parse_description(xml)
            private=GitHubParsers.parse_private(xml)
            url=GitHubParsers.parse_url(xml)
            forks=GitHubParsers.parse_forks(xml)
            forked=forks[0]
            fork_number=forks[1]
            homepage=GitHubParsers.parse_home(xml)
            watchers=GitHubParsers.parse_watch(xml)
            open_issues=GitHubParsers.parse_issues(xml)
            
            #inserts into database
            update='''UPDATE gh_projects
            SET description=%s,
            private=%s,
            url=%s,
            forked=%s,
            fork_number=%s,
            homepage=%s,
            watchers=%s,
            open_issues=%s,
            last_modified=NOW()
            WHERE datasource_id=%s
            AND project_name=%s
            AND developer_name=%s'''
            utils.db_insert(update,description,private,url,forked,fork_number,homepage,
                            watchers,open_issues,datasource_id,job[0],job[1])  
            
            #changes status, checks for errors, and gets new job   
            utils.change_status('Completed',datasource_id,job[0],job[1])
            job=utils.get_job(datasource_id,'Parsing')
            if(utils.error):
                sys.exit()  
                
        #if failure occurs, posts error and finds new job     
        except:
            print("!!!!WARNING!!!! parsing has failed.")
            utils.post_error(traceback.format_exc(),datasource_id,job[0],job[1])
            job=utils.get_job(datasource_id,'Parsing')
            if(utils.error):
                sys.exit()
    
main(sys.argv)

