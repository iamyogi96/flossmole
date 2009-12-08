'''
Created on Sep 21, 2009

@author: StevenNorris
'''
import httplib
import urllib2
from SourceForgeUtils import SourceForgeUtils
import re
from HTMLParser import HTMLParser

def get_page(url):
    conn=httplib.HTTPConnection('sourceforge.net')
    conn.request("GET",url)
    resp=conn.getresponse()
    html_page=resp.read()
    html_page=str(html_page)
    conn.close()
    return html_page

def get_page2(url):
    response = urllib2.urlopen(url)
    html = response.read()
    return html

    
def memberskillsSpider(page):
    match=re.search('project/stats.+?&type=.+?"',page)
    if(match!=None):
        link=match.group(0)
        return link[0:len(link)-1]
    else:
        return None
    
def developersSpider(page):
    match=re.compile('<tr class=".+?">.+?</tr>',re.DOTALL)
    links=match.findall(page);
    return links

def profileSpider(page):
    link=re.findall('users/.+?/',page)
    link=link[0]
    return link
    

get='''SELECT developers_html FROM project_indexes WHERE datasource_id=%s AND proj_unixname=%s'''
utils=SourceForgeUtils('dbInfoTest.txt')
utils.cursor.execute(get,('0','adempiere'))
page=utils.cursor.fetchone()
links=developersSpider(page[0])
link=profileSpider(links[0])

#page=utils.get_page('http://'+'sourceforge.net/'+links[0])
print link



