'''
Created on Dec 13, 2009

This module is used to spider the main mailing list page for each project and insert it's subsequent specific mailing list pages into the database.

@author: Steven Norris
'''
import re
import sys

import time


BASE_INDEX='sourceforge.net/projects/'
BASE_SITE='sourceforge.net/'

#This method spiders the main mailing list page for specific mailing list links
def mailinglists_spider(page):
    matches=[]
    start_matches=re.findall('/mailarchive/forum.php\?forum_name=.+?>',page)
    if(start_matches):
        for match in start_matches:
            if matches.count(match[1:len(match)-2]  )==0:
                matches.append(match[1:len(match)-2])
        return matches
    
    else:
        return None

#This method runs the main spidering for the module
def run(utils,datasource_id,complete):
    print('\nGathering specific mailinglist pages.')
    
    #Gather job and check for errors
    if(complete):
        job=utils.get_mailing_job(datasource_id,'gathering_mailinglistsspecific')
    else:
        job=utils.get_job(datasource_id,'gather_mailinglistsspecific')
    if (utils.error):
        sys.exit()
    while(job!=None):
        time.sleep(3)
        unixname=job[0]
        print('\nGathering for '+unixname)
        
        #Retrive mailinglists page from database
        print("Retrieving Mailinglists HTML")
        mailing_page=utils.get_mailing(datasource_id,unixname)
        if(mailing_page):
            mailing_page=mailing_page[0]
                    
            #Parse out links for mailing listss
            print('Finding Links')
            links=mailinglists_spider(mailing_page)
            
            #Gather pages for each link
            if(links):
                for link in links:
                    print('Inserting Mailinglist Page '+link)
                    name=link[33:]
                    mailinglist=utils.get_page('http://'+BASE_SITE+link)
                    
                    #Insert page into database
                    if(mailinglist and re.search('We apologize.  The page you were looking for cannot be found.',mailinglist)==None):
                        update='''INSERT INTO mailinglist_indexes  (proj_unixname,mailinglist_html, datasource_id, list_name,date_collected)
                        VALUES(%s,%s,%s,%s,NOW())'''
                        utils.db_insert(update,unixname,mailinglist,datasource_id,name)
                    
                    #Print warning if page does not exist
                    else:
                        print('Link '+link+ 'either led to a faulty page or did not exist.')
                        
                #Change status, get job, and check for errors
                if(complete):
                    utils.change_mailing_status('gathering_messages',datasource_id,unixname)
                    job=utils.get_mailing_job(datasource_id,'gathering_mailinglistsspecific')
                else:
                    utils.change_status('gather_messages',datasource_id,unixname)
                    job=utils.get_job(datasource_id,'gather_mailinglistsspecific')
                if(utils.error):
                    sys.exit()
            
            #Print warning if links do not exist
            else:
                print("!!Specific Mailing Lists do not Exist!!.")
                if(complete):
                    utils.change_mailing_status('gathering_messages',datasource_id,unixname)
                    job=utils.get_mailing_job(datasource_id,'gathering_mailinglistsspecific')
                else:
                    utils.change_status('gather_messages',datasource_id,unixname)
                    job=utils.get_job(datasource_id,'gather_mailinglistsspecific')
                if(utils.error):
                    sys.exit()
                    
        #if development page does not collect properly, post error and get new job.
        else:
            print("!!!!WARNING!!!! Mailinglist page did not collect correctly.")
            if(complete):
                utils.post_mailing_error('gathering_mailinglistsspecific:\nMailinglist gathering yielded a null response.',datasource_id,unixname)
                job=utils.get_mailing_job(datasource_id,'gathering_mailinglistsspecific')
            else:
                utils.change_status('gather_messages',datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_mailinglistsspecific')
            if(utils.error):
                sys.exit()
        