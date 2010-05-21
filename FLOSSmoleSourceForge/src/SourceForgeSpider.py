'''
Created on Aug 16, 2009
This module is designed to run the necessary code to spider the information from 
sourceforge.net and add the information to the oss_mole database.

RUN INSTRUCTIONS
Run this module from command line with the following format:
[Interpreter] SourceForgeSpider.py [datasource_id] [Test T/F] [Stage 1/2/3/4/5] [Mailing Mode]

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
        if(not test=='T' and  not test=='F'):
            test=1/0
        stage=argv[3]
        if(stage=='1'):
            stage=1
        elif(stage=='2'):
            stage=2
        elif(stage=='3'):
            stage=3
        elif(stage=='4'):
            stage=4
        elif(stage=='5'):
            stage=5
            mailing=argv[4]
            if(not mailing=='M' and not mailing=='A'):
                mailing=1/0
        else:
            stage=1/0
            
    except:
        print("""RUN INSTRUCTIONS
        Run this module from command line with the following format:
[Interpreter] SourceForgeSpider.py [datasource_id] [Test T/F] [Stage 1/2/3/4/5] [Mailing Collection A/M]""")
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
    if(stage==1):
        SourceForgeIndex.run(utils,datasource_id,0)
    elif(stage==2):
        SourceForgeIndex.run(utils,datasource_id,1)
        SourceForgeDevelopment.run(utils,datasource_id,0)
        SourceForgeDevelopers.run(utils,datasource_id)
        SourceForgeResumes.run(utils,datasource_id)
    elif(stage==3):
        SourceForgeIndex.run(utils,datasource_id,2) 
        SourceForgeDonors.run(utils,datasource_id)
    elif(stage==4):
        SourceForgeIndex.run(utils,datasource_id,1)
        SourceForgeDevelopment.run(utils,datasource_id,1)
        SourceForge60day.run(utils,datasource_id)
        SourceForgeYear.run(utils,datasource_id)
    else:
        SourceForgeIndex.run(utils,datasource_id,1)
        SourceForgeDevelopment.run(utils,datasource_id,2)
        SourceForgeMailingLists.run(utils,datasource_id)
        SourceForgeMailingListsSpecific.run(utils,datasource_id)
        if(mailing=='A'):
            SourceForgeMailingPages.run(utils,datasource_id)
        else:
            SourceForgeMailingPagesMonthly.run(utils,datasource_id)
    
    
    
main(sys.argv)