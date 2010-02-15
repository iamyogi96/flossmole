'''
Created on Feb 14, 2010

This module collects the donor page for each project.

@author: Steven Norris
'''

import re
import sys
import traceback
import time

BASE_SITE='sourceforge.net/'

#The spiders the given page for the donors link
def donorsSpider(html):
    matches=re.search('project/project_donations\.php\?group_id=.+?"',html)
    if(matches!=None):
        match=matches.group(0)
        link=match[0:len(match)-1]
        return link
    else:
        return None

#This runs the spidering for the donors pages and adds them to project_indexes
def run(utils,datasource_id):
    
    print("\nGathering donor pages.")
    
    #runs jobs
    job=utils.get_job(datasource_id,"gather_donors")
    if(utils.error):
        sys.exit()
    while(job!=None):
        time.sleep(3)
        try:
            unixname=job[0]
            print("\nGathering for "+unixname)
            
            #Collects index page and spiders for link
            print("Retrieving index HTML")
            index=utils.get_index(datasource_id,unixname)
            if(index):
                index=index[0]
                print("Finding Link")
                link=donorsSpider(index)
                
                #Gathering page and inserting into database
                if(link):
                    print("Gathering page and inserting into database.")
                    donors=utils.get_page("http://"+BASE_SITE+link)
                else:
                    print("Link was not found.")
                    donors=None
                
                if(donors and re.search('We apologize.  The page you were looking for cannot be found.',donors)==None):
                    update="UPDATE project_indexes SET donors_html=%s WHERE datasource_id=%s AND proj_unixname=%s"
                    utils.db_insert(update,donors,datasource_id,unixname)
                    utils.change_status('gather_mailinglists',datasource_id,unixname)
                    
                    #change gather_60day
                    job=utils.get_job(datasource_id,'gather_donors')
                    if(utils.error):
                        sys.exit()
                        
                #if donors insertion fails posts error, gets job, and checks for errors
                else:
                    print("!! Donors page either does not exist or did not collect properly.")
                    utils.change_status('gather_mailinglists',datasource_id,unixname)
                    job=utils.get_job(datasource_id,'gather_donors')
                    if(utils.error):
                        sys.exit()
                                    
                
            #if development doesn't collect properly posts error, gets job, and checks for errors
            else:
                print("!!!!WARNING!!!! Donors page did not collect correctly.")
                utils.post_error('gather_memberlist:\nIndex gathering yielded a null response.',datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_donors')
                if(utils.error):
                    sys.exit()
        
        #if collecting process fails posts error, gets job, and checks for errors
        except:
            print("!!!!WARNING!!!! Memberlist page did not collect correctly.")
            utils.post_error('gather_memberlist:\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_donors')
            if(utils.error):
                sys.exit()   
