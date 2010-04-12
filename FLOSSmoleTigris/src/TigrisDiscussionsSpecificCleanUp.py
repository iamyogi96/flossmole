'''
Created on Mar 29, 2010
This module performs the clean up for gather_discussions_specific jobs.
@author: StevenNorris
'''

import sys
import traceback

def run(utils,datasource_id):
    
    #Cleans up gather_index jobs
    print("\nStarting discussions specific clean up.")
    
    #Gets Job
    job=utils.get_cleanup_job(datasource_id,'gather_discussions_specific')
    if(utils.error):
        sys.exit()
    while(job!=None):
        
        #Cleans up for the job
        try:
            unixname=job[0]
            print "Cleaning up for "+unixname
            utils.delete_discussions_specific(unixname,datasource_id)
            utils.change_status('gather_discussions_specific','Clean_Up',datasource_id,unixname)
            job=utils.get_cleanup_job(datasource_id,'gather_discussions_specific')
            if(utils.error):
                sys.exit()
                
        #If process fails, post error and get new job
        except:
            print("!!!!WARNING!!!! Clean up discussions specific for "+unixname+" failed.")
            utils.post_error('Clean_Up(dicsussions_specific):\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_cleanup_job(datasource_id,'gather_discussions_specific')
            if(utils.error):
                sys.exit()
