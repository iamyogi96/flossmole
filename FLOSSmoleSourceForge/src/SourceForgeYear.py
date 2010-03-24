'''
Created on Sep 28, 2009

This module spiders the yearly stats page for each job and prepares for individual developer spidering.

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
           
    #collects the yearstats pages for each job and adds them to sv_indexes
    print("\nGathering yearstats pages.")
    
    #runs jobs
    job=utils.get_job(datasource_id,'gather_year')
    if(utils.error):
        sys.exit()
    while(job!=None):
        time.sleep(3)
        try:
            unixname=job[0]
            print("\nGathering for "+unixname)
            
            #collects development page and crawls for yearstats link
            print("Retrieving development HTML.")
            dev_page=utils.get_development(datasource_id,unixname)
            dev_page=dev_page[0]
            if(dev_page):
                print("Finding link.")
                id=statsSpider(dev_page)
                
                #inserts yearstats page into project_indexes
                if(id):
                    print("Inserting yearstats page.")
                    year=utils.get_page("http://"+BASE_SITE+"project/stats/?group_id="+id+"&ugn="+unixname+"&type&mode=alltime")
                else:
                    print("No group id found.")
                    year=None
                    
                if(year and re.search('We apologize.  The page you were looking for cannot be found.',year)==None):
                    i=0
                    while(re.search("Connection to statistics server timed out",year)!=None and i<5):
                        year=utils.get_page("http://"+BASE_SITE+"project/stats/?group_id="+id+"&ugn="+unixname+"&type&mode=alltime")
                        i+=1
                    if(re.search("Connection to statistics server timed out",year)==None):
                        update="UPDATE project_indexes SET all_time_stats_html=%s WHERE datasource_id=%s AND proj_unixname=%s"
                        utils.db_insert(update,year,datasource_id,unixname)
                        #changed gather_resumes
                        utils.change_status('completed','gather_year',datasource_id,unixname)
                        job=utils.get_job(datasource_id,'gather_year')
                        if(utils.error):
                            sys.exit()
                    else:
                        print("!!!!WARNING!!!! yearstats page timed out.")
                        utils.change_status('completed','gather_year',datasource_id,unixname)
                        insert='''INSERT INTO sf_jobs (unixname,datasource_id,status,last_modified)
                        VALUES(%s,%s,%s,NOW())'''
                        utils.db_insert(insert,unixname,datasource_id,'error_year')
                        job=utils.get_job(datasource_id,'gather_year')
                        if(utils.error):
                            sys.exit()
                        
                #if yearstats insertion fails posts error, gets job, and checks for errors
                else:
                    print("yearstats page does not exist.")
                    utils.change_status('completed','gather_year',datasource_id,unixname)
                    job=utils.get_job(datasource_id,'gather_year')
                    if(utils.error):
                        sys.exit()

            
            #if development doesn't collect properly posts error, gets job, and checks for errors
            else:
                print("!!!!WARNING!!!! yearstats page did not collect correctly.")
                utils.post_error('gather_year:\nDevelopment gathering yielded a null response.',datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_year')
                if(utils.error):
                    sys.exit()
        
        #if collecting process fails posts error, gets job, and checks for errors
        except:
            print("!!!!WARNING!!!! yearstats page did not collect correctly.")
            utils.post_error('gather_year:\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_year')
            if(utils.error):
                sys.exit()   
                

