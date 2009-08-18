'''
Created on Jun 14, 2009

@author: Steven Norris

This module parses the html documents found on savannah.
'''

import re
from BeautifulSoup import BeautifulSoup

#parses description from index pages
def parse_index(html):
    p=re.compile('<div class="indexcenter\">.+<!-- end indexcenter -->',re.DOTALL)
    results=p.findall(html)
    if (results):
        description=results[0]
        description=description[25:len(description)-30]
        description=description.replace('<p>','')
        description=description.replace('</p>','')
        description=description.replace('<br/>','')
        description=description.replace('<br />','')
        description=description.replace('<a href="http://www.gnu.org/licenses/old-licenses/gpl-2.0.html">','')
        description=description.replace('</a>','')
    else:
        description=None
    return description

#parses project's id from index page
def parse_project_id(html):
    p=re.compile('Id: <strong>#.+?</strong>')
    results=p.findall(html)
    if (results):
        id=results[0]
        id=id[13:len(id)-9]
    else:
        id=None
    return id

#parses the long name for a project from index page
def parse_project_longname(html):
    p=re.compile('>Name: <strong>.+?</strong></span></div><div class="boxitemalt">')
    results=p.findall(html)
    if(results):
        name=results[0]
        name=name[15:len(name)-46]
        if(name==''):
            name=None
        else:
            name=BeautifulSoup(name,convertEntities=BeautifulSoup.HTML_ENTITIES)
            name=name.contents[0]
            try:
                name=name.encode("utf-8")
            except:
                name='!!!Warning!!! Encoding Error on Longname!'
    else:
        name=None
    return name

#parses the number of members for a project form index
def parse_member_num(html):
    p=re.compile('<strong>.+?</strong> active member')
    results=p.findall(html)
    if(results):
        num=results[0]
        num=num[8:len(num)-23]
    else:
        num=None
    return num

#parses the group type for a project from index
def parse_group_type(html):
    p=re.compile('Group Type: <strong>.+?</strong>')
    results=p.findall(html)
    if(results):
        type=results[0]
        type=type[20:len(type)-9]
    else:
        type=None
    return type

#parses the number of mailing lists for a project from index
def parse_mailing_lists(html):
    p=re.compile('<strong>.+?</strong> public mailing-list')
    results=p.findall(html)
    if(results):
        lists=results[0]
        lists=lists[8:len(lists)-29]
    else:
        lists=None
    return lists

#parses the bugs open and total for a project from index
def parse_bugs(html):
    p=re.compile('Bug Tracker</a> (.+?total)')
    open=re.compile('<strong>.+?</strong> open item')
    total=re.compile(', <strong>.+?</strong> total')
    results=p.findall(html)
    if (results):
        string=results[0]
        open_bugs=open.findall(string)
        open_bugs=open_bugs[0]
        open_bugs=open_bugs[8:len(open_bugs)-19]
        total_bugs=total.findall(string)
        total_bugs=total_bugs[0]
        total_bugs=total_bugs[10:len(total_bugs)-15]
        bugs=(open_bugs,total_bugs)
    else:
        bugs=(None,None)
    return bugs

#parses the tech support managers for a project from index
def parse_tech(html):
    p=re.compile('Tech Support Manager</a> (.+?total)')
    open=re.compile('<strong>.+?</strong> open item')
    total=re.compile(', <strong>.+?</strong> total')
    results=p.findall(html)
    if (results):
        string=results[0]
        open_tech=open.findall(string)
        open_tech=open_tech[0]
        open_tech=open_tech[8:len(open_tech)-19]
        total_tech=total.findall(string)
        total_tech=total_tech[0]
        total_tech=total_tech[10:len(total_tech)-15]
        tech=(open_tech,total_tech)
    else:
        tech=(None,None)
    return tech

#parses the task managers for a project from index
def parse_task(html):
    p=re.compile('Task Manager</a> (.+?total)')
    open=re.compile('<strong>.+?</strong> open item')
    total=re.compile(', <strong>.+?</strong> total')
    results=p.findall(html)
    if (results):
        string=results[0]
        open_task=open.findall(string)
        open_task=open_task[0]
        open_task=open_task[8:len(open_task)-19]
        total_task=total.findall(string)
        total_task=total_task[0]
        total_task=total_task[10:len(total_task)-15]
        tasks=(open_task,total_task)
    else:
        tasks=(None,None)
    return tasks

#parses the patch managers for a project from index
def parse_patch(html):
    p=re.compile('Patch Manager</a> (.+?total)')
    open=re.compile('<strong>.+?</strong> open item')
    total=re.compile(', <strong>.+?</strong> total')
    results=p.findall(html)
    if (results):
        string=results[0]
        open_patch=open.findall(string)
        open_patch=open_patch[0]
        open_patch=open_patch[8:len(open_patch)-19]
        total_patch=total.findall(string)
        total_patch=total_patch[0]
        total_patch=total_patch[10:len(total_patch)-15]
        patches=(open_patch,total_patch)
    else:
        patches=(None,None)
    return patches

#parses the people a project is looking for from index
def parse_looking(html):
    p=re.compile('<strong>.+?</strong> contributor')
    results=p.findall(html)
    if(results):
        people=results[0]
        people=people[8:len(people)-21]
    else:
        people=None
    return people

#parses the license for a project from index
def parse_license(html):
    p=re.compile('License: .+?<br />')
    p2=re.compile('>.+?</a>')
    results=p.findall(html)
    if(results):
        string=results[0]
        license=p2.findall(string)
        if(license):
            license=license[0]
            license=license[1:len(license)-4]
        else:
            license=string[9:len(string)-6]
    else:
        license=None
    return license
    
#parses the development status of a project from index
def parse_dev_status(html):
    p=re.compile('Development Status: .+?</p>',re.DOTALL)
    results=p.findall(html)
    if(results):
        status=results[0]
        status=status[20:len(status)-5]
    else:
        status=None
    return status

#parses member's time from info page
def parse_time(html):
    p=re.compile('Site Member Since:.+?</strong>',re.DOTALL)
    p2=re.compile('<strong>.+?</strong>')
    results=p.findall(html)
    if(results):
        string=results[0]
        time=p2.findall(string)
        time=time[0]
        time=time[8:len(time)-9]
    else:
        time=None
    return time

#parses member's name from skills pages
def parse_member_name (html):
    p=re.compile('<title>People at Savannah: .+ Resume')
    results=p.findall(html)
    if (results):
        name=results[0]
        name=name[27:len(name)-7]
    else:
        name=None
    return name

#parse member's description from skills pages
def parse_member_description(html):
    p=re.compile('<h3>Resume.+?<h3>',re.DOTALL)
    results=p.findall(html)
    if(results):
        description=results[0]
        description=description[15:len(description)-4]
        description=description.replace('<p>','')
        description=description.replace('</p>','')
        description=description.replace('<br/>','')
        description=description.replace('<br />','')
    else:
        description=None
    return description
    
#parses each skill into a triple and adds to an array of skills triples, returns skills array
def parse_skills(html):
    skill_table_re=re.compile('<th class="boxtitle">Experience.+</table>',re.DOTALL)
    results=skill_table_re.findall(html)
    skill_table=results[0]
    skillset_re=re.compile('<tr .+?</tr>',re.DOTALL)
    skillset=skillset_re.findall(skill_table)
    skills=[]
    ind_skill_re=re.compile('<td>.+?</td>')
    for item in skillset:
        ind_skill=ind_skill_re.findall(item)
        skills.append(ind_skill)
    for i in range(len(skills)):
        item=skills[i]
        for j in range(len(item)):
            item2=item[j]
            item2=item2[4:len(item[j])-5]
            item[j]=item2
        skills[i]=item
    return skills