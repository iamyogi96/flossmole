'''
Created on Sep 28, 2009

This module spiders the developers page for each project and prepares for 60 day stats spidering.

@author: Steven Norris
'''

import re
import sys
import traceback
import time

BASE_INDEX='sourceforge.net/projects/'
BASE_SITE='sourceforge.net/'

#This spider finds the memberlist link on the development page    
def memberlistSpider(page):
    match=re.search('project/memberlist\.php.+?"',page)
    if(match!=None):
        link=match.group(0)
        link=link[0:len(link)-1]
        return link
    else:
        return None

def run(utils,datasource_id):
    
    #collects the memberlist pages for each job and adds them to project_indexes
    print("\nGathering memberlist pages.")
    
    #runs jobs
    job=utils.get_job(datasource_id,'gather_memberlist')
    if(utils.error):
        sys.exit()
    while(job!=None):
        time.sleep(3)
        try:
            unixname=job[0]
            print("\nGathering for "+unixname)
            
            #collects development page and crawls for memberlist link
            print("Retrieving development HTML.")
            dev_page=utils.get_development(datasource_id,unixname)
            if(dev_page):
                dev_page=dev_page[0]
                print("Finding link.")
                link=memberlistSpider(dev_page)
                
                #inserts memberlist page into project_indexes
                if(link):
                    print("Inserting memberlist page.")
                    memberlist=utils.get_page("http://"+BASE_SITE+link)
                else:
                    print("Link was not found.")
                    memberlist=None
                    
                if(memberlist and re.search('We apologize.  The page you were looking for cannot be found.',memberlist)==None):
                    update="UPDATE project_indexes SET developers_html=%s WHERE datasource_id=%s AND proj_unixname=%s"
                    utils.db_insert(update,memberlist,datasource_id,unixname)
                    utils.change_status('gather_resumes','gahter_memberlist',datasource_id,unixname)
                    #change gather_60day
                    job=utils.get_job(datasource_id,'gather_memberlist')
                    if(utils.error):
                        sys.exit()
                        
                #if memberlist insertion fails posts error, gets job, and checks for errors
                else:
                    print("!!!!WARNING!!!! Memberlist page did not collect correctly.")
                    utils.post_error('gather_memberlist:\nMemberlist page either did not exist or led to a faulty page.',datasource_id,unixname)
                    job=utils.get_job(datasource_id,'gather_memberlist')
                    if(utils.error):
                        sys.exit()
            
            #if development doesn't collect properly posts error, gets job, and checks for errors
            else:
                print("!!!!WARNING!!!! Memberlist page did not collect correctly.")
                utils.post_error('gather_memberlist:\nDevelopment gathering yielded a null response.',datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_memberlist')
                if(utils.error):
                    sys.exit()
        
        #if collecting process fails posts error, gets job, and checks for errors
        except:
            print("!!!!WARNING!!!! Memberlist page did not collect correctly.")
            utils.post_error('gather_memberlist:\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_memberlist')
            if(utils.error):
                sys.exit()   
