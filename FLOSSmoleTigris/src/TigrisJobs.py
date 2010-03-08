'''
Created on Aug 16, 2009
This module is designed to populate the jobs database for tigris.org.

RUN INSTRUCTIONS
Run this module from command line with the following format:
[Interpreter] TigrisJobs.py [datasource_id] [Test T/F]
Test is a string variable. Be sure to use a capital 'T' to denote test mode. 
Otherwise use 'F'.

@author: StevenNorris
'''

import sys
import re
from TigrisUtils import TigrisUtils
import traceback
import socket
import time

BASE_SITE="http://www.tigris.org/servlets/ProjectList"

#Spiders the main page for the list of project names
def projectsSpider(page):
    find=re.compile('<th>Name</th>.+?</table>',re.DOTALL)
    table=find.search(page)
    if(table==None):
        return table
    table=table.group(0)
    find=re.compile('<tr class=.+?</tr>',re.DOTALL)
    projects=find.findall(table)
    if(projects==None):
        return projects
    projectNames=[]
    for project in projects:
        projectName=re.search('<td>.+?</a>',project)
        projectName=projectName.group(0)
        projectName=re.search('">.+?</a>',projectName)
        projectName=projectName.group(0)
        projectName=projectName[2:len(projectName)-4]
        projectNames.append(projectName)
    return projectNames

#spider counts number of total projects and returns that number
def numberSpider(page):
    find=re.compile('<th>Name</th>.+?</table>',re.DOTALL)
    table=find.search(page)
    if table==None:
        return table
    table=table.group(0)
    find=re.compile('<tr class=.+?</tr>',re.DOTALL)
    catagories=find.findall(table)
    if catagories==None:
        return catagories
    find=re.compile('<td>.</td>    <td>.+?</td>',re.DOTALL)
    number=0
    for catagory in catagories:
        match=find.search(catagory)
        numS=match.group(0)
        numS=numS[18:len(numS)-5]
        num=int(numS)
        number=number+num
    return number

#adds the jobs to the tg_jobs table in the selected database
def main(argv):
    print "Start of Run: "+time.strftime("%I:%M:%S %p")
    
    #set variables
    try:
        datasource_id=argv[1]
        test=argv[2]
    except:
        print ("""RUN INSTRUCTIONS\n
        Run this module from command line with the following format:\n
        [Interpreter] TigrisJobs.py [datasource_id] [Test T/F]\n
        Test is a string variable. Be sure to use a capital 'T' to denote test mode.\n 
        Otherwise use 'F'.""")
        sys.exit()
    
    #checks for test mode
    if(test=='T'):
        try:
            print("TEST MODE ACTIVATED")
            utils=TigrisUtils('dbInfoTest.txt')
        except:
            print("Please create the dbInfo.txt and the dbInfoTest.txt files. See ReadMe for formatting.")
            sys.exit()
    else:
        try:
            utils=TigrisUtils('dbInfo.txt')
        except:
            print("Please create the dbInfo.txt and the dbInfoTest.txt files. See ReadMe for formatting.")
            sys.exit()
    
    #Collects project names and posts jobs to tg_jobs
    try:
        print "Collecting Project Names"
        numPage=utils.get_page(BASE_SITE)
        numPages=numberSpider(numPage)
        main=utils.get_page(BASE_SITE+'?type=Projects&mode=TopLevel&itemsPerPage='+str(numPages))
        projectNames=projectsSpider(main)
        print "Collecting Project Links"
        
        #Check for test to set number of projects to collect
        if (test=="T"):
            final=50
        else:
            final=len(projectNames)
            
        #create jobs for projects
        for project in projectNames[0:final]:
            print "Collecting Link for "+project
            try:
                insert='''INSERT INTO tg_jobs (unixname,datasource_id,status,last_modified,modified_by)
                VALUES(%s,%s,'gather_index',NOW(),%s)'''
                utils.db_insert(insert,project,datasource_id,socket.gethostname())
            except:
                print('!!!!WARNING!!!! Job creation failed for '+project+'.')
                print(traceback.format_exc())      
        
                    
    #If collection fails, print warning and traceback error
    except:
        print "!!!!WARNING!!!! Project unixnames did not collect properly"
        print traceback.format_exc()
        
    print "End of Run: "+time.strftime("%I:%M:%S %p")
        
main(sys.argv)