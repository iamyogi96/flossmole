'''
Created on Aug 16, 2009
This module is designed to populate the jobs database for sourceforge.net.

RUN INSTRUCTIONS
Run this module from command line with the following format:
[Interpreter] SourceForgeJobs.py [datasource_id] [Test T/F]
Test is a string variable. Be sure to use a capital 'T' to denote test mode. 
Otherwise use 'F'.

@author: StevenNorris
'''

import sys
from SourceForgeUtils import SourceForgeUtils
import traceback

#adds the jobs to the sf_jobs table in the selected database
def main(argv):
    
    #set variables
    try:
        datasource_id=argv[1]
        test=argv[2]
    except:
        print ("""RUN INSTRUCTIONS\n
        Run this module from command line with the following format:\n
        [Interpreter] SourceForgeJobs.py [datasource_id] [Test T/F]\n
        Test is a string variable. Be sure to use a capital 'T' to denote test mode.\n 
        Otherwise use 'F'.""")
        sys.exit()
    
    #checks for test mode
    if(test=='T'):
        print("TEST MODE ACTIVATED")
        utils=SourceForgeUtils('dbInfoTest.txt')
        #gathering project unixnames and adding jobs to database
        try:
            print("Gathering unixnames.")
            projects_list=utils.get_projects(datasource_id)
            try:
                print("Creating Jobs")
                for project in projects_list[0:50]:
                    project=project[0]
                    print("Creating job for "+project)
                    try:
                        insert='''INSERT INTO sf_jobs (unixname,datasource_id,status,last_modified)
                        VALUES(%s,%s,'gather_index',NOW())'''
                        utils.db_insert(insert,project,datasource_id)
                    except:
                        print('!!!!WARNING!!!! Job creation failed for '+project+'.')
                        print(traceback.format_exc())
            except:
                print('!!!!WARNING!!!! Jobs did not create succesfully')
                print(traceback.format_exc())
        except:
            print('!!!!WARNING!!!! Projects unixnames not collected properly.')
            print(traceback.format_exc())
    
    else:
        utils=SourceForgeUtils('dbInfo.txt')
        #gathering project unixnames and adding jobs to database
        try:
            print("Gathering unixnames.")
            projects_list=utils.get_projects(datasource_id)
            print (projects_list)
            try:
                print("Creating Jobs")
                for project in projects_list[0:10]:
                    print("Creating job for "+project)
                    try:
                        insert='''INSERT INTO sf_jobs (unixname,datasource_id,status,last_modified)
                        VALUES(%s,%s,'gather_index',NOW())'''
                        utils.db_insert(insert,project,datasource_id)
                    except:
                        print('!!!!WARNING!!!! Job creation failed for '+project+'.')
                        print(traceback.format_exc())
            except:
                print('!!!!WARNING!!!! Jobs did not create succesfully')
                print(traceback.format_exc())
        except:
            print('!!!!WARNING!!!! Projects unixnames not collected properly.')
            print(traceback.format_exc())
            

    
main(sys.argv)