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
import httplib
import re
import time
import MySQLdb
import traceback
import sys

BASE_SITE='github.com'

'''
This class is used to check every page of the repository for a projects list
'''
class GitHubSpider(HTMLParser):
    
    #Used to store the links needing to be checked
    check_links=[]
    
    #Used to reset check_links after every feed()
    def reset_link_list(self):
        self.check_links=[]
        
    #Used to handle the start tags of the main page
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            link=attrs[0][1]
            if re.search('/tree(?!.)', link)!=None:
                self.check_links.append(link)
                
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
                if re.search("/repositories\?page",link)!=None and hotkey=='l':
                    self.check_link=link
            except:
                '''
                do nothing
                '''
                
'''
This method runs the spider sequence needed to collect the information from github.com
'''
def main(argv):
    
    #Declaring variables and creating spiders
    projects_pages="/repositories"
    hasNextPage=True
    spider=GitHubSpider()
    spider_Next=HasNextSpider()
    track_page=1
    datasource_id=argv[1]
    datasource_id=str(datasource_id)
    test=argv[2]
    
    #checks for test mode
    if(test=='True'):
        utils=GitHubutils("dbInfoTest.txt")
        try:
            print("TEST MODE ACTIVATED")
            #Establish the connection and get the base_page
            print("Setting up connection.")
            
            #Begin loop through project pages
            while(hasNextPage and track_page<9):
                print("\n")
                print("Beginning on page "+str(track_page))
                print("Gathering base page.")
                base_page=utils.get_page("http://"+BASE_SITE+projects_pages)
                time.sleep(2)
            
                #Create the spider and begin the feed
                print("Gathering project links.")
                spider.feed(base_page)
                
                #Storing project links and preparing spider
                redirect_links=spider.check_links
                spider.reset_link_list()
                
                print("Creating jobs.")
                #Gathering pages for each project link
                for link in redirect_links[0:3]:
                    print("Creating job for : "+link)
                    link_segments=link.split('/')
                    project_name=link_segments[2]
                    developer_name=link_segments[1]
                    
                    #gathers xml page and inserts into database
                    insert='''INSERT IGNORE INTO gh_jobs (datasource_id,project_name,developer_name,status,last_modified)
                    VALUES(%s,%s,%s,%s,NOW())'''
                    utils.db_insert(insert,datasource_id,project_name,developer_name,'XMLgathering')

                #Check for next link
                spider_Next.feed(base_page)
                next_link=spider_Next.check_link
                spider_Next.reset_link()
                track_page+=1
                if next_link!='' and track_page<9:
                    print(next_link)
                    projects_pages=next_link
                else:
                    print("Final link reach.")
                    hasNextPage=False
        except:
            print('Job creation failed.')
            print(traceback.format_exc())
            sys.exit()
    else:
        utils=GitHubutils("dbInfo.txt")
        try:
            #Establish the connection and get the base_page
            print("Setting up connection.")
            
            #Begin loop through project pages
            while(hasNextPage):
                print("\n")
                print("Beginning on page "+str(track_page))
                print("Gathering base page.")
                base_page=utils.get_page("http://"+BASE_SITE+projects_pages)
                time.sleep(2)
            
                #Create the spider and begin the feed
                print("Gathering project links.")
                spider.feed(base_page)
                
                #Storing project links and preparing spider
                redirect_links=spider.check_links
                spider.reset_link_list()
                
                print("Collecting jobs.")
                #Gathering pages for each project link
                for link in redirect_links:
                    print("Creating job for: "+link)
                    link_segments=link.split('/')
                    project_name=link_segments[2]
                    developer_name=link_segments[1]
                    
                    #gathers XMl page and inserts into database
                    insert='''INSERT INTO gh_jobs (datasource_id,project_name,developer_name,status,last_modified)
                    VALUES(%s,%s,%s,%s,NOW())'''
                    utils.db_insert(insert,datasource_id,project_name,developer_name,'XMLgathering')
                        
                #Check for next link
                spider_Next.feed(base_page)
                next_link=spider_Next.check_link
                spider_Next.reset_link()
                track_page+=1
                if next_link!='':
                    print('Following next page at: '+next_link)
                    projects_pages=next_link
                else:
                    print("Final link reach.")
                    hasNextPage=False
        except:
            print('Job creation failed.')
            sys.exit()
main(sys.argv)