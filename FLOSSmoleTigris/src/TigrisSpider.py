'''
Created on Feb 21, 2010

This runs the spidering for Tigris.org opensource projects.

@author: Steven Norris
'''

from TigrisUtils import TigrisUtils
import sys
import TigrisIndex
import TigrisMemberlist
import TigrisDiscussions
import TigrisDiscussionsSpecific
import TigrisMessages
import time
import TigrisMessagesMonth

def main(argv):
    
    print "Start of Run: "+time.strftime("%I:%M:%S %p")
    
    #set variables
    try:
        datasource_id=argv[1]
        test=argv[2]
        mailing=argv[3]
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
        
    #runs the spidering
    TigrisIndex.run(utils,datasource_id)
    TigrisMemberlist.run(utils,datasource_id)
    TigrisDiscussions.run(utils,datasource_id)
    TigrisDiscussionsSpecific.run(utils,datasource_id)
    if(mailing=='A'):
        TigrisMessages.run(utils,datasource_id)
    else:
        TigrisMessagesMonth.run(utils,datasource_id)

    print "End of Run: "+time.strftime("%I:%M:%S %p")
    
main(sys.argv)