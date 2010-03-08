'''
Created on Feb 21, 2010

This module spiders the specific discussion pages for each project in the job database.

@author: Steven Norris
'''

import sys
import traceback
import time
import re

#spiders for the specific discussion page links
def discussionsSpecificSpider(page):
    find=re.compile("<a href='viewForumSummary.+?</a>",re.DOTALL)
    found=find.findall(page)
    if (found):
        names=[]
        links=[]
        id=[]
        for section in found:
            name=re.search("<a href='.+?'>\s+(?P<discussion>(\S+\s*\S+)+)\s+</a>",section)
            name=name.group("discussion")
            names.append(name)
            link=re.search("dsForumId=.+?'>",section)
            link=link.group(0)
            link=link[0:len(link)-2]
            links.append(link)
            id.append(link[10:])
        final=[names,links,id]
        return final
    else:
        return None

#primary method for running spider
def run(utils,datasource_id):
    
    #Gathers specific discussion pages
    print("Gathering Specific Discussion Pages")
    
    #Gets Job
    job=utils.get_job(datasource_id,'gather_discussions_specific')
    if(utils.error):
        sys.exit()
    while(job!=None):
        
        #Gathers specific discussions pages
        try:
            unixname=job[0]
            print "Gathering Specific Discussion Pages for "+unixname
            print "\tGathering Discussions Pages"
            discussions=utils.get_discussions(datasource_id,unixname)
            #spiders links from discussions page and inserts specific discussions pages
            discussions=discussions[0]
            if(discussions):
                if (re.search("No discussions available to view",discussions)==None):
                    discussionsSpecific=discussionsSpecificSpider(discussions)
                    
                    #finds pages and adds to database
                    if (discussionsSpecific):
                        names=discussionsSpecific[0]
                        links=discussionsSpecific[1]
                        id=discussionsSpecific[2]
                        x=0
                        while(x<len(names)):
                            print("\tGathering page for "+names[x])
                            time.sleep(3)
                            specificsPage=utils.get_page("http://"+unixname+".tigris.org/ds/viewForumSummary.do?"+links[x]+"&countPerPage=1000")
                            if (specificsPage):
                                print("\tInserting Into Database")
                                insert="""INSERT INTO tg_discussions_indexes (unixname,discussion_id,discussion_name,html,last_modified,datasource_id)
                                VALUES(%s,%s,%s,%s,NOW(),%s)"""
                                utils.db_insert(insert,unixname,id[x],names[x],specificsPage,datasource_id)
                            else:
                                print ("\t\t!!!!WARNING!!!! Specific discussions page could not be found for "+names[x])
                            x+=1
                            
                        #changes status, gets new job, and checks for errors
                        utils.change_status('gather_messages',datasource_id,unixname)
                        job=utils.get_job(datasource_id,'gather_discussions_specific')
                        if (utils.error):
                            sys.exit()
                            
                    #If specific pages could not be collected, post errors and get new job
                    else:
                        print "\t!!!!WARNING!!!! Specific discussions pages could not be found for "+unixname
                        utils.post_error('gather_discussions_specific: \nSpecific discussions pages could not be collected.',datasource_id,unixname)
                        job=utils.get_job(datasource_id,'gather_discussions_specific')
                        if(utils.error):
                            sys.exit()
                
                #if discussions holds no specific discussions, post warning and get new job
                else:
                    print "\t!!Warning No specific discussions existed for "+unixname
                    utils.change_status('gather_messages',datasource_id,unixname)
                    job=utils.get_job(datasource_id,'gather_discussions_specific')
                    if(utils.error):
                        sys.exit() 
                    
            #if discussions page is not found, posts warning and gets new job
            else:
                print "\t!!Warning Discussions page could not be collected or did not exist for "+unixname
                utils.change_status('gather_messages',datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_discussions_specific')
                if(utils.error):
                    sys.exit()
                    
        #if collection fails entirely, posts error and gets new job
        except:
            print("!!!!WARNING!!! Discussions collection failed")
            utils.post_error('gather_discussions:\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_discussions_specific')
            if(utils.error):
                sys.exit()

