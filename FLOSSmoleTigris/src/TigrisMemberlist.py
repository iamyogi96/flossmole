'''
Created on Feb 21, 2010

This module spiders the memberlist pages for each project in the job database.

@author: Steven Norris
'''

import sys
import traceback
import time

#runs spidering for the memberlists
def run(utils,datasource_id):
    
    #Gathers Index Pages
    print("Gathering Memberlist Pages")
    
    #Gets Job
    job=utils.get_job(datasource_id,'gather_memberlist')
    if(utils.error):
        sys.exit()
    while(job!=None):
        time.sleep(3)
        
        #Gathers index page
        try:
            unixname=job[0]
            print "Gathering Memberlist Page for "+unixname
            memberlist=utils.get_page("http://"+unixname+".tigris.org/servlets/ProjectMemberList?mode=All&itemsPerPage=1000000")
            
            #inserts index page and gets new job
            if(memberlist):
                print("Inserting Into Database")
                update="""UPDATE tg_project_indexes SET memberlisthtml=%s, last_modified=NOW()
                WHERE datasource_id=%s AND unixname=%s"""
                utils.db_insert(update,memberlist,datasource_id,unixname)
                
                #changes status, gets new job, and checks for errors
                utils.change_status('gather_discussions',datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_memberlist')
                if (utils.error):
                    sys.exit()
            
            #if index page is not found, posts error and gets new job
            else:
                print "!!!!WARNING!!!! Memberlist Gathering Failed for "+unixname
                utils.post_error('gather_memberlist: \nMemberlist did not exist.' ,datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_memberlist')
                if(utils.error):
                    sys.exit()
                    
        #if collection fails entirely, posts error and gets new job
        except:
            print("!!!!WARNING!!! Memberlist collection failed")
            utils.post_error('gather_memberlist:\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_memberlist')
            if(utils.error):
                sys.exit()
