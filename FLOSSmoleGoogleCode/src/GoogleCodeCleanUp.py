'''
Created on Apr 12, 2010
This method is made to clean up the jobs left In_Progress by machine error and prepare them for a second run.
@author: StevenNorris
'''

from GoogleCodeUtils import GoogleCodeUtils
import sys
import GoogleCodeHomeCleanUp
import GoogleCodeUpdatesCleanUp
import GoogleCodePeopleCleanUp
import GoogleCodeDownloadsCleanUp
import GoogleCodeIssuesCleanUp
import GoogleCodeWikiCleanUp
import GoogleCodePeopleSpecificCleanUp
import GoogleCodeIssuesSpecificCleanUp



#main method for running clean ups
def main(argv):
    
    #set variables
    try:
        datasource_id=argv[1]
        test=argv[2]
    except:
        print("""RUN INSTRUCTIONS
    Run this module from command line with the following format:
    [Interpreter] GoogleCodeCleanUp.py [datasource_id] [Test T/F]
    Test is a string variable. Be sure to use a capital 'T' to denote test mode. 
    Otherwise use 'F'.""")
        sys.exit()
    
    #Checks for test mode
    try:
        if (test=='T'):
            print("TEST MODE ACTIVATED")
            utils=GoogleCodeUtils('dbInfoTest.txt')
        else:
            utils=GoogleCodeUtils('dbInfo.txt')
    except:
        print("Please create the dbInfo.txt and the dbInfoTest.txt files. See ReadMe for formatting.")
        sys.exit()
        
    #Does the cleanup for the GoogleCode projects
    GoogleCodeHomeCleanUp.run(utils,datasource_id)
    GoogleCodeUpdatesCleanUp.run(utils,datasource_id)
    GoogleCodePeopleCleanUp.run(utils,datasource_id)
    GoogleCodeDownloadsCleanUp.run(utils,datasource_id)
    GoogleCodeIssuesCleanUp.run(utils,datasource_id)
    GoogleCodeWikiCleanUp.run(utils,datasource_id)
    GoogleCodePeopleSpecificCleanUp.run(utils,datasource_id)
    GoogleCodeIssuesSpecificCleanUp.run(utils,datasource_id)
    
main(sys.argv)