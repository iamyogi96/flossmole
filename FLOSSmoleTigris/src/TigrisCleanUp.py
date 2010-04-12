'''
Created on Mar 29, 2010
This method is made to clean up the jobs left In_Progress by machine error and prepare them for a second run.
@author: StevenNorris
'''

from TigrisUtils import TigrisUtils
import sys
import time
import TigrisIndexCleanUp
import TigrisMemberlistCleanUp
import TigrisDiscussionsCleanUp
import TigrisDiscussionsSpecificCleanUp
import TigrisMessagesCleanUp

#main method for running clean ups
def main(argv):
    print "Start of Run: "+time.strftime("%I:%M:%S %p")
    
    #set variables
    try:
        datasource_id=argv[1]
        test=argv[2]
    except:
        print("""RUN INSTRUCTIONS
    Run this module from command line with the following format:
    [Interpreter] TigrisSpider.py [datasource_id] [Test T/F] [Mailing M/A]
    Test is a string variable. Be sure to use a capital 'T' to denote test mode. 
    Otherwise use 'F'. Also, use a capital 'A' to indicate collect all mail, otherwise use 'M'
    for only the month of the run to be collected.""")
        sys.exit()
    
    #Checks for test mode
    try:
        if (test=='T'):
            print("TEST MODE ACTIVATED")
            utils=TigrisUtils('dbInfoTest.txt')
        else:
            utils=TigrisUtils('dbInfo.txt')
    except:
        print("Please create the dbInfo.txt and the dbInfoTest.txt files. See ReadMe for formatting.")
        sys.exit()
        
    #Does the cleanup for the Tigris projects
    TigrisIndexCleanUp.run(utils,datasource_id)
    TigrisMemberlistCleanUp.run(utils,datasource_id)
    TigrisDiscussionsCleanUp.run(utils,datasource_id)
    TigrisDiscussionsSpecificCleanUp.run(utils,datasource_id)
    TigrisMessagesCleanUp.run(utils,datasource_id)
    
main(sys.argv)