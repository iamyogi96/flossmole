'''
Created on Mar 27, 2010
This module is designed to run the necessary code to spider the information from 
code.google.com and add the information to the oss_mole database.

RUN INSTRUCTIONS
Run this module from command line with the following format:
[Interpreter] GoogleCodeSpider.py [datasource_id] [Test T/F]
Test is a string variable. Be sure to use a capital 'T' to denote test mode. 
Otherwise use 'F'.

@author: StevenNorris
'''

from GoogleCodeUtils import GoogleCodeUtils
import sys
import GoogleCodeHome
import GoogleCodeUpdates
import GoogleCodePeople
import GoogleCodeWiki
import GoogleCodeIssues
import GoogleCodePeopleSpecific
import GoogleCodeIssuesSpecific
import GoogleCodeDownloads

#this method runs all necessary method for spidering sourceforge.net
def main(argv):
    
    #set variables
    try:
        datasource_id=argv[1]
        test=argv[2]
    except:
        print("""RUN INSTRUCTIONS
Run this module from command line with the following format:
[Interpreter] GoogleCodeSpider.py [datasource_id] [Test T/F]
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
    
    #runs the spidering
    GoogleCodeHome.run(utils,datasource_id)
    GoogleCodeUpdates.run(utils,datasource_id)
    GoogleCodePeople.run(utils,datasource_id)
    GoogleCodeDownloads.run(utils,datasource_id)
    GoogleCodeIssues.run(utils,datasource_id)
    GoogleCodeWiki.run(utils,datasource_id)
    GoogleCodePeopleSpecific.run(utils,datasource_id)
    GoogleCodeIssuesSpecific.run(utils,datasource_id)

main(sys.argv)
