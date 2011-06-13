'''
Created on Jul 18, 2009

@author: Steven Norris


This module creates the jobs to be run for GitHub

RUN INSTRUCTIONS
Run from command line using this format
[Interpret] GitHubJobs.py [DatasourceID] [Test mode True/False]

Test mode is based on string comparison so make sure capitalization and spelling are exact.
'''


from GitHubutils import GitHubutils
from HTMLParser import HTMLParser
import re
import time
import traceback
import sys
import string
import urllib

BASE_SITE='github.com'

'''
This method finds the Next link on the project page
'''
class HasNextSpider(HTMLParser):
    check_link=''
    
    #used to reset links after a run
    def reset_link(self):
        self.check_link=''
        
    #used to handle the start tags of the main page
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            link=attrs[0][1]
            try:
                hotkey=attrs[1][1]
                if re.search("/repositories/recent\?page",link)!=None and hotkey=='l':
                    self.check_link=link
            except:
                '''
                do nothing
                '''
                
def NextSpider(page):
    match=re.compile('><a href="/repositories/recent\?page=\d+?" hotkey="l">Next');
    groups=match.findall(page)
    if(groups):
        link=groups[0]
        return link[10:len(link)-16]
    else:
        return None
    
def GitHubSpider(page):
    match=re.compile('<td class="title">.+?</td>',re.DOTALL)
    groups=match.findall(page)
    finalLinks=[]
    for group in groups:
        link=re.findall('href="/.+?/.+?"',group)
        link=link[0]
        link=link[6:len(link)-1]
        finalLinks.append(link)
    return finalLinks
        
          
'''
This method runs the spider sequence needed to collect the information from github.com
'''
def main(argv):
    #Declaring variables and creating spiders
    projects_pages="/repositories/recent"
    hasNextPage=True
    track_page=1
    try:
        datasource_id=argv[1]
        datasource_id=str(datasource_id)
        test=argv[2]
    except:
        print("Format arguments thusly: [program] [datasource_id] [True/False(TestMode)]")
        sys.exit()
    
    #checks for test mode
    if(test=='True'):
        try:
            print("TEST MODE ACTIVATED")
            less_num=9
            utils=GitHubutils("dbInfoTest.txt")
        except:
            print("Please create the dbInfo.txt and dbInfoTest.txt files. Check ReadMe for formatting.")
            sys.exit()
    else:
        try:
            less_num=sys.maxint
            utils=GitHubutils("dbInfo.txt")
        except:
            print("Please create the dbInfo.txt and dbInfoTest.txt files. Check ReadMe for formatting.")
            sys.exit()
        
    try:



        for letter in string.lowercase:
          page = 1
          total_pages = 2 #initialize at anything >= 1 (page)
          while page <= total_pages:
            time.sleep(2)
            reader = urllib.urlopen('https://github.com/search?type=Repositories&language=&q='+letter+'&repo=&langOverride=&x=0&y=0&start_value='+str(page))
            current_html = reader.read()
            reader.close()
            
            if test=="True":
              total_pages = 1
            else:
              try:
                total_pages = int(re.search('>(\d+)</a>\n',current_html).group(1))
              except:
                pass
            page += 1
            repos = re.findall(r'<a href="/(\w+)/(\w+)">\1 / \2</a>',current_html)
            for repo in repos:
              project_name = repo[1]
              developer_name = repo[0]
              status = None
              insert='''INSERT IGNORE INTO gh_jobs (datasource_id,project_name,developer_name,status,last_modified) VALUES(%s,%s,%s,%s,NOW())'''
              try:
                utils.db_insert(insert,datasource_id,project_name,developer_name,'XMLgathering')
              except Exception as e:
                print e

        #Begin loop through project pages
#        while(hasNextPage and track_page<less_num):
#            print("Beginning on page "+str(track_page))
#            print("Gathering base page.")

            
            



#            base_page=utils.get_page("http://"+BASE_SITE+projects_pages)
#            time.sleep(2)
#        
#            #Find the project links 
#            print("Gathering project links.")
#
#            redirect_links=GitHubSpider(base_page)
#            if(test=="True"):
#                end_num=5
#            else:
#                end_num=len(redirect_links)
#            
#            print("Creating jobs.")
#            #Gathering pages for each project link
#            for link in redirect_links[0:end_num]:
#                print("Creating job for : "+link)
#                link_segments=link.split('/')
#                project_name=link_segments[2]
#                developer_name=link_segments[1]
#                
#                #gathers xml page and inserts into database
#                insert='''INSERT IGNORE INTO gh_jobs (datasource_id,project_name,developer_name,status,last_modified)
#                VALUES(%s,%s,%s,%s,NOW())'''
#                utils.db_insert(insert,datasource_id,project_name,developer_name,'XMLgathering')
#
#            #Check for next link
#            next_link=NextSpider(base_page)
#            track_page+=1
#            if next_link and track_page<less_num:
#                print(next_link)
#                projects_pages=next_link
#            else:
#                print("Final link reach.")
#                hasNextPage=False
    except:
        print('Job creation failed.')
        print(traceback.format_exc())
        sys.exit()
        
main(sys.argv)


