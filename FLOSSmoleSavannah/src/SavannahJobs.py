'''
Created on Jul 16, 2009

@author: Steven Norris

This program creates the jobs for savannah.gnu.org

RUN INSTRUCTIONS
Run from command line using this format
[Interpret] SavannahJobs.py [DatasourceID] [Test mode True/False]

Test mode is based on string comparison so make sure capitalization and spelling are exact.
'''
from HTMLParser import HTMLParser
import httplib
import re
import time
from FLOSSmoleutils import FLOSSmoleutils
import sys


BASE_SITE='savannah.gnu.org'
BASE_SITE2='savannah.nongnu.org'

'''
This spider searches the projects page for a list of projects.
'''

class SpiderSavannahProjectsList(HTMLParser):
    
    check_links=[]
    
    #allows for the links to be cleared
    def clear_check_links(self):
        self.check_links=[]
    
    #handles the start tag for the projects page link and adds the links to check_links
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            link=attrs[0][1]
            if re.search('\.\./projects/',link)!=None:
                self.check_links.append(link[2:len(link)])


def main(argv):
    
    #sets arguments
    print("!!WARNING!!\nIf the GNU projects have exceeded 400 or the non-GNU projects have exceeded 4000 \nthe code must be modified to notice that change.\n"
    +"In order to do this, simply modify the max_rows=____ portion of this line to represent \nthe correct number in each section:\n"
    +"page=spider.get_page(BASE_SITE,'/search/?type_of_search=soft&words=%2A&type=1&offset=0&max_rows=400#results')")
    data_source_id=argv[1]
    test=argv[2]
    print ("Creating jobs for "+str(data_source_id)+":\n")
    
    #creates spider
    spider=SpiderSavannahProjectsList()
    
    #checks for test mode and acts accordingly
    if(test=='True'):
        print("TEST MODE ACTIVATED")
        utils=FLOSSmoleutils("dbInfoTest.txt")
        #Creates jobs for GNU projects
        print("Creating GNU jobs.")
        page=utils.get_page('http://'+BASE_SITE+'/search/?type_of_search=soft&words=%2A&type=1&offset=0&max_rows=400#results')
        if(page):
            page_string=str(page)
            spider.feed(page_string)
            for link in spider.check_links[0:20]:
                insert='''INSERT INTO sv_jobs (
                target_name,status,datasource_id,GNU_NON,link,last_modified)
                VALUES(%s,'indexHTML',%s,'GNU',%s,NOW())'''
                try:
                    utils.db_insert(insert,link[10:len(link)],data_source_id,link)
                    if (utils.error):
                        sys.exit()
                except:
                    print("!!!!WARNING!!!! Project "+link+" did not insert correctly into sv_jobs.")
        else:
            print("!!!!WARNING!!!! Pages not collected properly for GNU projects.")
            sys.exit()
        
        #Creates jobs for NON-GNU projects
        print("\nCreating NON-GNU jobs.")
        spider.clear_check_links()
        page=utils.get_page('http://'+BASE_SITE+'/search/?type_of_search=soft&words=%2A&type=2&offset=0&max_rows=4000#results')
        if(page):
            page_string=str(page)
            spider.feed(page_string)
            for link in spider.check_links[0:20]:
                insert='''INSERT INTO sv_jobs (
                target_name,status,datasource_id,GNU_NON,link,last_modified)
                VALUES(%s,'indexHTML',%s,'NONGNU',%s,NOW())'''
                try:
                    utils.db_insert(insert,link[10:len(link)],data_source_id,link)
                    if (utils.error):
                        sys.exit()
                except:
                    print("!!!!WARNING!!!! Project "+link+" did not insert correctly into sv_jobs.")
        else:
            print("!!!WARNING!!! Pages did not collect properly for NON-GNU projects.")
            sys.exit()
    else:
        utils=FLOSSmoleutils("dbInfo.txt")
        #Creates jobs for GNU projects
        print("Creating GNU jobs.")
        page=utils.get_page('http://'+BASE_SITE+'/search/?type_of_search=soft&words=%2A&type=1&offset=0&max_rows=400#results')
        if(page):
            page_string=str(page)
            spider.feed(page_string)
            for link in spider.check_links:
                insert='''INSERT INTO sv_jobs (
                target_name,status,datasource_id,GNU_NON,link,last_modified)
                VALUES(%s,'indexHTML',%s,'GNU',%s,NOW())'''
                try:
                    utils.db_insert(insert,link[10:len(link)],data_source_id,link)
                    if (utils.error):
                        sys.exit()
                except:
                    print("!!!!WARNING!!!! Project "+link+" did not insert correctly into sv_jobs.")
        else:
            print("!!!!WARNING!!!! Pages not collected properly for GNU projects.")
            sys.exit()
        
        #Creates jobs for NON-GNU projects
        print("\nCreating NON-GNU jobs.")
        spider.clear_check_links()
        page=utils.get_page('http://'+BASE_SITE+'/search/?type_of_search=soft&words=%2A&type=2&offset=0&max_rows=4000#results')
        if(page):
            page_string=str(page)
            spider.feed(page_string)
            for link in spider.check_links:
                insert='''INSERT INTO sv_jobs (
                target_name,status,datasource_id,GNU_NON,link,last_modified)
                VALUES(%s,'indexHTML',%s,'NONGNU',%s,NOW())'''
                try:
                    utils.db_insert(insert,link[10:len(link)],data_source_id,link)
                    if (utils.error):
                        sys.exit()
                except:
                    print("!!!!WARNING!!!! Project "+link+" did not insert correctly into sv_jobs.")
        else:
            print("!!!WARNING!!! Pages did not collect properly for NON-GNU projects.")
            sys.exit()
main(sys.argv)
    