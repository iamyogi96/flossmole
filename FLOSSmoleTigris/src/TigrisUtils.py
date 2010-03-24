'''
Created on Aug 16, 2009
This module includes the necessary utilities for the source forge spider.
@author: StevenNorris
'''

import MySQLdb
import traceback
import urllib2
import socket

class TigrisUtils:
    #this gathers the initial connection to the database
    def __init__(self,file_name):
       # try:
        #    dbfile = open(file_name, 'r')
        #except:
         #   print(traceback.format_exc())
          #  raise Exception("Database file error: "+file_name)
        #self.host = dbfile.readline().strip()
        #self.port = int(dbfile.readline().strip())
        #self.username = dbfile.readline().strip()
        #self.password = dbfile.readline().strip()
        #self.database = dbfile.readline().strip()
        self.host="grid0.cs.elon.edu"
        self.port=8888
        self.username="snorris4"
        self.password="thejoker"
        self.database="test"
        self.db=MySQLdb.connect(host=self.host, user=self.username, passwd=self.password, db=self.database)
        self.cursor = self.db.cursor()
        self.error=False
        
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
        lock = '''LOCK TABLE tg_jobs READ, tg_jobs AS t WRITE'''
        select = '''SELECT unixname
            FROM tg_jobs AS t
            WHERE status = %s
            AND datasource_id = %s
            ORDER BY unixname
            LIMIT 1'''
        update='''UPDATE tg_jobs AS t SET status='In_Progress', last_modified=NOW()
        WHERE datasource_id=%s
        AND unixname=%s
        '''
        unlock = '''UNLOCK TABLES'''
        try:
            self.cursor.execute(lock)
            self.cursor.execute(select, (status,datasource_id))
            result = self.cursor.fetchone()
            self.cursor.execute(update,(datasource_id, result[0]))
            self.cursor.execute(unlock)
            return result
        except:
            print ("Finding job failed.")
            self.cursor.execute(unlock)     
   
    #this method allows for status changes
    def change_status(self,status,previous,datasource_id,unixname):
        update='''UPDATE tg_jobs 
        SET status=%s, previous_stage=%s, last_modified=NOW(), modified_by=%s
        WHERE datasource_id=%s 
        AND unixname=%s
        '''
        try:
            self.cursor.execute(update,(status,previous,socket.gethostname(),datasource_id,unixname))
        except:
            print('!!!!WARNING!!!! Status '+status+' did not update correctly for '+unixname+' with id '+datasource_id+'.')
            print(traceback.format_exc())
            self.error=True
    
    #this method allows for error posting 
    def post_error(self,message,datasource_id,unixname):
        update='''UPDATE tg_jobs 
        SET error_msg=%s, status='error', last_modified=NOW(), modified_by=%s
        WHERE datasource_id=%s
        AND unixname=%s'''
        try:
            self.cursor.execute(update,(message,socket.gethostname(),datasource_id,unixname))
        except:
            print('!!!!WARNING!!!! Error '+message+'could not be posted for'+unixname+' at '+datasource_id+'.')
            self.error=True
    
    #Gathers the discussions page for the named project
    def get_discussions(self,datasource_id,unixname):
        try:
            select="""SELECT discussionshtml FROM tg_project_indexes WHERE datasource_id=%s AND unixname=%s LIMIT 1"""
            self.cursor.execute(select,(datasource_id,unixname))
            discussions=self.cursor.fetchone()
            return discussions
        except:
            print("!!!!WARNING!!!! Collecting discussions page failed.")
            print(traceback.format_exc())
            
    #Gathers the specific discussions pages for the named project
    def get_discussions_specific(self,datasource_id,unixname):
        try:
            select="""SELECT html, discussion_name FROM tg_discussions_indexes WHERE datasource_id=%s AND unixname=%s"""
            self.cursor.execute(select,(datasource_id,unixname))
            discussions=self.cursor.fetchall()
            return discussions
        except:
            print("!!!!WARNING!!!! Collecting specific discussions pages failed.")
            print(traceback.format_exc())