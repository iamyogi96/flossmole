'''
Created on May 2, 2010

This module spiders the index page of each job and prepares for skills spidering.

@author: Steven Norris
'''

from HTMLParser import HTMLParser
import re
import time
import sys
import traceback

BASE_SITE1='savannah.gnu.org'
BASE_SITE2='savannah.nongnu.org'

'''
This spider handles the skills pages in each members page
'''
class SpiderSavannahSkills(HTMLParser):
    
    check_links=[]
  
    #handles the start tag for each skills page and adds it to check_links
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            link=attrs[0][1]
            if re.search('resume.php',link)!=None:
                self.check_links.append(link)

'''
This class allows for the collection of usernames from the skills pages
'''
class User_Name_Spider(HTMLParser):
    
    check_links=[]
    
    #handles the start tag for each user name and returns it
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            link=attrs[0][1]
            if re.search("/users",link)!=None:
                self.check_links.append(link)

def run(utils,data_source_id):
    
    #creates needed spiders
    spiderSkills=SpiderSavannahSkills()
    spiderUserName=User_Name_Spider()
    
    #Does the skills page collection for the projects
    print("\nGathering skills pages")
    job=utils.get_job(data_source_id,'skillsHTML')
    if (utils.error):
        sys.exit()
    while (job!=None):
        try:
            error=False
            member_html=utils.get_member_html(job[0],data_source_id)
            member_html=member_html[0]
            spiderSkills.feed(member_html)
            
            #collects the skill pages for each member
            print("Gathering skills pages for "+job[0])
            if(type=='gnu'):
                BASE_SITE=BASE_SITE1
            else:
                BASE_SITE=BASE_SITE2
            for link in spiderSkills.check_links:
                print("finding skills page at "+link)
                dev_id=link[27:]
                skills_page=utils.get_page('http://'+BASE_SITE+link)
                if(skills_page):
                    skills_page=str(skills_page)
                    spiderUserName.feed(skills_page)
                    user_name=spiderUserName.check_links[0]
                    info_page=utils.get_page('http://'+BASE_SITE+user_name)
                    if(info_page):
                        info_page=str(info_page)
                        user_name=user_name[7:]
                        spiderUserName.check_links=[]
                        
                        
                        print("Inserting for "+user_name+" on project "+job[0])
                        #Insert the developer into sv_developers
                        print("Inserting into sv_developers.")
                        insert='''INSERT IGNORE INTO sv_developers (datasource_id,dev_loginname,developer_id,skillshtml,infohtml,date_collected)
                        VALUES(%s,%s,%s,%s,%s,NOW())'''
                        utils.db_insert(insert,data_source_id,user_name,dev_id,skills_page,info_page)
                        
                        #Insert the developer into sv_developers_projects
                        print("Inserting into sv_developer_projects.")
                        insert='''INSERT INTO sv_developer_projects (datasource_id,dev_loginname,project_name,date_collected)
                        VALUES(%s,%s,%s,NOW())'''
                        utils.db_insert(insert,data_source_id,user_name,job[0])
                    else:
                        print('!!!!WARNING Skills pages did not collect correctly!!!!')
                        utils.post_error(traceback.format_exc(),job[0],data_source_id,job[1])
                        if(utils.error):
                            sys.exit()
                        error=True
                else:
                    print('!!!!WARNING Skills pages did not collect correctly!!!!')
                    utils.post_error(traceback.format_exc(),job[0],data_source_id,job[1])
                    if(utils.error):
                        sys.exit()
                    error=True
                    
            #refresh links, sleep, change status, get new job, and check for errors
            spiderSkills.check_links=[]
            time.sleep(3)
            print (error)
            if(not error):
                utils.change_status('indexparsing','skillsHTML',data_source_id,job[0])
            job=utils.get_job(data_source_id,'skillsHTML')
            if (utils.error): 
                sys.exit()
        
        #posts errors in case of faulty skills gathering
        except:
            print('!!!!WARNING!!!! Skills pages did not collect correctly.')
            utils.post_error(traceback.format_exc(),job[0],data_source_id,job[1])
            job=utils.get_job(data_source_id,'skillsHTML')
            if (utils.error):
                sys.exit()
        