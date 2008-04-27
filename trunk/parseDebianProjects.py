#!/usr/bin/env python
import MySQLdb
import sys
import re
import urllib
import time
from optparse import OptionParser
import traceback

STABLEPACKAGESURL = "http://packages.debian.org/stable/allpackages"
TESTINGPACKAGESURL = "http://packages.debian.org/testing/allpackages"
UNSTABLEPACKAGESURL = "http://packages.debian.org/unstable/allpackages"
DBFILENAME = "dbInfo.txt"

def getPages(projName, type, dbh):
	cursor = dbh.cursor()
	if (type == 'stable'):
		table = 'debian_project_indexes_stable'
		indexhtml = urllib.urlopen('http://packages.debian.org/stable/' + projName).read()
	elif (type == 'testing'):
		table = 'debian_project_indexes_testing'
		indexhtml = urllib.urlopen('http://packages.debian.org/testing/' + projName).read()
	else:
		table = 'debian_project_indexes_unstable'
		indexhtml = urllib.urlopen('http://packages.debian.org/unstable/' + projName).read()
	
	#URL parsing
	try:
		clURL = re.search(r'<a href="(.*?)">Debian Changelog</a>', indexhtml).group(1)
		cpURL = re.search(r'<a href="(.*?)">Copyright File</a>', indexhtml).group(1)
		bugURL = r'http://bugs.debian.org/' + projName
		devURL = re.search(r'<a href="(.*?)">Developer Information', indexhtml).group(1)
		devhtml = urllib.urlopen(devURL).read()
		bughtml = urllib.urlopen(bugURL).read()
		cphtml = urllib.urlopen(cpURL).read()
		clhtml = urllib.urlopen(clURL).read()
	
		insert = 'INSERT INTO ' + table + """( 
			proj_unixname, 
			datasource_id, 
			indexhtml, 
			bugshtml, 
			devshtml, 
			copyrighthtml, 
			changeloghtml, 
			date_collected) 
			VALUES(%s, %s, %s, %s, %s, %s, %s, NOW())"""
		cursor.execute(insert, (projName, options.DATASOURCEID, indexhtml, bughtml, devhtml, cphtml, clhtml))
	except:
		logFile.write("An unhandled exception occurred in URL parsing section, project: " + projName + "\n")
		traceback.print_exc(None, logFile)
		logFile.write("\n\n")

	#description parsing
	try:
		result = re.search(r'<div id="pdesc">\s*<h2>(.*?)</h2>\s*<p>(.*?)</div>', indexhtml, re.DOTALL)
		longName = result.group(1)
		desc = result.group(2)
		update = """UPDATE debian_projects 
			SET proj_longname = %s, 
			description = %s 
			WHERE proj_unixname = %s 
			AND datasource_id = %s
			AND type = %s"""
		cursor.execute(update, (longName, desc, projName, options.DATASOURCEID, type))
	except:
		logFile.write("An unhandled exception occurred in description parsing section, project: " + projName + "\n")
		traceback.print_exc(None, logFile)
		logFile.write("\n\n")
	
	#developer parsing
	try:
		result = re.search(r'<td class="labelcell">Maintainer</td>\s*<td class="contentcell">\s*<a href="(.*?)">(.*?)</a>\s*<a class="email" href="mailto:(.*?)">', devhtml, re.DOTALL)
		url = result.group(1)
		name = result.group(2)
		email = result.group(3)
		insert = """INSERT INTO debian_project_developers( 
			proj_unixname, 
			datasource_id, 
			name, 
			email, 
			url, 
			role, 
			date_collected) 
			VALUES(%s, %s, %s, %s, %s, \'Maintainer\', NOW())"""
		cursor.execute(insert, (projName, options.DATASOURCEID, name, email, url))
	
		result = re.search(r'Co-Maintainers</a></td>\s*<td class="contentcell">(.*?)</td>', devhtml)
		if (result):
			comaintlist = result.group(1)
			comaints = str.split(r'<br>', comaintlist)
			for comaint in comaints:
				result = re.search(r'<a href="(.*?)">(.*?)</a>\s*[<a class="email" href="mailto:(.*?)>mail</a>]', comaint)
				if (result):
					url = result.group(1)
					name = result.group(2)
					email = result.group(3)
					insert = """INSERT INTO debian_project_developers( 
						proj_unixname, 
						datasource_id, 
						name, 
						email, 
						url, 
						role, 
						date_collected) 
						VALUES(%s, %s, %s, %s, %s, 'Co-Maintainer', NOW())"""
					cursor.execute(insert, (projName, options.DATASOURCEID, name, email, url))
	except:
		logFile.write("An unhandled exception occurred in developer parsing section, project: " + projName + "\n")
		traceback.print_exc(None, logFile)
		logFile.write("\n\n")

	#description homepage parsing
	try:
		description = re.search(r'<div id="pdesc">\s*<h2>.*?</h2>\s*<p>(.*?)</div>', indexhtml, re.DOTALL).group(1)
		result1 = re.search(r'Homepage: <a href="(.*?)"', description)
		result2 = re.search(r'http://(.*?)"', description)
		result3 = re.search(r'http://(.*?)\s+', description)
		result4 = re.search(r'<a href="(.*?)"', description)
		if (result1):
			homepage = result1.group(1)
		elif (result2):
			homepage = r'http://' + result2.group(1)
		elif (result3):
			homepage = r'http://' + result3.group(1)
		elif (result4):
			homepage = result4.group(1)
		else:
			homepage = ''
		update = """UPDATE debian_projects 
				SET descr_homepage = %s 
				WHERE proj_unixname = %s 
				AND datasource_id = %s 
				AND type = %s"""
		cursor.execute(update, (homepage, projName, options.DATASOURCEID, type))
	except:
		logFile.write("An unhandled exception occurred in description homepage parsing section, project: " + projName + "\n")
		traceback.print_exc(None, logFile)
		logFile.write("\n\n")

	#copyright parsing
	try:
		result1 = re.search(r'http://(.*?)>', cphtml)
		result2 = re.search(r'http://(.*?)<', cphtml)
		result3 = re.search(r'http://(.*?)\)', cphtml)
		result4 = re.search(r'http://(.*?),', cphtml)
		result5 = re.search(r'http://(.*?)"', cphtml)
		result6 = re.search(r'http://(.*?)\'', cphtml)
		result7 = re.search(r'http://(.*?)/\.', cphtml)
		result8 = re.search(r'http://(.*?).$', cphtml)
		result9 = re.search(r'http://(.*?);', cphtml)
		result10 = re.search(r'http://(.*?)\s+', cphtml)
		result11 = re.search(r'http://(.*?)$', cphtml)
		if (result1):
			homepage = 'http://' + result1.group(1)
		elif (result2):
			homepage = 'http://' + result2.group(1)
		elif (result3):
			homepage = 'http://' + result3.group(1)
		elif (result4):
			homepage = 'http://' + result4.group(1)
		elif (result5):
			homepage = 'http://' + result5.group(1)
		elif (result6):
			homepage = 'http://' + result6.group(1)
		elif (result7):
			homepage = 'http://' + result7.group(1)
		elif (result8):
			homepage = 'http://' + result8.group(1)
		elif (result9):
			homepage = 'http://' + result9.group(1)
		elif (result10):
			homepage = 'http://' + result10.group(1)
		elif (result11):
			homepage = 'http://' + result11.group(1)
		else:
			homepage = ''
		homepage = homepage.rstrip(' ,)><\'";')
		
		insert = """INSERT INTO debian_copyright_urls( 
			proj_unixname, 
			datasource_id, 
			url, 
			date_collected) 
			VALUES(%s, %s, %s, NOW())"""
		cursor.execute(insert, (projName, options.DATASOURCEID, homepage))
	except:
		logFile.write("An unhandled exception occurred in copyright parsing section, project: " + projName + "\n")
		traceback.print_exc(None, logFile)
		logFile.write("\n\n")

def processProjects(projectsFile, type):
	doWork = False
	projects = re.finditer(r'<dt><a href="(.*?)"\s+id=".*?">.*?</a>\s+\((.*?)\)\s*</dt>\s*<dd>(.*?)</dd>', projectsFile)
	for project in projects:
		if (restart and not doWork and project.group(1) == options.RESTARTPROJ):
			doWork = True
		elif not restart and not doWork:
			doWork = True
		if doWork:
			try:
				projName = project.group(1)
				version = project.group(2)
				desc = project.group(3)
				insert = """INSERT INTO debian_projects( 
					proj_unixname, 
					version, 
					description, 
					type, 
					datasource_id, 
					date_collected) 
					VALUES (%s, %s, %s, %s, %s, NOW())"""
				cursor.execute(insert, (projName, version, desc, type, options.DATASOURCEID))
				getPages(projName, type, dbh)
				print('Completed project ' + projName)
			except:
				logFile.write("An unhandled exception occurred in method processProjects, project: " + projName + "\n")
				traceback.print_exc(None, logFile)
				logFile.write("\n\n")

#Main routine
try:
	parser = OptionParser()
	parser.add_option('-l', '--logfile', action='store', type='string', dest='LOGFILEPATH')
	parser.add_option('-s', '--subgroup', action='store', type='string', dest='SUBGROUP')
	parser.add_option('-d', '--datasource', action='store', type='int', dest='DATASOURCEID')
	parser.add_option('-r', '--restart', action='store', type='string', dest='RESTARTPROJ')
	parser.set_default('LOGFILEPATH', './debianLog.txt')
	parser.set_default('SUBGROUP', 'all')
	parser.set_default('DATASOURCEID', 0)
	(options, args) = parser.parse_args()
	
	if (options.RESTARTPROJ):
		restart =  True
	else:
		restart = False
	
	logFile = open(options.LOGFILEPATH, 'w')
	dbFile = open(DBFILENAME, 'r')
	host = dbFile.readline()
	port = dbFile.readline()
	username = dbFile.readline()
	password = dbFile.readline()
	database = dbFile.readline()
	dbFile.close()
	host.strip()
	port.strip()
	username.strip()
	password.strip()
	database.strip()

	dbh = MySQLdb.connect(host=host[:-1], port=int(port[:-1]),  user=username[:-1], passwd=password[:-1], db=database[:-1])
	cursor = dbh.cursor()

	if (options.SUBGROUP == 'stable'):
		processProjects(urllib.urlopen(STABLEPACKAGESURL).read(), 'stable')
	elif (options.SUBGROUP == 'testing'):
		processProjects(urllib.urlopen(TESTINGPACKAGESURL).read(), 'testing')
	elif (options.SUBGROUP == 'unstable'):
		processProjects(urllib.urlopen(UNSTABLEPACKAGESURL).read(), 'unstable')
	elif (options.SUBGROUP == 'all'):
		processProjects(urllib.urlopen(STABLEPACKAGESURL).read(), 'stable')
		processProjects(urllib.urlopen(TESTINGPACKAGESURL).read(), 'testing')
		processProjects(urllib.urlopen(UNSTABLEPACKAGESURL).read(), 'unstable')
except:
	logFile.write("An unhandled exception occurred in main routine\n")
	traceback.print_exc(None, logFile)
	logFile.write("\n\n")
