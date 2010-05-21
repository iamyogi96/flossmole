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
import re
from SavannahUtils import SavannahUtils
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
            
def spiderNumbers(html):
    match=re.search("""<a href="/search/\?type_of_search=soft&amp;words=%%%&amp;type=1" class="center">(?P<GNU>\d+?)\D+?</a>""",html)
    if(match!=None):
        numberGNU=match.group('GNU')
        match=re.search("""<a href="/search/\?type_of_search=soft&amp;words=%%%&amp;type=2" class="center">(?P<NON>\d+?)\D+?</a>""",html)
        if(match!=None):
            numberNonGNU=match.group('NON')
            return (numberGNU,numberNonGNU)
        else:
            return None
    else:
        return None
    
def main(argv):
    
    #sets arguments
    try:
        data_source_id=argv[1]
        test=argv[2]
    except:
        print ("""RUN INSTRUCTIONS\n
        Run this module from command line with the following format:\n
        [Interpreter] SavannahJobs.py [datasource_id] [Test True/False]\n
        Test is a string variable. Be sure to use a capital 'T' to denote test mode.\n 
        Otherwise use 'F'.""")
        sys.exit()
        
    print ("Creating jobs for "+str(data_source_id)+":\n")
    
    #creates spider
    spider=SpiderSavannahProjectsList()
    
    #checks for test mode and acts accordingly
    if(test=='True'):
        print("TEST MODE ACTIVATED")
        utils=SavannahUtils("dbInfoTest.txt")
    else:
        utils=SavannahUtils("dbInfo.txt")

    #Getting project numbers
    print("Getting project numbers.")
    main_page=utils.get_page("http://savannah.gnu.org/")
    if(main_page):
        numbers=spiderNumbers(main_page);
        GNUnum=numbers[0]
        NONnum=numbers[1]
        
        #Creates jobs for GNU projects
        print("Creating GNU jobs.")
        page=utils.get_page('http://'+BASE_SITE+'/search/?type_of_search=soft&words=%2A&type=1&offset=0&max_rows='+GNUnum+'#results')
        if(page):
            page_string=str(page)
            spider.feed(page_string)
            if(test=='True'):
                end=20
            else:
                end=len(spider.check_links)
            for link in spider.check_links[0:end]:
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
        page=utils.get_page('http://'+BASE_SITE+'/search/?type_of_search=soft&words=%2A&type=2&offset=0&max_rows='+NONnum+'#results')
        if(page):
            page_string=str(page)
            spider.feed(page_string)
            if(test=='True'):
                end=20
            else:
                end=len(spider.check_links)
            for link in spider.check_links[0:end]:
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
            print("!!!WARNING!!!! Pages did not collect properly for NON-GNU projects.")
            sys.exit()
    else:
        print("!!!!WARNING!!!! Numbers for projects did not collect properly.")
        sys.exit()
            
main(sys.argv)
    