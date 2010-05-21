'''
Created on Jun 5, 2009

@author: Steven Norris

This module provides basic utilities for the FLOSS mole spiders.
'''
import MySQLdb
import httplib
import traceback

class GitHubutils:
    
    #this gathers the initial connection to the database
    def __init__(self,file_name):
        try:
            dbfile = open(file_name, 'r')
        except:
            raise Exception("Database file error: dbinfo.txt")
        self.host = dbfile.readline().strip()
        self.port = int(dbfile.readline().strip())
        self.username = dbfile.readline().strip()
        self.password = dbfile.readline().strip()
        self.database = dbfile.readline().strip()
        self.db=MySQLdb.connect(host=self.host, user=self.username, passwd=self.password, db=self.database)
        self.cursor = self.db.cursor()
        self.error=False
        
    '''
    This method provides the ability to gather a page
    '''
    def get_page(self,url):
        try:
            conn=httplib.HTTPConnection('github.com')
            conn.request("GET",url)
            resp=conn.getresponse()
            html_page=resp.read()
            html_page=str(html_page)
            conn.close()
            return html_page
        except:
            print ("The page request failed.")
    
    '''
    This method provides the ability to insert into a database
    '''
    def db_insert(self,query_string,*params):
        try:
            self.cursor.execute(query_string, params) 
        except:
            print("!!!!WARNING!!!! Insertion into "+self.database+" failed.")
            print(traceback.format_exc())
            
    '''
    This method provides the ability to get a job from the job database.
    '''
    def get_job(self, datasource_id, status):
        lock = '''LOCK TABLE gh_jobs READ, gh_jobs AS t WRITE'''
        select = '''SELECT project_name,developer_name
            FROM gh_jobs AS t
            WHERE status = %s
            AND datasource_id = %s
            LIMIT 1'''
        update='''UPDATE gh_jobs AS t SET status='In_Progress', last_modified=NOW()
        WHERE datasource_id=%s
        AND project_name=%s
        AND developer_name=%s
        '''
        unlock = '''UNLOCK TABLES'''
        try:
            self.cursor.execute(lock)
            self.cursor.execute(select, (status,datasource_id))
            result = self.cursor.fetchone()
            self.cursor.execute(update,(datasource_id, result[0],result[1]))
            self.cursor.execute(unlock)
            return result
        except:
            print ("Finding job failed.")
            self.cursor.execute(unlock)  
            return None   
            
    #this method allows for status changes
    def change_status(self,status,previous_stage,datasource_id,project,developer):
        update='''UPDATE gh_jobs 
        SET status=%s, previous_stage=%s, last_modified=NOW() 
        WHERE datasource_id=%s 
        AND project_name=%s
        AND developer_name=%s
        '''
        try:
            self.cursor.execute(update,(status,previous_stage,datasource_id,project,developer))
        except:
            print('!!!!WARNING!!!! Status '+status+' did not update correctly for '+project+' by '+developer+' with id '+datasource_id+'.')
            print(traceback.format_exc())
            self.error=True
    
    #this method allows for error posting 
    def post_error(self,message,datasource_id,project,developer):
        update='''UPDATE gh_jobs 
        SET error_msg=%s, status='error', last_modified=NOW()
        WHERE datasource_id=%s
        AND project_name=%s
        AND developer_name=%s'''
        gather='''SELECT status FROM gh_jobs
        WHERE datasource_id=%s
        AND project_name=%s
        AND developer_name=%s
        LIMIT 1'''
        try:
            self.cursor.execute(gather,(datasource_id,project,developer))
            fail_stage=self.cursor.fetchone()
            fail_stage=fail_stage[0]
            message=fail_stage+":\n"+message
            self.cursor.execute(update,(message,datasource_id,project,developer))
        except:
            print('!!!!WARNING!!!! Error '+message+'could not be posted to '+project+' for '+developer+' at '+datasource_id+'.')
            self.error=True
            
    def gather_xml(self,project_name,developer_name,datasource_id):
        gather='''SELECT XML FROM gh_projects
        WHERE datasource_id=%s
        AND project_name=%s
        AND developer_name=%s
        LIMIT 1'''
        try:
            self.cursor.execute(gather,(datasource_id,project_name,developer_name))
            xml=self.cursor.fetchone()
            xml=xml[0]
        except:
            print('!!!!WARNING!!!! XML not found for '+project_name+' and '+developer_name+' at '+str(datasource_id))
            xml=None
        return xml
    
    '''
    This method provides the ability to get a clean up job from the job database.
    '''
    def get_cleanup_job(self, datasource_id, previousStage):
        lock = '''LOCK TABLE gh_jobs READ, gh_jobs AS t WRITE'''
        select = '''SELECT project_name,developer_name
            FROM gh_jobs AS t
            WHERE status = 'In_Progress'
            AND previous_stage=%s
            AND datasource_id = %s
            LIMIT 1'''
        update='''UPDATE gh_jobs AS t SET status='Clean_Up', last_modified=NOW()
        WHERE datasource_id=%s
        AND project_name=%s
        AND developer_name=%s
        '''
        unlock = '''UNLOCK TABLES'''
        try:
            self.cursor.execute(lock)
            self.cursor.execute(select, (previousStage,datasource_id))
            result = self.cursor.fetchone()
            self.cursor.execute(update,(datasource_id, result[0],result[1]))
            self.cursor.execute(unlock)
            return result
        except:
            print ("Finding job failed.")
            self.cursor.execute(unlock)
            return None   
            
    '''
    Deletes a project for cleanup
    '''
    def delete_project(self,datasource_id,project,developer):
        try:
            delete='''DELETE FROM gh_projects WHERE project_name=%s AND developer_name=%s AND datasource_id=%s'''
            self.cursor.execute(delete,(project,developer,datasource_id))
        except:
            print("!!!!WARNING!!!! Deletion of project failed")
            print(traceback.format_exc())
        