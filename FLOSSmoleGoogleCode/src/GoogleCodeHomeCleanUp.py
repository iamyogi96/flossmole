'''
Created on Apr 12, 2010
This module performs the clean up for gather_home jobs.
@author: StevenNorris
'''

import sys
import traceback

def run(utils,datasource_id):
    
    #Cleans up gather_home jobs
    print("\nStarting home clean up.")
    
    #Gets Job
    job=utils.get_cleanup_job(datasource_id,'gather_home')
    if(utils.error):
        sys.exit()
    while(job!=None):
        
        #Cleans up for the job
        try:
            unixname=job[0]
            print "Cleaning up for "+unixname
            utils.delete_home(unixname,datasource_id)
            utils.change_status('gather_home','Clean_Up',datasource_id,unixname)
            job=utils.get_cleanup_job(datasource_id,'gather_home')
            if(utils.error):
                sys.exit()
                
        #If process fails, post error and get new job
        except:
            print("!!!!WARNING!!!! Clean up home for "+unixname+" failed.")
            utils.post_error('Clean_Up(home):\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_cleanup_job(datasource_id,'gather_home')
            if(utils.error):
                sys.exit()

