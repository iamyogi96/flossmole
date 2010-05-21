'''
Created on May 26, 2009

@author: Steven Norris

This program runs as a spider for the the savannah.gnu.org to add information about
both the GNU projects and non-GNU projects to a database for further investigation.

RUN INSTRUCTIONS
Run from command line using this format
[Interpret] SavannahSpider.py [DatasourceID] [Test mode True/False]

Test mode is based on string comparison so make sure capitalization and spelling are exact.
'''

from SavannahUtils import SavannahUtils
import sys
import SavannahIndex
import SavannahSkills
import SavannahParsing
            
'''
Runs the spiders for savannah.gnu.org
'''
def main(argv):
    
    try:
        data_source_id=argv[1]
        test=argv[2]
    except:
        print("Format arguments thusly: [program] [datasource_id] [True/False(TestMode)]")
        sys.exit()
        
    #checks for test mode
    if(test=='True'):
        utils=SavannahUtils("dbInfoTest.txt")
    else:
        utils=SavannahUtils("dbInfo.txt")
    
    #does the spidering
    SavannahIndex.run(utils,data_source_id)
    SavannahSkills.run(utils,data_source_id)
    SavannahParsing.run(utils,data_source_id)

main(sys.argv)
    