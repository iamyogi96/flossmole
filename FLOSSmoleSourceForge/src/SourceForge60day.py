'''
Created on Sep 28, 2009

This module spiders the 60 day stats page for each job and prepares for yearly spidering.

@author: Steven Norris
'''

import re
import sys
import traceback
import time

BASE_INDEX='sourceforge.net/projects/'
BASE_SITE='sourceforge.net/'

#This spider finds the link fot the stats pag eon the development page
def statsSpider(page):
    match=re.search('group_id=.+?"',page)
    if(match!=None):
        link=match.group(0)
        return link[9:len(link)-11]
    else:
        return None

def run(utils,datasource_id):
    
    #collects the 60daystats pages for each job and adds them to sv_indexes
    print("\nGathering 60daystats pages.")
    
    #runs jobs
    job=utils.get_job(datasource_id,'gather_60day')
    if(utils.error):
        sys.exit()
    while(job!=None):
        time.sleep(3)
        try:
            unixname=job[0]
            print("\nGathering for "+unixname)
            
            #collects development page and crawls for 60day link
            print("Retrieving development HTML.")
            dev_page=utils.get_development(datasource_id,unixname)
            dev_page=dev_page[0]
            if(dev_page):
                print("Finding link.")
                id=statsSpider(dev_page)
                
                #inserts 60day page into project_indexes
                if(id):
                    print("Inserting 60daystats page.")
                    stats60=utils.get_page("http://"+BASE_SITE+"project/stats/?group_id="+id+"&ugn="+unixname+"&type&mode=60day")
                else:
                    print("No group id found.")
                    stats60=None
                    
                if(stats60 and re.search('We apologize.  The page you were looking for cannot be found.',stats60)==None):
                    i=0
                    while(re.search("Connection to statistics server timed out",stats60)!=None and i<5):
                        stats60=utils.get_page("http://"+BASE_SITE+"project/stats/?group_id="+id+"&ugn="+unixname+"&type&mode=60day")
                        i+=1
                    if(re.search("Connection to statistics server timed out",stats60)==None):
                        update="UPDATE sf_project_indexes SET statistics_html=%s WHERE datasource_id=%s AND proj_unixname=%s"
                        utils.db_insert(update,stats60,datasource_id,unixname)
                        utils.change_status('gather_year','gather_60day',datasource_id,unixname)
                        job=utils.get_job(datasource_id,'gather_60day')
                        if(utils.error):
                            sys.exit()
                    else:
                        print("!!!!WARNING!!!! 60daystats page timed out.")
                        utils.change_status('gather_year','gather_60day',datasource_id,unixname)
                        utils.post_error('gather_60day:\n60daystats page timed out.',datasource_id,unixname)
                        insert='''INSERT INTO sf_jobs (unixname,datasource_id,status,last_modified)
                        VALUES(%s,%s,%s,NOW())'''
                        utils.db_insert(insert,unixname,datasource_id,'error_60day')
                        job=utils.get_job(datasource_id,'gather_60day')
                        if(utils.error):
                            sys.exit()
                        
                #if 60day insertion fails posts error, gets job, and checks for errors
                else:
                    print("60daystats page does not exist.")
                    utils.change_status('gather_year','gather_60day',datasource_id,unixname)
                    job=utils.get_job(datasource_id,'gather_60day')
                    if(utils.error):
                        sys.exit()
                   
            
            #if development doesn't collect properly posts error, gets job, and checks for errors
            else:
                print("!!!!WARNING!!!! 60daystats page did not collect correctly.")
                utils.post_error('gather_60day:\nDevelopment gathering yielded a null response.',datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_60day')
                if(utils.error):
                    sys.exit()
        
        #if collecting process fails posts error, gets job, and checks for errors
        except:
            print("!!!!WARNING!!!! 60daystats page did not collect correctly.")
            utils.post_error('gather_60day:\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_60day')
            if(utils.error):
                sys.exit()   