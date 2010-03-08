'''
Created on Feb 21, 2010

This module spiders the discussion pages for each project in the job database.

@author: Steven Norris
'''

import sys
import traceback
import time
import re

#runs the main spidering for the dicussions
def run(utils,datasource_id):
    
    #Gathers Discussions Pages
    print("Gathering Discussion Pages")
    
    #Gets Job
    job=utils.get_job(datasource_id,'gather_discussions')
    if(utils.error):
        sys.exit()
    while(job!=None):
        time.sleep(3)
        
        #Gathers discussions page
        try:
            unixname=job[0]
            print "Gathering Discussions Page for "+unixname
            discussions=utils.get_page("http://"+unixname+".tigris.org/ds/viewForums.do")
            
            #inserts discussions page and gets new job
            if(discussions and re.search("No discussions available to view",discussions)==None):
                print("Inserting Into Database")
                update="""UPDATE tg_project_indexes SET discussionshtml=%s, last_modified=NOW()
                WHERE datasource_id=%s AND unixname=%s"""
                utils.db_insert(update,discussions,datasource_id,unixname)
                
                #changes status, gets new job, and checks for errors
                utils.change_status('gather_discussions_specific',datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_discussions')
                if (utils.error):
                    sys.exit()
            
            #if discussions page is not found, posts error and gets new job
            else:
                print "!!!!WARNING!!!! Discussions Page either did not exist or failed to collect for "+unixname
                utils.change_status('gather_discussions_specific',datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_discussions')
                if(utils.error):
                    sys.exit()
                    
        #if collection fails entirely, posts error and gets new job
        except:
            print("!!!!WARNING!!! Discussions collection failed")
            utils.post_error('gather_discussions:\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_discussions')
            if(utils.error):
                sys.exit()
