'''
Created on May 2, 2010

@author: StevenNorris
'''

import SavannahParsers
import sys
import traceback

def run(utils,data_source_id):
    
    #Parses indexes for projects
    print("\nParsing Indexes")
    job=utils.get_job(data_source_id,'indexparsing')
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
            utils.change_status('skillsparsing','indexparsing',data_source_id,job[0])
            job=utils.get_job(data_source_id,'indexparsing')
            if (utils.error):
                sys.exit()
        
        #posts error in case of faulty index parsing
        except:
            print('!!!!WARNING!!!! Index pages did not parse correctly.')
            utils.post_error(traceback.format_exc(),job[0],data_source_id,job[1])
            job=utils.get_job(data_source_id,'indexparsing')
            if (utils.error):
                sys.exit()
                
    #parses skills pages for projects
    print("\nParsing Skills")
    job=utils.get_job(data_source_id,'skillsparsing')
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
                utils.change_status('completed','skillsparsing',data_source_id,job[0])
                
            #gathers new job and checks for errors
            job=utils.get_job(data_source_id,'skillsparsing')
            if (utils.error):
                sys.exit()
        
        #posts error in case of faulty skills parsing
        except:
            print('!!!!WARNING!!!! Skills pages did not parse correctly.')
            utils.post_error(traceback.format_exc(),job[0],data_source_id,job[1])
            job=utils.get_job(data_source_id,'skillsparsing')
            if (utils.error):
                sys.exit()