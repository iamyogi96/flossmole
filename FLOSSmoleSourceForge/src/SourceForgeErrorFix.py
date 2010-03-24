'''
Created on Oct 14, 2009

This module is used after an initial run to rerun any timed out errors.

@author: Steven Norris
'''
from SourceForgeUtils import SourceForgeUtils
import sys
import SourceForge60day
import SourceForgeYear


#!!!!WARNING!!!!! Running this error fix will only collect 60day stats and year stats that have timed out.
# To complete the process for these projects please rerun the SourceForgeSpider for the datasource_id.

def main(argv):
    
    try:
        datasource_id=argv[1]
        test=argv[2]
    except:
        print("""RUN INSTRUCTIONS
        Run this module from command line with the following format:
        [Interpreter] SourceForgeJobs.py [datasource_id] [Test T/F]
        Test is a string variable. Be sure to use a capital 'T' to denote test mode. 
        Otherwise use 'F'.""") 
        sys.exit()
    
    #Checks for test mode
    if (test=='T'):
        print("TEST MODE ACTIVATED")
        utils=SourceForgeUtils('dbInfoTest.txt')
    else:
        utils=SourceForgeUtils('dbInfo.txt')
    
    print('Running Error Fixes')
    
    #runs jobs to prepare for reruns
    job=utils.get_job(datasource_id,'error_60day')
    while(job!=None):
        unixname=job[0]
        utils.change_status('gather_60day','error_60day',datasource_id,unixname)
        job=utils.get_job(datasource_id,'error_60day')
        if(utils.error):
            sys.exit()
    
    SourceForge60day.run(utils,datasource_id)
    
    job=utils.get_job(datasource_id,'error_year')
    while(job!=None):
        unixname=job[0]
        utils.change_status('gather_year','error_year',datasource_id,unixname)
        job=utils.get_job(datasource_id,'error_year')
        if(utils.error):
            sys.exit()
    
    SourceForgeYear.run(utils,datasource_id)
    
main(sys.argv)
        