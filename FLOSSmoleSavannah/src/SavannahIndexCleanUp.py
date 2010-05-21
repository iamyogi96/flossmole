'''
Created on May 2, 2010
This module performs the clean up for index jobs.
@author: StevenNorris
'''

import sys
import traceback

def run(utils,datasource_id):
    
    #Cleans up index jobs
    print("\nStarting index clean up.")
    
    #Gets Job
    job=utils.get_cleanup_job(datasource_id,'indexHTML')
    if(utils.error):
        sys.exit()
    while(job!=None):
        
        #Cleans up for the job
        try:
            unixname=job[0]
            print "Cleaning up for "+unixname
            utils.delete_index(unixname,datasource_id)
            utils.change_status('indexHTML','Clean_Up',datasource_id,unixname)
            job=utils.get_cleanup_job(datasource_id,'indexHTML')
            if(utils.error):
                sys.exit()
                
        #If process fails, post error and get new job
        except:
            print("!!!!WARNING!!!! Clean up indexes for "+unixname+" failed.")
            utils.post_error('Clean_Up(index):\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_cleanup_job(datasource_id,'indexHTML')
            if(utils.error):
                sys.exit()
