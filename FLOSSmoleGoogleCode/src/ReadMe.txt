Run Instructions:
All runs are passed with two arguments, as follows:
    1st. [datasource_id]
    2nd. [T/F(Test Mode Selection-Must be "T" specifically if running test mode.)]
    
1. Run GoogleCodeJobs.py given two arguments. GoogleCodeJobs.py [datasource_id] [Test Mode]
2. Run GoogleCodeSpider.py given two arguments. GoogleCodeSpider.py [datsource_id] [Test Mode]
4. Run GoogleCodeCleanUp.py given two arguments. GoogleCodeCleanUp.py [datasource_id] [Test Mode]
5. Rerun GoogleCodeSpider.py given two arguments. GoogleCodeSpider.py [datsource_id] [Test Mode]


GoogleCodeJobs.py-creates jobs to be run from a pre-processed projects list
GoogleCodeSpider.py-spiders pages based on pre-processed jobs list
GoogleCodeCleanUp.py-resets projects stuck In_Progress due to machine error

Two text files must be created in order to run both test mode and the non-test mode. The format is as follows

dbInfo.txt & dbInfoTest.txt:

databasename
port#
username
password
tablename
