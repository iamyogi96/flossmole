'''
Created on May 2, 2010

This module spiders the index page of each job and prepares for skills spidering.

@author: Steven Norris
'''

from HTMLParser import HTMLParser
import re
import time
import sys
import traceback

BASE_SITE1='savannah.gnu.org'
BASE_SITE2='savannah.nongnu.org'

'''
This spider gathers the members list for each projects page
'''
class SpiderSavannahMembersList(HTMLParser):
    
    check_link=''
    
    #handles the start tag for the memberslist link and sets it to check_link
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            link=attrs[0][1]
            if re.search('memberlist.php',link)!=None:
                self.check_link=link

def run(utils,data_source_id):
    
    #Does the index collection jobs for projects
    print("\nGathering indexes")
    spiderMembers=SpiderSavannahMembersList()
    job=utils.get_job(data_source_id,'indexHTML')
    if(utils.error):
        sys.exit()
    while(job!=None):
        try:
            link=job[2]
            type=job[1]
            project_name=job[0]
            print("Gathering data for "+link+".")
            
            #gets the home page for each project
            print("Gathering home page.")
            if(type=='gnu'):
                BASE_SITE=BASE_SITE1
            else:
                BASE_SITE=BASE_SITE2
            print 'http://'+BASE_SITE+link
            page=utils.get_page('http://'+BASE_SITE+link)
            if(page):
                home_page=str(page)
                
                #finds the members page for the project
                print("Gathering members page.")
                spiderMembers.feed(home_page)
                members_page=utils.get_page('http://'+BASE_SITE+spiderMembers.check_link)
                if(page):
                    members_page=str(members_page)
                    
                    #Insert the homepage and members page into sv_project_indexes
                    print("Inserting into sv_project_indexes.")
                    insert='''INSERT INTO sv_project_indexes (
                    project_name,datasource_id,indexhtml,memberhtml,date_collected)
                    VALUES(%s,%s,%s,%s,NOW())'''
                    utils.db_insert(insert,project_name,data_source_id,home_page,members_page)
                    
                    #Insert the type into sv_projects
                    print("Inserting into sv_projects.")
                    insert='''INSERT INTO sv_projects (
                    project_name,datasource_id,gnu_or_non,date_collected)
                    VALUES(%s,%s,%s,NOW())'''
                    utils.db_insert(insert,project_name,data_source_id,type)
                    
                    #sleeps then status change and select new job while checking for fatal errors
                    time.sleep(3)
                    utils.change_status('skillsHTML','indexHTML',data_source_id,project_name)
                    job=utils.get_job(data_source_id,'indexHTML')
                    if (utils.error):
                        sys.exit()
                else:
                    print("!!!!WARNING!!!! Members page either did not exits or failed to collect for "+project_name)
                    utils.post_error(traceback.format_exc(),project_name,data_source_id,type)
                    job=utils.get_job(data_source_id,'indexHTML')
                    if(utils.error):
                        sys.exit()
            else:
                print("!!!!WARNING!!!! Index page either did not exist or failed to collect for "+project_name)
                utils.post_error(traceback.format_exc(),project_name,data_source_id,type)
                job=utils.get_job(data_source_id,'indexHTML')
                if(utils.error):
                    sys.exit()
                    
        #posting error for faulty gathering    
        except:
            print("!!!!WARNING!!!! Index gathering failed for "+project_name+".")
            utils.post_error(traceback.format_exc(),project_name,data_source_id,type)
            job=utils.get_job(data_source_id,'indexHTML')
            if(utils.error):
                sys.exit()
                