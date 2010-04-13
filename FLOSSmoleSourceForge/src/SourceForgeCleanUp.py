'''
Created on Apr 12, 2010
This method is made to clean up the jobs left In_Progress by machine error and prepare them for a second run.
@author: StevenNorris
'''

from SourceForgeUtils import SourceForgeUtils
import sys
import SourceForgeIndexCleanUp
import SourceForgeDevelopmentCleanUp
import SourceForgeDevelopersCleanUp
import SourceForgeResumesCleanUp
import SourceForgeDonorsCleanUp
import SourceForgeMailingListsCleanUp
import SourceForgeMailingListsSpecificCleanUp
import SourceForgeMailingPagesCleanUp
import SourceForge60dayCleanUp
import SourceForgeYearCleanUp


#main method for running clean ups
def main(argv):
    
    #set variables
    try:
        datasource_id=argv[1]
        test=argv[2]
    except:
        print("""RUN INSTRUCTIONS
    Run this module from command line with the following format:
    [Interpreter] SourceForgeCleanUp.py [datasource_id] [Test T/F]
    Test is a string variable. Be sure to use a capital 'T' to denote test mode. 
    Otherwise use 'F'.""")
        sys.exit()
    
    #Checks for test mode
    try:
        if (test=='T'):
            print("TEST MODE ACTIVATED")
            utils=SourceForgeUtils('dbInfoTest.txt')
        else:
            utils=SourceForgeUtils('dbInfo.txt')
    except:
        print("Please create the dbInfo.txt and the dbInfoTest.txt files. See ReadMe for formatting.")
        sys.exit()
        
    #Does the cleanup for the Tigris projects
    SourceForgeIndexCleanUp.run(utils,datasource_id)
    SourceForgeDevelopmentCleanUp.run(utils,datasource_id)
    SourceForgeDevelopersCleanUp.run(utils,datasource_id)
    SourceForgeResumesCleanUp.run(utils,datasource_id)
    SourceForgeDonorsCleanUp.run(utils,datasource_id)
    SourceForgeMailingListsCleanUp.run(utils,datasource_id)
    SourceForgeMailingListsSpecificCleanUp.run(utils,datasource_id)
    SourceForgeMailingPagesCleanUp.run(utils,datasource_id)
    SourceForge60dayCleanUp.run(utils,datasource_id)
    SourceForgeYearCleanUp.run(utils,datasource_id)
    
main(sys.argv)