#!/usr/bin/env python
import sys
import MySQLdb
import traceback

#Constants
DBFILENAME = 'dbInfo.txt'

class Debian_Utilities:
    
    #Executes the supplied query string using the supplied parameters and returns
    #the first row returned by the query
    def execQuery(self, queryString, *params):
        try:
            cursor = self.dbh.cursor()
            cursor.execute(queryString, params)
        except:
            raise Exception(traceback.format_exc())
        return cursor.fetchone()

    #Creates a database connection using the information contained in the DBFILENAME
    #file and returns the database connection handle
    def connect(self):
        try:
            dbFile = open(DBFILENAME, 'r')
        except:
            print 'Cannot open database information file - exiting'
            sys.exit()
    
        host = dbFile.readline().strip()
        port = int(dbFile.readline().strip())
        username = dbFile.readline().strip()
        password = dbFile.readline().strip()
        database = dbFile.readline().strip()
    
        try:
            dbh = MySQLdb.connect(host=host, user=username, passwd=password, db=database)
        except:
            print 'Error connecting to database - exiting\nTraceback:\n' + traceback.format_exc()
            sys.exit()
    
        return dbh
    
    #Returns a tuple containing the information of a job to be completed in the form
    #of (job ID, project name, debian type, datasource id)
    def findJob(self, job_type):
        lock = '''LOCK TABLE debian_jobs READ, debian_jobs as t WRITE'''
        select = '''SELECT job_id, proj_name, debian_type, datasource_id
            FROM debian_jobs AS t
            WHERE job_type = %s
            AND status = 'pending'
            LIMIT 1;'''
        update = '''UPDATE debian_jobs AS t
            SET status = 'in progress',
            last_modified = NOW()
            WHERE job_id = %s'''
        unlock = '''UNLOCK TABLES'''
        try:
            cursor = self.dbh.cursor()
            cursor.execute(lock)
            cursor.execute(select, (job_type))
            result = cursor.fetchone()
            cursor.execute(update, (result[0]))
            cursor.execute(unlock)
        except:
            raise Exception('Error in job selection')
        return result
    
    #Updates the status of the specified job with the supplied status message
    def updateStatus(self, status, id):
        update = 'SELECT status FROM debian_jobs WHERE job_id=' + str(id) + ''' FOR UPDATE;
            UPDATE debian_jobs
            SET status = %s, last_modified = NOW()
            WHERE job_id = %s'''
    
        try:
            self.dbh.cursor().execute(update, (status, id))
        except:
            print 'Error updating status to ' + status + ' on job ' + str(id) + ' - exiting'
            sys.exit()
    
    #Posts the supplied error message to the specified job in the job queue
    def postError(self, message, id):
        update = 'SELECT error_msg FROM debian_jobs WHERE job_id=' + str(id) + ''' FOR UPDATE;
            UPDATE debian_jobs
            SET status = 'error', error_msg = %s, last_modified = NOW()
            WHERE job_id = %s'''
        try:
            self.dbh.cursor().execute(update, (message, id))
        except:
            print 'Error writing error message to job ' + str(id) + ': ' + message + ' - exiting'
            sys.exit()
    
    #Creates the database connection
    def __init__(self):
        self.dbh = self.connect()
