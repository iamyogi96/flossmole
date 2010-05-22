'''
Created on Feb 21, 2010

This module spiders the index pages for each project in the job database.

@author: Steven Norris
'''

import sys
import traceback
import time

#runs spidering for the indexes
def run(utils,datasource_id):
    
    #Gathers Index Pages
    print("Gathering Index Pages")
    
    #Gets Job
    job=utils.get_job(datasource_id,'gather_index')
    if(utils.error):
        sys.exit()
    while(job!=None):
        time.sleep(3)
        
        #Gathers index page
        try:
            unixname=job[0]
            print "Gathering Index Page for "+unixname
            index=utils.get_page("http://"+unixname+".tigris.org")
            
            #inserts index page and gets new job
            if(index):
                print("Inserting Into Database")
                insert1="""INSERT INTO tg_projects (unixname,datasource_id,last_modified,url)
                VALUES(%s,%s,NOW(),%s)"""
                utils.db_insert(insert1,unixname,datasource_id,"http://"+unixname+".tigris.org")
                insert2="""INSERT INTO tg_project_indexes (unixname,indexhtml,last_modified,datasource_id)
                VALUES(%s,%s,NOW(),%s)"""
                utils.db_insert(insert2,unixname,index,datasource_id)
                
                #changes status, gets new job, and checks for errors
                utils.change_status('gather_memberlist','gather_index',datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_index')
                if (utils.error):
                    sys.exit()
            
            #if index page is not found, posts error and gets new job
            else:
                print "!!!!WARNING!!!! Index Gathering Failed for "+unixname
                utils.post_error('gather_index: \nIndex either did not exist or led to faulty page.' ,datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_index')
                if(utils.error):
                    sys.exit()
                    
        #if collection fails entirely, posts error and gets new job
        except:
            print("!!!!WARNING!!! Index collection failed")
            utils.post_error('gather_index:\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_index')
            if(utils.error):
                sys.exit()