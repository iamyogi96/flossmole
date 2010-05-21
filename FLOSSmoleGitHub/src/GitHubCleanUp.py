'''
Created on May 21, 2010

Cleans up projects stuck in In_Progress for GitHub

@author: StevenNorris
'''

import sys
from GitHubutils import GitHubutils
import traceback

def main(argv):
    
    try:
        datasource_id=argv[1]
        test=argv[2]
    except:
        print("Format arguments thusly: [program] [datasource_id] [True/False(TestMode)]")
        sys.exit()
       
    try:
        #checks for test mode
        if(test=='True'):
            print('TEST MODE ACTIVATED')
            utils=GitHubutils("dbInfoTest.txt")
        else:
            utils=GitHubutils("dbInfo.txt")
    except:
        print("Please create the dbInfo.txt and dbInfoTest.txt files. Check ReadMe for formatting.")
        sys.exit()
        
    print("Cleaning up XMLgathering")
    job=utils.get_cleanup_job(datasource_id, 'XMLgathering')
    if(utils.error):
        sys.exit()
    while(job!=None):
        
        #cleans up for each project
        try:
            project_name=job[0]
            developer_name=job[1]
            print('Cleaning up for '+project_name+' by '+developer_name)
            utils.delete_project(datasource_id,project_name,developer_name)
            utils.change_status('XMLgathering','Clean_Up', datasource_id, project_name, developer_name)
            job=utils.get_cleanup_job(datasource_id, 'XMLgathering')
            if(utils.error):
                sys.exit()
                
        #if clean up fails
        except:
            print("!!!!WARNING!!!! Clean up failed")
            utils.post_error('CleanUp(XMLgathering): \n'+traceback.format_exc(), datasource_id, project_name, developer_name)
            job=utils.get_cleanup_job(datasource_id, 'XMLgathering')
            if(utils.error):
                sys.exit()
                
    print("Cleaning up Parsing")
    job=utils.get_cleanup_job(datasource_id, 'Parsing')
    if(utils.error):
        sys.exit()
    while(job!=None):
        
        #cleans up for each project
        try:
            project_name=job[0]
            developer_name=job[1]
            print('Cleaning up for '+project_name+' by '+developer_name)
            utils.change_status('Parsing','Clean_Up', datasource_id, project_name, developer_name)
            job=utils.get_cleanup_job(datasource_id, 'Parsing')
            if(utils.error):
                sys.exit()
                
        #if clean up fails
        except:
            print("!!!!WARNING!!!! Clean up failed")
            utils.post_error('CleanUp(Parsing): \n'+traceback.format_exc(), datasource_id, project_name, developer_name)
            job=utils.get_cleanup_job(datasource_id, 'Parsing')
            if(utils.error):
                sys.exit()
            
            
main(sys.argv)