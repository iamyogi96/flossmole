'''
Created on Dec 13, 2009

This module collects the mailing list page for each project given a utilities module and datasource_id.

@author: Steven Norris
'''
import re
import sys

import time


BASE_INDEX='sourceforge.net/projects/'
BASE_SITE='sourceforge.net/'

#This parses the mailnglist link from the given page and returns it
def mailinglist_spider(page):
    match=re.search('/mail/\?group_id=.+?"',page)
    if(match!=None):
        return match.group(0)[1:len(match.group(0))-1]
    else:
        return None

#This method works as the main method
def run(utils, datasource_id):
    print('\nGathering mailinglist pages.')
    
    #Gather job and check for errors
    job=utils.get_job(datasource_id,'gather_mailinglists')    
    if (utils.error):
        sys.exit()
    while(job!=None):
        time.sleep(3)
        unixname=job[0]
        print('\nGathering for '+unixname)
        
        #Retrive development page from database
        print("Retrieving Development HTML")
        development_page=utils.get_development(datasource_id,unixname)
        
        if(development_page):
            development_page=development_page[0]
            
            #Parse out link for mailing list and gather page
            print('Finding Link')
            link=mailinglist_spider(development_page)
            if(link):
                print('Inserting Mailinglist Page')
                mailinglist=utils.get_page('http://'+BASE_SITE+link)
            else:
                print('Link to mailing list not found.')
                mailinglist=None
                
            #Insert mailing list page into database
            if(mailinglist and re.search('We apologize.  The page you were looking for cannot be found.',mailinglist)==None):
                update='''INSERT INTO sf_mailing_indexes (mailinglist_html,datasource_id,proj_unixname,date_collected)
                VALUES(%s,%s,%s,NOW())'''
                utils.db_insert(update,mailinglist,datasource_id,unixname)
                utils.change_status('gather_mailinglistsspecific','gather_mailinglists',datasource_id,unixname)                    
                job=utils.get_job(datasource_id,'gather_mailinglists')
                if(utils.error):
                    sys.exit()
            
            #If the page does not exist, post error and get new job
            else:
                print("!!!!WARNING!!!! Mailinglist page did not collect correctly.")
                utils.change_status('gather_mailinglistsspecific','gather_mailinglists',datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_mailinglists')
                if(utils.error):
                    sys.exit()
            
        #if development page does not collect properly, post error and get new job.
        else:
            print("!!!!WARNING!!!! Development  page did not collect correctly.")
            utils.post_error('gather_mailinglists:\nDevelopment gathering yielded a null response.',datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_mailinglists')
            if(utils.error):
                sys.exit()
        
        