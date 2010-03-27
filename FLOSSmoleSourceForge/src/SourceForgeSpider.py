'''
Created on Aug 16, 2009
This module is designed to run the necessary code to spider the information from 
sourceforge.net and add the information to the oss_mole database.

RUN INSTRUCTIONS
Run this module from command line with the following format:
[Interpreter] SourceForgeSpider.py [datasource_id] [Test T/F]
Test is a string variable. Be sure to use a capital 'T' to denote test mode. 
Otherwise use 'F'.

@author: StevenNorris
'''

from SourceForgeUtils import SourceForgeUtils
import sys
import SourceForgeIndex
import SourceForgeDevelopment
import SourceForge60day
import SourceForgeYear
import SourceForgeDevelopers
import SourceForgeResumes
import SourceForgeMailingLists
import SourceForgeMailingListsSpecific
import SourceForgeMailingPagesMonthly
import SourceForgeDonors
import SourceForgeMailingPages

#this method runs all necessary method for spidering sourceforge.net
def main(argv):
    
    #set variables
    try:
        datasource_id=argv[1]
        test=argv[2]
        mailing=argv[3]
    except:
        print("""RUN INSTRUCTIONS
Run this module from command line with the following format:
[Interpreter] SourceForgeSpider.py [datasource_id] [Test T/F] [Mailing Collection A/M]
Test is a string variable. Be sure to use a capital 'T' to denote test mode. 
Otherwise use 'F'. Mailing Collection is a string variable. Be sure to use a capital 'A'
to dentoe collection of all messages. Otherwise use 'M' to denote collection for just this month.""")
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
    
    #runs the spidering
    SourceForgeIndex.run(utils,datasource_id)
    SourceForgeDevelopment.run(utils,datasource_id)
    SourceForgeDevelopers.run(utils,datasource_id)
    SourceForgeResumes.run(utils,datasource_id)
    SourceForgeDonors.run(utils,datasource_id)
    SourceForgeMailingLists.run(utils,datasource_id)
    SourceForgeMailingListsSpecific.run(utils,datasource_id)
    if(mailing=='A'):
        SourceForgeMailingPages.run(utils,datasource_id)
    else:
        SourceForgeMailingPagesMonthly.run(utils,datasource_id)
    SourceForge60day.run(utils,datasource_id)
    SourceForgeYear.run(utils,datasource_id)
    
    
    
main(sys.argv)