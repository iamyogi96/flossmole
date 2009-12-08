'''
Created on Aug 16, 2009
This module is designed to run the necessary code to spider the information from 
sourceforge.net and add the information to the oss_mole database.

RUN INSTRUCTIONS
Run this module from command line with the following format:
[Interpreter] SourceForgeJobs.py [datasource_id] [Test T/F]
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

#this method runs all necessary method for spidering sourceforge.net
def main(argv):
    
    #set variables
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
    try:
        if (test=='T'):
            print("TEST MODE ACTIVATED")
            utils=SourceForgeUtils('dbInfoTest.txt')
        else:
            utils=SourceForgeUtils('dbInfo.txt')
    except:
        print("Please create the dbInfo.txt and the dbInfoText.txt files. See ReadMe for formatting.")
        sys.exit()
    
    #runs the spidering
    SourceForgeIndex.run(utils,datasource_id)
    SourceForgeDevelopment.run(utils,datasource_id)
    SourceForgeDevelopers.run(utils,datasource_id)
    SourceForge60day.run(utils,datasource_id)
    SourceForgeYear.run(utils,datasource_id)
    SourceForgeResumes.run(utils,datasource_id)
    
    
main(sys.argv)