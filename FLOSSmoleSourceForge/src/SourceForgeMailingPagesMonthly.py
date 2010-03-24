'''
Created Dec. 13, 2009

This module is used to spider the mailing list pages for message pages and store them in the database.

@author: Steven Norris
'''

import re
import sys
import time
from datetime import date

BASE_INDEX='sourceforge.net/mailarchive/'
BASE_SITE='sourceforge.net/'

def mailing_month(page,yearMonth):
    final_match=None
    matches=re.findall('(forum.php\?forum_name=.+?&amp;max_rows=.+?&amp;style=.+?&amp;viewmonth=.+?)">\((\d+?)\)</a>',page)
    if matches:
        matchSet=matches[0]
        match=matchSet[0]
        num=matchSet[1]
        match=match.replace('&amp;','&')
        final_match=(match[0:match.find('max_rows')+10]+num+
                                 match[match.find('&style='):match.find('&style=')+7]+'flat'+
                                 match[match.find('&viewmonth='):match.find('&viewmonth=')+12]+yearMonth)
    return final_match

def run(utils,datasource_id):
    print('\nGathering message pages.')
    
    #Gather job and check for errors
    job=utils.get_job(datasource_id,'gather_messages')
    if (utils.error):
        sys.exit()
    while(job!=None):
        time.sleep(3)
        unixname=job[0]
        print('\nGathering for '+unixname)
        
        #Retrieve mailinglists page from database
        print("Retrieving Specific Mailing List HTML")
        mailing_pages=utils.get_mailing_specific(datasource_id,unixname)
        if(mailing_pages):
            
            #Gathering links for each year and month
            for page in mailing_pages:
                list=page[0]
                html=page[1]
                print('*Retrieving for '+list)
                today=date.today()
                formated=today.strftime("%Y%m")
                month_link=mailing_month(html,formated)
                if(month_link):
                    
                    #Gather pages for each link
                    year=month_link[len(month_link)-6:len(month_link)-2]
                    month=month_link[len(month_link)-2:]
                    time.sleep(3)
                    print('**Collecting for '+month+':'+year)
                    print('**Using link: '+month_link)
                    page=utils.get_page('http://'+BASE_INDEX+month_link)
                    
                    #Insert each page into databse
                    if(page and re.search('We apologize.  The page you were looking for cannot be found.',page)==None):
                        insert='''INSERT INTO mailing_pages_indexes (proj_unixname,list_name,year,month,messages_html,datasource_id,date_collected)
                                        VALUES (%s,%s,%s,%s,%s,%s,NOW())'''
                        print('**Inserting into database')
                        utils.db_insert(insert,unixname,list,year,month,page,datasource_id)
                        
                    #If page doesn't exist, print warning
                    else:
                        print('**Link '+month_link+ 'either led to a faulty page or did not exist.')
                        
                    
                #If links don't exist, set status, get job, and check for errors
                else:
                    print("*!!Specific Mailing List Pages do not Exist!!.")
                    
            #Change status, get job, and check for errors        
            utils.change_status('gather_60day','gather_messages',datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_messages')
            if(utils.error):
                sys.exit()
        
        #If specific mailing lists don't exist, change status, get job, and check for errors
        else:
            print("!!Specific Mailing Lists do not Exist!!")
            utils.change_status('gather_60day','gather_messages',datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_messages')
            if(utils.error):
                sys.exit()