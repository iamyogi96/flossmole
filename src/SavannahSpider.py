'''
Created on May 26, 2009

@author: Steven Norris

This program runs as a spider for the the savannah.gnu.org to add information about
both the GNU projects and non-GNU projects to a database for further investigation.

RUN INSTRUCTIONS
Run from command line using this format
[Interpret] SavannahSpider.py [DatasourceID] [Test mode True/False]

Test mode is based on string comparison so make sure capitalization and spelling are exact.
'''
from HTMLParser import HTMLParser
import httplib
import re
import time
from FLOSSmoleutils import FLOSSmoleutils
import SavannahParsers
import sys
import traceback

BASE_SITE='savannah.gnu.org'
BASE_SITE2='savannah.nongnu.org'

'''
This spider gathers the members list for each projects page
'''
class SpiderSavannahMembersList(HTMLParser):
    
    check_link=''
    
    #handles the start tag for the memberslist link and sets it to check_link
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            link=attrs[0][1]
            if re.search('memberlist.php',link)!=None:
                self.check_link=link
                
'''
This spider handles the skills pages in each members page
'''
class SpiderSavannahSkills(HTMLParser):
    
    check_links=[]
  
    #handles the start tag for each skills page and adds it to check_links
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            link=attrs[0][1]
            if re.search('resume.php',link)!=None:
                self.check_links.append(link)

'''
This class allows for the collection of usernames from the skills pages
'''
class User_Name_Spider(HTMLParser):
    
    check_links=[]
    
    #handles the start tag for each user name and returns it
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            link=attrs[0][1]
            if re.search("/users",link)!=None:
                self.check_links.append(link)
       
'''
Runs the spiders for savannah.gnu.org
'''
def main(argv):
    
    try:
        data_source_id=argv[1]
        test=argv[2]
    except:
        print("Format arguments thusly: [program] [datasource_id] [True/False(TestMode)]")
        sys.exit()
        
    #checks for test mode
    if(test=='True'):
        utils=FLOSSmoleutils("dbInfoTest.txt")
    else:
        utils=FLOSSmoleutils("dbInfo.txt")
        
    #creates needed spiders
    spiderMembers=SpiderSavannahMembersList()
    spiderSkills=SpiderSavannahSkills()
    spiderUserName=User_Name_Spider()
    
    #Does the index collection jobs for GNU projects
    print("\nGathering for GNU projects.")
    job=utils.get_job(data_source_id,'indexHTML','GNU')
    if(utils.error):
        sys.exit()
    while(job!=None):
        try:
            link=job[2]
            type=job[1]
            project_name=job[0]
            print("Gathering data for "+link+".")
            
            #gets the home page for each project
            print("Gathering home page.")
            page=utils.get_page('http://'+BASE_SITE+link)
            if(page):
                home_page=str(page)
                
                #finds the members page for the project
                print("Gathering members page.")
                spiderMembers.feed(home_page)
                members_page=utils.get_page('http://'+BASE_SITE+spiderMembers.check_link)
                if(page):
                    members_page=str(members_page)
                    
                    #Insert the homepage and members page into sv_project_indexes
                    print("Inserting into sv_project_indexes.")
                    insert='''INSERT INTO sv_project_indexes (
                    project_name,datasource_id,indexhtml,memberhtml,date_collected)
                    VALUES(%s,%s,%s,%s,NOW())'''
                    utils.db_insert(insert,project_name,data_source_id,home_page,members_page)
                    
                    #Insert the type into sv_projects
                    print("Inserting into sv_projects.")
                    insert='''INSERT INTO sv_projects (
                    project_name,datasource_id,gnu_or_non,date_collected)
                    VALUES(%s,%s,%s,NOW())'''
                    utils.db_insert(insert,project_name,data_source_id,type)
                    
                    #sleeps then status change and select new job while checking for fatal errors
                    time.sleep(3)
                    utils.change_status('skillsHTML',data_source_id,project_name,type)
                    job=utils.get_job(data_source_id,'indexHTML','GNU')
                    if (utils.error):
                        sys.exit()
                else:
                    print("!!!!WARNING!!!! Index gathering failed for "+project_name)
                    utils.post_error(traceback.format_exc(),project_name,data_source_id,type)
                    job=utils.get_job(data_source_id,'indexHTML','GNU')
                    if(utils.error):
                        sys.exit()
            else:
                print("!!!!WARNING!!!! Index gathering failed for "+project_name)
                utils.post_error(traceback.format_exc(),project_name,data_source_id,type)
                job=utils.get_job(data_source_id,'indexHTML','GNU')
                if(utils.error):
                    sys.exit()
                    
        #posting error for faulty gathering    
        except:
            print("!!!!WARNING!!!! Index gathering failed for "+project_name+".")
            utils.post_error(traceback.format_exc(),project_name,data_source_id,type)
            job=utils.get_job(data_source_id,'indexHTML','GNU')
            if(utils.error):
                sys.exit()
                
    #Does the skills page collection for the GNU projects
    print("\nGathering skills pages for GNU")
    job=utils.get_job(data_source_id,'skillsHTML','GNU')
    if (utils.error):
        sys.exit()
    while (job!=None):
        try:
            error=False
            member_html=utils.get_member_html(job[0],data_source_id)
            member_html=member_html[0]
            spiderSkills.feed(member_html)
            
            #collects the skill pages for each member
            print("Gathering skills pages for "+job[0])
            for link in spiderSkills.check_links:
                print("finding skills page at "+link)
                dev_id=link[27:]
                skills_page=utils.get_page('http://'+BASE_SITE+link)
                if(page):
                    skills_page=str(skills_page)
                    spiderUserName.feed(skills_page)
                    user_name=spiderUserName.check_links[0]
                    info_page=utils.get_page('http://'+BASE_SITE+user_name)
                    if(info_page):
                        info_page=str(info_page)
                        user_name=user_name[7:]
                        spiderUserName.check_links=[]
                        
                        
                        print("Inserting for "+user_name+" on project "+job[0])
                        #Insert the developer into sv_developers
                        print("Inserting into sv_developers.")
                        insert='''INSERT IGNORE INTO sv_developers (datasource_id,dev_loginname,developer_id,skillshtml,infohtml,date_collected)
                        VALUES(%s,%s,%s,%s,%s,NOW())'''
                        utils.db_insert(insert,data_source_id,user_name,dev_id,skills_page,info_page)
                        
                        #Insert the developer into sv_developers_projects
                        print("Inserting into sv_developer_projects.")
                        insert='''INSERT INTO sv_developer_projects (datasource_id,dev_loginname,project_name,date_collected)
                        VALUES(%s,%s,%s,NOW())'''
                        utils.db_insert(insert,data_source_id,user_name,job[0])
                    else:
                        print('!!!!WARNING Skills pages did not collect correctly!!!!')
                        utils.post_error(traceback.format_exc(),job[0],data_source_id,job[1])
                        if(sys.error):
                            sys.exit()
                        error=True
                else:
                    print('!!!!WARNING Skills pages did not collect correctly!!!!')
                    utils.post_error(traceback.format_exc(),job[0],data_source_id,job[1])
                    if(sys.error):
                        sys.exit()
                    error=True
                    
            #refresh links, sleep, change status, get new job, and check for errors
            spiderSkills.check_links=[]
            time.sleep(3)
            if(not error):
                utils.change_status('indexparsing',data_source_id,job[0],job[1])
            job=utils.get_job(data_source_id,'skillsHTML','GNU')
            if (utils.error): 
                sys.exit()
        
        #posts errors in case of faulty skills gathering
        except:
            print('!!!!WARNING!!!! Skills pages did not collect correctly.')
            utils.post_error(traceback.format_exc(),job[0],data_source_id,job[1])
            job=utils.get_job(data_source_id,'skillsHTML','GNU')
            if (utils.error):
                sys.exit()
                
    #Does all index collection jobs for NON-GNU projects
    print("\nGathering for NON-GNU projects.")
    job=utils.get_job(data_source_id,'indexHTML','NONGNU')
    if (utils.error):
        sys.exit()
    while(job!=None):
        try:
            link=job[2]
            type=job[1]
            project_name=job[0]
            print("Gathering data for "+link+".")
            
            #gets the home page for each project
            print("Gathering home page.")
            page=utils.get_page('http://'+BASE_SITE2+link)
            if(page):
                home_page=str(page)
                
                #finds the members page for the project
                print("Gathering members page.")
                spiderMembers.feed(home_page)
                members_page=utils.get_page('http://'+BASE_SITE2+spiderMembers.check_link)
                if(page):
                    members_page=str(members_page)
                    
                    #Insert the homepage and members page into sv_project_indexes
                    print("Inserting into sv_project_indexes.")
                    insert='''INSERT INTO sv_project_indexes (
                    project_name,datasource_id,indexhtml,memberhtml,date_collected)
                    VALUES(%s,%s,%s,%s,NOW())'''
                    utils.db_insert(insert,project_name,data_source_id,home_page,members_page)
                    
                    #Insert the type into sv_projects
                    print("Inserting into sv_projects.")
                    insert='''INSERT INTO sv_projects (
                    project_name,datasource_id,gnu_or_non,date_collected)
                    VALUES(%s,%s,%s,NOW())'''
                    utils.db_insert(insert,project_name,data_source_id,type)
                    
                    #sleep, change status, get new job, and check for fatal errors
                    time.sleep(3)
                    utils.change_status('skillsHTML',data_source_id,project_name,type)
                    job=utils.get_job(data_source_id,'indexHTML','NONGNU')
                    if (utils.error):
                        sys.exit()
                else:
                    print('!!!!WARNING!!!! Index gathering failed for '+project_name+'.')
                    utils.post_error(traceback.format_exc(),project_name,data_source_id,type)
                    job=utils.get_job(data_source_id,'indexHTML','NONGNU')
                    if(utils.error):
                        sys.exit()
            else:
                print('!!!!WARNING!!!! Index gathering failed for '+project_name+'.')
                utils.post_error(traceback.format_exc(),project_name,data_source_id,type)
                job=utils.get_job(data_source_id,'indexHTML','NONGNU')
                if(utils.error):
                    sys.exit()
            
        #post error in case of faulty index gathering
        except:
            print("!!!!WARNING!!!! Index gathering failed for "+project_name+".")
            utils.post_error(traceback.format_exc(),project_name,data_source_id,type)
            job=utils.get_job(data_source_id,'indexHTML','NONGNU')
            if (utils.error):
                sys.exit()
                
    #Does the skills page collection for the NONGNU projects
    print("\nGathering skills pages for NONGNU.")
    job=utils.get_job(data_source_id,'skillsHTML','NONGNU')
    if (utils.error):
        sys.exit()
    while (job!=None):
        try:
            error=False
            member_html=utils.get_member_html(job[0],data_source_id)
            member_html=member_html[0]
            spiderSkills.feed(member_html)
            
            #collects the skill pages for each member
            print("Gathering skills pages for "+job[0])
            for link in spiderSkills.check_links:
                print("finding skills page at "+link)
                dev_id=link[27:]
                skills_page=utils.get_page('http://'+BASE_SITE2+link)
                if(page):
                    skills_page=str(skills_page)
                    spiderUserName.feed(skills_page)
                    user_name=spiderUserName.check_links[0]
                    info_page=utils.get_page('http://'+BASE_SITE2+user_name)
                    if(page):
                        info_page=str(info_page)
                        user_name=user_name[7:]
                        spiderUserName.check_links=[]
                        
                        print("Inserting for "+user_name+" on project "+job[0])
                        #Insert the type into sv_developers
                        print("Inserting into sv_developers.")
                        insert='''INSERT IGNORE INTO sv_developers (datasource_id,dev_loginname,developer_id,skillshtml,infohtml,date_collected)
                        VALUES(%s,%s,%s,%s,%s,NOW())'''
                        utils.db_insert(insert,data_source_id,user_name,dev_id,skills_page,info_page)
                        
                        #Insert the type into sv_developers_projects
                        print("Inserting into sv_developer_projects.")
                        insert='''INSERT INTO sv_developer_projects (datasource_id,dev_loginname,project_name,date_collected)
                        VALUES(%s,%s,%s,NOW())'''
                        utils.db_insert(insert,data_source_id,user_name,job[0])
                    else:
                       print('!!!!WARNING!!!! Skills pages did not collect correctly.')
                       utils.post_error(traceback.format_exc(),job[0],data_source_id,job[1])
                       if(utils.error):
                           sys.exit()
                       error=True 
                else:
                    print('!!!!WARNING!!!! Skills pages did not collect correctly.')
                    utils.post_error(traceback.format_exc(),job[0],data_source_id,job[1])
                    if(utils.error):
                        sys.exit()
                    error=True
                    
            #refreshes links, sleeps, changes status, gets new job, and checks for fatal errors
            spiderSkills.check_links=[]
            time.sleep(3)
            if(not error):
                utils.change_status('indexparsing',data_source_id,job[0],job[1])
            job=utils.get_job(data_source_id,'skillsHTML','NONGNU')
            if(utils.error):
                sys.exit()
            
        #posts error in case of faulty skills collection
        except:
            print('!!!!WARNING!!!! Skills pages did not collect correctly.')
            utils.post_error(traceback.format_exc(),job[0],data_source_id,job[1])
            job=utils.get_job(data_source_id,'skillsHTML','GNU')
            if (utils.error):
                sys.exit()
                
    #Parses indexes for GNU projects
    print("\nParsing Indexes for GNU.")
    job=utils.get_job(data_source_id,'indexparsing','GNU')
    if (utils.error):
        sys.exit()
    while (job!=None):
        try:
            #parses and updates database
            print("Parsing for "+job[0])
            index_html=utils.get_index_html(job[0],data_source_id)
            index_html=index_html[0]
            description=SavannahParsers.parse_index(index_html)
            id_num=SavannahParsers.parse_project_id(index_html)
            dev_count=SavannahParsers.parse_member_num(index_html)
            long_name=SavannahParsers.parse_project_longname(index_html)
            group=SavannahParsers.parse_group_type(index_html)
            mail=SavannahParsers.parse_mailing_lists(index_html)
            bugs=SavannahParsers.parse_bugs(index_html)
            tech=SavannahParsers.parse_tech(index_html)
            looking=SavannahParsers.parse_looking(index_html)
            task=SavannahParsers.parse_task(index_html)
            patch=SavannahParsers.parse_patch(index_html)
            license=SavannahParsers.parse_license(index_html)
            status=SavannahParsers.parse_dev_status(index_html)
            update='''UPDATE sv_projects
            SET description=%s, 
            id_num=%s,
            project_dev_count=%s,
            project_long_name=%s,
            project_group_type=%s,
            number_of_mailing_lists=%s,
            bugs_open=%s,
            bugs_total=%s,
            techsupp_open=%s,
            techsupp_total=%s,
            looking_for_number=%s,
            taskmgr_open=%s,
            taskmgr_total=%s,
            patchmgr_open=%s,
            patchmgr_total=%s,
            license=%s,
            development_status=%s,
            date_collected=NOW()
            WHERE datasource_id=%s
            AND project_name=%s
            AND gnu_or_non=%s'''
            utils.db_insert(update,description,id_num,dev_count,long_name,group,mail,bugs[0],bugs[1],tech[0],tech[1],looking,
                            task[0],task[1],patch[0],patch[1],license,status,data_source_id,job[0],job[1])
            
            #change status, get new job, and check for errors
            utils.change_status('skillsparsing',data_source_id,job[0],job[1])
            job=utils.get_job(data_source_id,'indexparsing','GNU')
            if (utils.error):
                sys.exit()
        
        #posts error in case of faulty index parsing
        except:
            print('!!!!WARNING!!!! Index pages did not parse correctly.')
            utils.post_error(traceback.format_exc(),job[0],data_source_id,job[1])
            job=utils.get_job(data_source_id,'indexparsing','GNU')
            if (utils.error):
                sys.exit()
                
    #parses skills pages for GNU projects
    print("\nParsing Skills for GNU.")
    job=utils.get_job(data_source_id,'skillsparsing','GNU')
    if (utils.error):
        sys.exit()
    while (job!=None):
        try:
            #gathers a list of members
            members=utils.get_members(job[0],data_source_id)
            error=False
            for member in members:
                error=False
                try:
                    #parses name and description for each member, then updates database
                    member=member[0]
                    print("Parsing for "+member+" for project "+job[0])
                    skillshtml=utils.get_skills_html(member,data_source_id)
                    skillshtml=skillshtml[0]
                    name=SavannahParsers.parse_member_name(skillshtml)
                    description=SavannahParsers.parse_member_description(skillshtml)
                    infohtml=utils.get_info_html(member,data_source_id)
                    infohtml=infohtml[0]
                    member_since=SavannahParsers.parse_time(infohtml)
                    update='''UPDATE sv_developers SET real_name=%s, description=%s, member_since=%s, date_collected=NOW() 
                    WHERE dev_loginname=%s
                    AND datasource_id=%s'''
                    utils.db_insert(update,name,description,member_since,member,data_source_id)
                    
                    #parses skills for each member then updates database
                    skill_sets=SavannahParsers.parse_skills(skillshtml)
                    for skillset in skill_sets:
                        insert='''INSERT IGNORE INTO sv_dev_skills (datasource_id,dev_loginname,skill,level,experience,date_collected)
                        VALUES(%s,%s,%s,%s,%s,NOW())'''  
                        utils.db_insert(insert,data_source_id,member,skillset[0],skillset[1],skillset[2])
                
                #posts error in case of faulty member parsing
                except:
                    print('!!!!WARNING!!!! Skills pages did not parse correctly.')
                    utils.post_error(traceback.format_exc(),job[0],data_source_id,job[1])
                    error=True
                    if (utils.error):
                        sys.exit()
            
            #checks for faulty parsing on one member, so as not to change error status if it exists
            if(not error):
                utils.change_status('completed',data_source_id,job[0],job[1])
                
            #gathers new job and checks for errors
            job=utils.get_job(data_source_id,'skillsparsing','GNU')
            if (utils.error):
                sys.exit()
        
        #posts error in case of faulty skills parsing
        except:
            print('!!!!WARNING!!!! Skills pages did not parse correctly.')
            utils.post_error(traceback.format_exc(),job[0],data_source_id,job[1])
            job=utils.get_job(data_source_id,'skillsparsing','GNU')
            if (utils.error):
                sys.exit()


    #parses indexes for NONGNU projects            
    print("\nParsing Indexes for NONGNU.")
    job=utils.get_job(data_source_id,'indexparsing','NONGNU')
    if (utils.error):
        sys.exit()
    while (job!=None):
        try:
            #parses index and updates database
            print("Parsing for "+job[0])
            index_html=utils.get_index_html(job[0],data_source_id)
            index_html=index_html[0]
            description=SavannahParsers.parse_index(index_html)
            id_num=SavannahParsers.parse_project_id(index_html)
            dev_count=SavannahParsers.parse_member_num(index_html)
            long_name=SavannahParsers.parse_project_longname(index_html)
            group=SavannahParsers.parse_group_type(index_html)
            mail=SavannahParsers.parse_mailing_lists(index_html)
            bugs=SavannahParsers.parse_bugs(index_html)
            tech=SavannahParsers.parse_tech(index_html)
            looking=SavannahParsers.parse_looking(index_html)
            task=SavannahParsers.parse_task(index_html)
            patch=SavannahParsers.parse_patch(index_html)
            license=SavannahParsers.parse_license(index_html)
            status=SavannahParsers.parse_dev_status(index_html)
            update='''UPDATE sv_projects
            SET description=%s, 
            id_num=%s,
            project_dev_count=%s,
            project_long_name=%s,
            project_group_type=%s,
            number_of_mailing_lists=%s,
            bugs_open=%s,
            bugs_total=%s,
            techsupp_open=%s,
            techsupp_total=%s,
            looking_for_number=%s,
            taskmgr_open=%s,
            taskmgr_total=%s,
            patchmgr_open=%s,
            patchmgr_total=%s,
            license=%s,
            development_status=%s,
            date_collected=NOW()
            WHERE datasource_id=%s
            AND project_name=%s
            AND gnu_or_non=%s'''
            utils.db_insert(update,description,id_num,dev_count,long_name,group,mail,bugs[0],bugs[1],tech[0],tech[1],looking,
                            task[0],task[1],patch[0],patch[1],license,status,data_source_id,job[0],job[1])
            
            #changes status, gets new job, and checks for errors
            utils.change_status('skillsparsing',data_source_id,job[0],job[1])
            job=utils.get_job(data_source_id,'indexparsing','NONGNU')
            if (utils.error):
                sys.exit()
        
        #posts error in case of faulty index parsing
        except:
            print('!!!!WARNING!!!! Index pages did not parse correctly.')
            utils.post_error(traceback.format_exc(),job[0],data_source_id,job[1])
            job=utils.get_job(data_source_id,'indexparsing','NONGNU')
            if (utils.error):
                sys.exit()
    
    #parses skills for NONGNU projects
    print("\nParsing Skills for NONGNU.")
    job=utils.get_job(data_source_id,'skillsparsing','NONGNU')
    if (utils.error):
        sys.exit()
    while (job!=None):
        try:
            #gathers list of members from database
            members=utils.get_members(job[0],data_source_id)
            error=False
            for member in members:
                error=False
                try:
                    
                    #parses name and description of each member and updates database
                    member=member[0]
                    print('Parsing for '+member+' for project '+job[0])
                    skillshtml=utils.get_skills_html(member,data_source_id)
                    skillshtml=skillshtml[0]
                    name=SavannahParsers.parse_member_name(skillshtml)
                    description=SavannahParsers.parse_member_description(skillshtml)
                    infohtml=utils.get_info_html(member,data_source_id)
                    infohtml=infohtml[0]
                    member_since=SavannahParsers.parse_time(infohtml)
                    update='''UPDATE sv_developers SET real_name=%s, description=%s, member_since=%s, date_collected=NOW() 
                    WHERE dev_loginname=%s
                    AND datasource_id=%s'''
                    utils.db_insert(update,name,description,member_since,member,data_source_id)
                    skill_sets=SavannahParsers.parse_skills(skillshtml)
                    
                    #parses skills for each member
                    for skillset in skill_sets:
                        insert='''INSERT IGNORE INTO sv_dev_skills (datasource_id,dev_loginname,skill,level,experience,date_collected)
                        VALUES(%s,%s,%s,%s,%s,NOW())'''  
                        utils.db_insert(insert,data_source_id,member,skillset[0],skillset[1],skillset[2])
                
                #posts error in case of faulty member parsing
                except:
                    print('!!!!WARNING!!!! Skills pages did not parse correctly.')
                    utils.post_error(traceback.format_exc(),job[0],data_source_id,job[1])
                    error=True
                    if (utils.error):
                        sys.exit()
            
            #checks for individual member parsing error so as to not overwrite error status
            if(not error):
                utils.change_status('completed',data_source_id,job[0],job[1])
                
            #gets new job and checks for errors
            job=utils.get_job(data_source_id,'skillsparsing','NONGNU')
            if (utils.error):
                sys.exit()
        
        #posts error in case of faulty skills parsing
        except:
            print('!!!!WARNING!!!! Skills pages did not parse correctly.')
            utils.post_error(traceback.format_exc(),job[0],data_source_id,job[1])
            job=utils.get_job(data_source_id,'skillsparsing','NONGNU')
            if (utils.error):
                sys.exit()
                
    print("Process Completed.")
    
def test():
    select='SELECT project_name, indexhtml FROM sv_project_indexes WHERE datasource_id=0'
    utils=FLOSSmoleutils('dbInfoTest.txt')
    utils.cursor.execute(select,)
    results=utils.cursor.fetchall()
    for result in results:
        name=result[0]
        index=result[1]
        parsed=SavannahParsers.parse_project_longname(index)
        print ('Name: '+name)
        print(parsed)

main(sys.argv)
    