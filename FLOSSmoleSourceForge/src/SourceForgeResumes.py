'''
Created on Sep 28, 2009

This module spiders the individual developer pages for each job and completes the job cycle.

@author: Steven Norris
'''

import re
import sys
import traceback
import time

BASE_INDEX='sourceforge.net/projects/'
BASE_SITE='sourceforge.net/'

def developersSpider(page):
    match=re.compile('<tr class=".+?">.+?</tr>',re.DOTALL)
    links=match.findall(page);
    return links
    
    
def resumeSpider(page):
    link=re.findall('people/viewprofile.php.+?"',page)
    if (link):
        link=link[0]
    else:
        link=None
    return link

def profileSpider(page):
    link=re.findall('users/.+?/',page)
    link=link[0]
    return link

def run(utils,datasource_id):
    
    #collects the developer pages for each job and adds them to sv_indexes
    print("\nGathering developer pages.")
    
    #runs jobs
    job=utils.get_job(datasource_id,'gather_resumes')
    if(utils.error):
        sys.exit()
    while(job!=None):
        time.sleep(3)
        try:
            unixname=job[0]
            print("\nGathering for "+unixname)
            
            #collects memberlist page and crawls for developer links
            print("Retrieving memberlist HTML.")
            members=utils.get_memberlist(datasource_id,unixname)
            members=members[0]
            if(members):
                print("Finding link.")
                links=developersSpider(members)
                
                #inserts developer pages into project_indexes
                if(links):
                    print("Inserting developer pages.")
                    for link in links:
                        
                        profileLink=profileSpider(link)
                        if (profileLink):
                            time.sleep(3)
                            profile=utils.get_page("http://"+BASE_SITE+profileLink)
                            userName=profileLink[6:len(profileLink)-1]
                            print("Finding pages for "+userName)
                            
                            if(profile and re.search('We apologize.  The page you were looking for cannot be found.',profile)==None):
                                insert='''INSERT IGNORE INTO sf_developer_indexes (dev_loginname,profile_html,date_collected,datasource_id)
                                VALUES(%s,%s,NOW(),%s)'''
                                utils.db_insert(insert,userName,profile,datasource_id)
                                
                                resumeLink=resumeSpider(link)
                                if (resumeLink):
                                    time.sleep(3)
                                    resume=utils.get_page("http://"+BASE_SITE+resumeLink)
                                    if(resume and re.search('We apologize.  The page you were looking for cannot be found.',resume)==None):
                                        update='''UPDATE sf_developer_indexes SET skills_html=%s WHERE datasource_id=%s AND dev_loginname=%s'''
                                        utils.db_insert(update,resume,datasource_id,userName)
                                    else:
                                        print("!!!!WARNING!!!! Resume page led to a faulty page or did not exist for "+userName)
                                        print(resumeLink);
                                        utils.post_error('gather_resumes:\nA resume page either did not exist or led to a faulty page.',datasource_id, unixname)
                                        job=utils.get_job(datasource_id,'gather_resumes')
                                        if(utils.error):
                                            sys.exit()
                            
                            else:
                                print("!!!!WARNING!!!! Resume pages did not collect correctly for "+userName)
                                utils.post_error('gather_resumes:\nA profile page either did not exist or led to a faulty page.',datasource_id,unixname)
                                job=utils.get_job(datasource_id,'gather_resumes')
                                if(utils.error):
                                    sys.exit()
                            
                        else:
                            print("!!!!WARNING!!!! resumeLink does not exist.")
                            utils.post_error('gather_resumes:\nA resume page either did not exist or led to a faulty page.',datasource_id,unixname)
                            job=utils.get_job(datasource_id,'gather_resumes')
                            if(utils.error):
                                sys.exit()
                    
                    #change completed
                    utils.change_status('gather_donors','gather_resumes',datasource_id,unixname)
                    job=utils.get_job(datasource_id,'gather_resumes')
                    if(utils.error):
                        sys.exit()  
                        
                else:
                    print("!!!!WARNING!!!! Links to developer pages not found.")
                    utils.post_error('gather_resumes:\nResume links were not found.',datasource_id,unixname)
                    job=utils.get_job(datasource_id,'gather_resumes')
                    if(utils.error):
                        sys.exit()
            
            #if memberlist doesn't collect properly posts error, gets job, and checks for errors
            else:
                print("!!!!WARNING!!!! Developer pages did not collect correctly.")
                utils.post_error('gather_resumes:\nIndex gathering yielded a null response.',datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_resumes')
                if(utils.error):
                    sys.exit()
        
        #if collecting process fails posts error, gets job, and checks for errors
        except:
            print("!!!!WARNING!!!! Developer pages did not collect correctly.")
            utils.post_error('gather_resumes:\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_resumes')
            if(utils.error):
                sys.exit()

