'''
Created on Mar 27, 2010
This module does the spidering for the code.google.com project individual people pages.
@author: StevenNorris
'''

BASE_LINK="http://code.google.com"

import sys
import time
import traceback
import re

#This method spiders the given page for the specific people links
def peopleSpider(html):
    links=[]
    matches=re.findall('<a style="white-space: nowrap" href="(/u/.+?)"',html)
    if (len(matches)!=0):
        for match in matches:
            name=match[3:len(match)-1]
            links.append((name,match))
        return links
    else:
        return None

def run(utils,datasource_id):
    print("\nGathering individual people pages.")
    
    #runs jobs
    job=utils.get_job(datasource_id,"gather_people_specific")
    if(utils.error):
        sys.exit()
    while(job!=None):
        time.sleep(3)
        try:
            unixname=job[0]
            print ("Gathering for "+unixname)
            
            #gets home page
            home=utils.get_home(datasource_id, unixname)
            
            #checks for forbidden or non-existant pages
            if(home):
                home=home[0]
                if(re.search('<title>Project hosting on Google Code</title>',home)==None):
                    
                    #gaathers and insertspages for each developer link found
                    links=peopleSpider(home)
                    if(links):
                        for link in links:
                            time.sleep(3)
                            name=link[0]
                            link=link[1]
                            print("\tInserting developer "+name+" for "+unixname)
                            dev=utils.get_page(BASE_LINK+link)
                            insertJoin="""INSERT IGNORE INTO gc_developer_projects (unixname,dev_name,datasource_id,last_modified)
                            VALUES(%s,%s,%s,NOW())"""
                            insert="""INSERT IGNORE INTO gc_developer_indexes (dev_name,datasource_id,devhtml,last_modified)
                            VALUES(%s,%s,%s,NOW())"""
                            utils.db_insert(insertJoin,unixname,name,datasource_id)
                            utils.db_insert(insert,name,datasource_id,dev)
                            
                        #get new job
                        utils.change_status("gather_issues_specific","gather_people_specific",datasource_id,unixname)
                        job=utils.get_job(datasource_id,'gather_people_specific')
                        if(utils.error):
                            sys.exit()
                    
                    #if no links are found, get new job
                    else:
                        print("!! No links found for "+unixname)
                        utils.change_status("gather_issues_specific","gather_people_specific",datasource_id,unixname)
                        job=utils.get_job(datasource_id,'gather_people_specific')
                        if(utils.error):
                            sys.exit()
                
                #if home page leads to a forbidden page, get new job
                else:
                    print("!! Home page led to a forbidden page.")
                    utils.change_status("gather_issues_specific","gather_people_specific",datasource_id,unixname)
                    job=utils.get_job(datasource_id,'gather_people_specific')
                    if(utils.error):
                        sys.exit()
                    
            #if home page gathering fails, post error and get new job
            else:
                print("!!!WARNING!!!! Home page gathering failed for "+unixname)
                utils.post_error('gather_people_specific: \nHome page did not collect correctly.' ,datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_people_specific')
                if(utils.error):
                    sys.exit()
                    
        #if process fails, post error and get new job
        except:
            print("!!!!WARNING!!! Specific people pages collection failed")
            utils.post_error('gather_people_specific:\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_people_specific')
            if(utils.error):
                sys.exit()