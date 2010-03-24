'''
Created on Mar 1, 2010

This module runs the spidering for the messages for each specific mailing list.

@author: Steven Norris
'''

import sys
import traceback
import time
import re
    
#spiders the links for the messages
def messagesSpider(page):
    links=[]
    try:
        linksRaw=re.findall("<a href='viewMessage\.do.+?'>",page)
        for link in linksRaw:
            link=link[9:len(link)-2]
            link=link.replace("&amp;","&")
            links.append(link)
        return links
    except:
        return None

#Spiders the id of the message from the given link
def messageIdSpider(link):
    try:
        id=re.search("dsMessageId=.+",link)
        id=id.group(0)
        id=id[12:]
        return id
    except:
        return None

#Spiders the id of the discussion from the given link 
def discussionIdSpider(link):
    try:
        id=re.search("dsForumId=.+?&",link)
        id=id.group(0)
        id=id[10:len(id)-1]
        return id
    except:
        return None
    
#This spider finds the next link, if there is one, for the messages.
def nextSpider(page):
    try:
        find=re.compile('&laquo; Previous.+?<span class="nowrap"><a href="(?P<Link>viewForumSummary.do.+?)">Next &raquo;</a>',re.DOTALL)
        link=find.search(page);
        link=link.group("Link")
        link=link.replace("&amp;","&")
        return link
    except:
        return None

#runs the spidering for the mailing lists
def run(utils,datasource_id):
    
    #Gathers specific discussion pages
    print("Gathering Messages Pages")
    
    #Gets Job
    job=utils.get_job(datasource_id,'gather_messages')
    if(utils.error):
        sys.exit()
    while(job!=None):
        
        #Gathers the specific discussion pages for each project
        try:
            unixname=job[0]
            print "Gathering Messages Pages for "+unixname
            print "\tGathering Specific Discussions Pages"
            
            #Gathers specific discussions pages
            specifics=utils.get_discussions_specific(datasource_id,unixname)
    
            if(specifics):

                #Gathers messages for each specific page
                for page in specifics:
                    name=page[1]
                    print "\tGathering for Discussion "+name
                    next=True;
                    page_num=1;
                    page=page[0]
                    while (next):
                        print "\t\tGathering messages for page "+str(page_num)
                        messages=messagesSpider(page);
                        
                        #inserts messages into database
                        if(messages):
                            for link in messages[0:1]:
                                time.sleep(3)
                                mId=messageIdSpider(link)
                                dId=discussionIdSpider(link)
                                print "\t\t\tGathering page for message id "+mId+" at discussion id "+dId+" for project "+unixname
                                print "\t\t\tUsing link "+link
                                message=utils.get_page("http://"+unixname+".tigris.org/ds/"+link)
                                print "\t\t\tInserting into database."
                                insert="""INSERT INTO tg_messages_indexes (unixname,datasource_id,discussion_id,message_id,html,last_modified)
                                VALUES(%s,%s,%s,%s,%s,NOW())"""
                                utils.db_insert(insert,unixname,datasource_id,dId,mId,message)
                                
                            #check for next page and collect accordingly
                            next_link=nextSpider(page);
                            if(next_link):
                                page=utils.get_page("http://"+unixname+".tigris.org/ds/"+next_link)
                                page_num=page_num+1
                            else:
                                next=False;
                                
                        #If messages do not exist, print warning and continue loop
                        else:
                            print "\t\t!! Messages were not found or did not exist for page "+str(page_num) 
                            next_link=nextSpider(page);
                            if(next_link):
                                page=utils.get_page("http://"+unixname+".tigris.org/ds/"+next_link)
                                page_num=page_num+1
                            else:
                                next=False;
                
                #changes status, gets new job, and checks for errors
                utils.change_status('completed','gather_messages',datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_messages')
                if (utils.error):
                    sys.exit()
                  
            #If specific message pages do not exist, print warning, change status, and get new job
            else:
                print "!! Specific discussions pages do not exist."
                utils.change_status('completed','gather_messages',datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_messages')
                if (utils.error):
                    sys.exit()
        
        #If error occurs, print error and get new job
        except:
            utils.post_error('gather_messages: \nMessages did not collect properly. '+traceback.format_exc() ,datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_messages')
            if(utils.error):
                sys.exit()
    
        
        