'''
Created on May 2, 2010
This module performs the clean up for parsing jobs.
@author: StevenNorris
'''

import sys
import traceback

def run(utils,datasource_id):
    
    #Cleans up parsing jobs
    print("\nStarting parsing clean up.")
    
    #Gets jobs for indexParsing
    print("\nIndex parsing clean up.")
    job=utils.get_cleanup_job(datasource_id,'indexparsing')
    if(utils.error):
        sys.exit()
    while(job!=None):
        
        #Cleans up for the job
        try:
            unixname=job[0]
            print "Cleaning up for "+unixname
            utils.change_status('indexparsing','Clean_Up',datasource_id,unixname)
            job=utils.get_cleanup_job(datasource_id,'indexparsing')
            if(utils.error):
                sys.exit()
                
        #If process fails, post error and get new job
        except:
            print("!!!!WARNING!!!! Clean up skills for "+unixname+" failed.")
            utils.post_error('Clean_Up(indexParsing):\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_cleanup_job(datasource_id,'indexparsing')
            if(utils.error):
                sys.exit()
    
    #Gets jobs for skillsParsing   
    print("\nSkills parsing clean up.")      
    job=utils.get_cleanup_job(datasource_id,'skillsparsing')
    if(utils.error):
        sys.exit()
    while(job!=None):
        
        #Cleans up for the job
        try:
            unixname=job[0]
            print "Cleaning up for "+unixname
            utils.change_status('skillsparsing','Clean_Up',datasource_id,unixname)
            job=utils.get_cleanup_job(datasource_id,'skillsparsing')
            if(utils.error):
                sys.exit()
                
        #If process fails, post error and get new job
        except:
            print("!!!!WARNING!!!! Clean up skills for "+unixname+" failed.")
            utils.post_error('Clean_Up(indexParsing):\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_cleanup_job(datasource_id,'skillsparsing')
            if(utils.error):
                sys.exit()


