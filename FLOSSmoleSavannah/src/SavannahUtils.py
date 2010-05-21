'''
Created on Jun 5, 2009

@author: Steven Norris

This module provides basic utilities for the FLOSS mole spiders.
'''
import MySQLdb
#import httplib
import traceback
import urllib2
        
class SavannahUtils:
    
    #forms initial connection with database
    def __init__(self,file_name):
        try:
            dbfile = open(file_name, 'r')
        except:
            raise Exception("Database file error: dbInfo.txt")
        try:
            self.host = dbfile.readline().strip()
            self.port = int(dbfile.readline().strip())
            self.username = dbfile.readline().strip()
            self.password = dbfile.readline().strip()
            self.database = dbfile.readline().strip()
            self.db=MySQLdb.connect(host=self.host, user=self.username, passwd=self.password, db=self.database)
            self.cursor = self.db.cursor()
            self.error=False
        except:
            print("!!!WARNINGS!!! Database connection failed.")
            
    '''
    This method provides the ability to gather a page
    '''
    def get_page(self,url):
        try:
            response = urllib2.urlopen(url)
            html = response.read()
            return html
        except:
            print ("The page request failed.")
       # try:
        #    conn=httplib.HTTPConnection('savannah.gnu.org')
         #   conn.request("GET",url)
          #  resp=conn.getresponse()
           # html_page=resp.read()
            #html_page=str(html_page)
           # conn.close()
           # return html_page
       # except:
        #    print ("!!!WARNING!!! The page request failed.")
    
    
    '''
    This method provides the ability to insert into a database
    '''
    def db_insert(self,query_string,*params):
        try:
            self.cursor.execute(query_string, params) 
        except:
            print("!!!!WARNING!!!! Insertion into "+self.database+" failed.\n")
    
    '''
    This method provides the ability to get a job from the job database.
    '''
    def get_job(self, datasource_id, status):
        lock = '''LOCK TABLE sv_jobs READ, sv_jobs AS t WRITE'''
        select = '''SELECT target_name,GNU_NON,link
            FROM sv_jobs AS t
            WHERE status = %s
            AND datasource_id = %s
            LIMIT 1'''
        update='''UPDATE sv_jobs AS t
        SET status='in_progress', last_modified=NOW() 
        WHERE datasource_id=%s 
        AND target_name=%s 
        AND GNU_NON=%s'''
        unlock = '''UNLOCK TABLES'''
        try:
            self.cursor.execute(lock)
            self.cursor.execute(select, (status,datasource_id))
            result = self.cursor.fetchone()
            self.cursor.execute(update,(datasource_id,result[0],result[1]))
            self.cursor.execute(unlock)
            return result
        except:
            print ("Finding job failed.")
            self.cursor.execute(unlock)
            
    #this method allows for status changes
    def change_status(self,status,previous_stage,datasource_id,target):
        update='''UPDATE sv_jobs 
        SET status=%s, previous_stage=%s, last_modified=NOW() 
        WHERE datasource_id=%s 
        AND target_name=%s'''
        try:
            self.cursor.execute(update,(status,previous_stage,datasource_id,target))
        except:
            print('!!!!WARNING!!!! Status '+status+' did not update correctly for '+target+' '+datasource_id+'.')
            self.error=True
            
    #this method allows for the retrieval of a list of members for a project
    def get_members(self,project_name,datasource_id):
        try:
            gather='''SELECT dev_loginname FROM sv_developer_projects
            WHERE project_name=%s
            AND datasource_id=%s'''
            self.cursor.execute(gather,(project_name,datasource_id))
            return self.cursor.fetchall()
        except:
            print("!!!WARNING!!! Retrieving members failed.")
            
    #this method allows for the retrieval of the membershtml
    def get_member_html(self,project,datasource_id):
        try:
            gather='''SELECT memberhtml FROM sv_project_indexes 
            WHERE project_name=%s AND datasource_id=%s
            LIMIT 1'''
            self.cursor.execute(gather,(project,datasource_id))
            return self.cursor.fetchone()
        except:
            print("!!!WARNING!!! Retrieving memberhtml failed.")
    
    #this method allows for the retrieval of the indexhtml
    def get_index_html(self,project,datasource_id):
        try:
            gather='''SELECT indexhtml FROM sv_project_indexes
            WHERE project_name=%s AND datasource_id=%s
            LIMIT 1'''
            self.cursor.execute(gather,(project,datasource_id))
            return self.cursor.fetchone()
        except:
            print("!!!WARNING!!! Retrieving indexhtml failed.")
    
    #this method allows for the retrieval of the skillshtml
    def get_skills_html(self,username,datasource_id):
        try:
            gather='''SELECT skillshtml FROM sv_developers
            WHERE dev_loginname=%s AND datasource_id=%s
            LIMIT 1'''
            self.cursor.execute(gather,(username,datasource_id))
            return self.cursor.fetchone()
        except:
            print("!!!Warning!!! Retrieving skillshtml failed.")
    
    #this method allows for the retrieval of the infohtml
    def get_info_html(self,username,datasource_id):
        try:
            gather='''SELECT infohtml FROM sv_developers
            WHERE dev_loginname=%s AND datasource_id=%s
            LIMIT 1'''
            self.cursor.execute(gather,(username,datasource_id))
            return self.cursor.fetchone()
        except:
            print("!!!Warning!!! Retrieving skillshtml failed.")
    
    #this method allows for error posting
    def post_error(self,message,target,datasource_id,type):
        update='''UPDATE sv_jobs 
        SET error_msg=%s, status='error', last_modified=NOW()
        WHERE datasource_id=%s
        AND target_name=%s
        AND GNU_NON=%s'''
        gather='''SELECT status FROM sv_jobs
        WHERE datasource_id=%s
        AND target_name=%s
        AND GNU_NON=%s
        LIMIT 1'''
        try:
            self.cursor.execute(gather,(datasource_id,target,type))
            fail_stage=self.cursor.fetchone()
            fail_stage=fail_stage[0]
            message=fail_stage+":\n"+message
            self.cursor.execute(update,(message,datasource_id,target,type))
        except:
            print('!!!!WARNING!!!! Error '+message+'could not be posted to '+target+'.')
            self.error=True
            
    '''
    This method provides the ability to get a job from the job database.
    '''
    def get_cleanup_job(self, datasource_id, status):
        lock = '''LOCK TABLE sv_jobs READ, sv_jobs AS t WRITE'''
        select = '''SELECT target_name,GNU_NON,link
            FROM sv_jobs AS t
            WHERE status = "In_Progress"
            AND previous_stage = %s
            AND datasource_id = %s
            LIMIT 1'''
        update='''UPDATE sv_jobs AS t
        SET status='Clean_Up', last_modified=NOW() 
        WHERE datasource_id=%s 
        AND target_name=%s'''
        unlock = '''UNLOCK TABLES'''
        try:
            self.cursor.execute(lock)
            self.cursor.execute(select, (status,datasource_id))
            result = self.cursor.fetchone()
            self.cursor.execute(update,(datasource_id,result[0]))
            self.cursor.execute(unlock)
            return result
        except:
            print ("Finding job failed.")
            self.cursor.execute(unlock)
            
    #This method allows for the deletion of a project and it's indexes
    def delete_index(self,unixname,datasource_id):
        try:
            update="""DELETE FROM sv_project_indexes WHERE project_name=%s AND datasource_id=%s"""
            update2="""DELETE FROM sv_projects WHERE project_name=%s AND datasource_id=%s"""
            self.cursor.execute(update,(unixname,datasource_id))
            self.cursor.execute(update2,(unixname,datasource_id))
        except:
            print("!!!!WARNING!!!! Deletion of index failed.")
            print (traceback.format_exc())
            
    #This method allows for the deletion of a project's skills indexes
    def delete_skills(self,unixname,datasource_id):
        try:
            update="""DELETE FROM sv_developer_projects WHERE project_name=%s AND datasource_id=%s"""
            self.cursor.execute(update,(unixname,datasource_id))
        except:
            print("!!!!WARNING!!!! Deletion of index failed.")
            print (traceback.format_exc())