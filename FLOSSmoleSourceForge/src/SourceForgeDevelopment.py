'''
Created on Sep 28, 2009

This module spiders the development pages for each job and prepares for the developers spidering.

@author: Steven Norris
'''

import re
import sys
import traceback
import time

BASE_INDEX='sourceforge.net/projects/'
BASE_SITE='sourceforge.net/'

#This spider finds the links for the development page
def developmentSpider(page):
    match=re.search('projects/.+?/develop',page)
    if (match!=None):
        return match.group(0)
    else:
        return None

def run(utils,datasource_id,stage):
    #collects the development pages for each job and adds them to sv_indexes
    print("\nGathering development pages.")
    if(stage==0):
        stage='gather_memberlist'
    elif(stage==1):
        stage='gather_60day'
    else:
        stage='gather_mailinglists'
    
    #runs jobs
    job=utils.get_job(datasource_id,'gather_development')
    if(utils.error):
        sys.exit()
    while(job!=None):
        time.sleep(3)
        try:
            unixname=job[0]
            print("\nGathering for "+unixname)
            
            #collects index page and crawls for development link
            print("Retrieving index HTML.")
            index_page=utils.get_index(datasource_id,unixname)
            index_page=index_page[0]
            if(index_page):
                print("Finding link.")
                link=developmentSpider(index_page)
                
                #inserts development page into project_indexes
                if(link):
                    print("Inserting development page.")
                    development=utils.get_page("http://"+BASE_SITE+link)
                else:
                    print("Link to development page not found.")
                    development=None
                if(development and re.search('We apologize.  The page you were looking for cannot be found.',development)==None):
                    update="UPDATE sf_project_indexes SET development_html=%s WHERE datasource_id=%s AND proj_unixname=%s"
                    utils.db_insert(update,development,datasource_id,unixname)
                    utils.change_status(stage,'gather_development',datasource_id,unixname)
                    job=utils.get_job(datasource_id,'gather_development')
                    if(utils.error):
                        sys.exit()
                        
                #if development insertion fails posts error, gets job, and checks for errors
                else:
                    print("!!!!WARNING!!!! Development page did not collect correctly.")
                    utils.post_error('gather_development:\nDevelopment page either did not exist or led to a faulty page.',datasource_id,unixname)
                    job=utils.get_job(datasource_id,'gather_development')
                    if(utils.error):
                        sys.exit()
            
            #if index_page doesn't collect properly posts error, gets job, and checks for errors
            else:
                print("!!!!WARNING!!!! Development page did not collect correctly.")
                utils.post_error('gather_development:\nIndex gathering yielded a null response.',datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_development')
                if(utils.error):
                    sys.exit()
        
        #if collecting process fails posts error, gets job, and checks for errors
        except:
            print("!!!!WARNING!!!! Development page did not collect correctly.")
            utils.post_error('gather_development:\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_development')
            if(utils.error):
                sys.exit()

