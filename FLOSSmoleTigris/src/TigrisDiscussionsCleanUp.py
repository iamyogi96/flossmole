'''
Created on Mar 29, 2010
This module performs the clean up for gather_discussions jobs.
@author: StevenNorris
'''

import sys
import traceback

def run(utils,datasource_id):
    
    #Cleans up gather_index jobs
    print("\nStarting discussions clean up.")
    
    #Gets Job
    job=utils.get_cleanup_job(datasource_id,'gather_discussions')
    if(utils.error):
        sys.exit()
    while(job!=None):
        
        #Cleans up for the job
        try:
            unixname=job[0]
            print "Cleaning up for "+unixname
            utils.delete_discussions(unixname,datasource_id)
            utils.change_status('gather_discussions','Clean_Up',datasource_id,unixname)
            job=utils.get_cleanup_job(datasource_id,'gather_discussions')
            if(utils.error):
                sys.exit()
                
        #If process fails, post error and get new job
        except:
            print("!!!!WARNING!!!! Clean up dicsussions for "+unixname+" failed.")
            utils.post_error('Clean_Up(dicsussions):\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_cleanup_job(datasource_id,'gather_discussions')
            if(utils.error):
                sys.exit()
