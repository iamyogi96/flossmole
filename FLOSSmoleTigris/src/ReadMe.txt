Run Instructions:
Job runs are passed with two arguments, as follows:
    1st. [datasource_id]
    2nd. [T/F(Test Mode Selection-Must be "T" specifically if running test mode.)]
 
Spider runs are passed with three arguments, as follows:
    1st. [datasource_id]
    2nd. [T/F(Test Mode Selection-Must be "T" specifically if running test mode.)]
    3rd. [M/A(Mailing List Mode Selection-Must be "A" specifically if running for all messages collection and "M" for monthly collection.)]
    
1. Run TigrisJobs.py given two arguments. TigrisJobs.py [datasource_id] [Test Mode]
2. Run TigrisSpider.py given two arguments. TigrisSpider.py [datsource_id] [Test Mode] [Mailing List Mode]
3. Run TigrisCleanUp.py given two arguments. TigrisCleanUp.py [datasource_id] [Test Mode]
4. Rerun TigrisSpider.py given two arguments. TigrisSpider.py [datsource_id] [Test Mode] [Mailing List Mode]

TigrisJobs.py-creates jobs to be run from Tigris.org
TigrisSpider.py-spiders pages based on pre-processed jobs list


Two text files must be created in order to run both test mode and the non-test mode. The format is as follows

dbInfo.txt & dbInfoTest.txt:

hostname
port#
username
password
databasename


   