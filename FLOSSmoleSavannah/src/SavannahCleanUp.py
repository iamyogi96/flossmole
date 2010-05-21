'''
Created on May 21, 2010

Performs the clean up for projects left In_Progress for Savannah.

@author: StevenNorris
'''

import sys
from SavannahUtils import SavannahUtils
import SavannahIndexCleanUp
import SavannahSkillsCleanUp
import SavannahParsingCleanUp

def main(argv):
    
    #set variables
    try:
        datasource_id=argv[1]
        test=argv[2]
    except:
        print("""RUN INSTRUCTIONS
    Run this module from command line with the following format:
    [Interpreter] SavannahCleanUp.py [datasource_id] [Test True/False]
    Test is a string variable. Be sure to use a capital 'T' to denote test mode. 
    Otherwise use 'F'.""")
        sys.exit()
    
    #Checks for test mode
    try:
        if (test=='T'):
            print("TEST MODE ACTIVATED")
            utils=SavannahUtils('dbInfoTest.txt')
        else:
            utils=SavannahUtils('dbInfo.txt')
    except:
        print("Please create the dbInfo.txt and the dbInfoTest.txt files. See ReadMe for formatting.")
        sys.exit()
        
    #running clean up
    SavannahIndexCleanUp.run(utils,datasource_id)
    SavannahSkillsCleanUp.run(utils,datasource_id)
    SavannahParsingCleanUp.run(utils,datasource_id)

main(sys.argv)
        