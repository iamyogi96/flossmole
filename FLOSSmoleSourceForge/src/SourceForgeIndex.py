'''
Created on Sep 28, 2009

This module spiders the index page of each job and prepares for development spidering.

@author: Steven Norris
'''

import re
import sys
import traceback
import time

BASE_INDEX='sourceforge.net/projects/'
BASE_SITE='sourceforge.net/'

def run(utils,datasource_id,stage):
    #Gathers index pages
    print("Gathering index pages")
    if(stage==0):
        stage='completed'
    elif(stage==1):
        stage='gather_development'
    else:
        stage='gather_donors'
    #runs jobs
    job=utils.get_job(datasource_id,'gather_index')
    if(utils.error):
        sys.exit()
    while(job!=None):
        time.sleep(3)
        try:
            unixname=job[0]
            print("Gathering index for "+unixname)
            index=utils.get_page("http://"+BASE_INDEX+unixname)
            
            if(index and re.search('We apologize.  The page you were looking for cannot be found.',index)==None):
                insert="""INSERT INTO sf_project_indexes (proj_unixname,indexhtml,date_collected,datasource_id)
                VALUES(%s,%s,NOW(),%s)"""
                utils.db_insert(insert,unixname,index,datasource_id)
                
                #changes status, gets new job, and checks for errors
                utils.change_status(stage,'gather_index',datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_index')
                if (utils.error):
                    sys.exit()
            
            #if page does not collect properly, posts error, gets new job, and checks for errors
            else:
                print("!!!!WARNING!!!! Index gathering failed for "+unixname)
                utils.post_error('gather_index: \nIndex either did not exist or led to faulty page.' ,datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_index')
                if(utils.error):
                    sys.exit()
         
        #if index process fails, posts error, gets new job, and checks for errors   
        except:
            print("!!!!WARNING!!! Index collection failed")
            utils.post_error('gather_index:\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_index')
            if(utils.error):
                sys.exit()
    
