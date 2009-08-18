'''
Created on Jul 19, 2009

This module houses all the parsers needed for GitHub

@author: Steven Norris
'''

import re

#This parses the description for the XML
def parse_description(xml):
    p=re.compile('<description>.+?</description>',re.DOTALL)
    results=p.findall(xml)
    if(results):
        description=results[0]
        description=description[13:len(description)-14]
    else:
        description=None
    return description

#this parses the forks boolean and integer for the XML
def parse_forks(xml):
    boolean=re.compile('<fork type="boolean">.+?</fork>')
    integer=re.compile('<forks type="integer">.+?</forks>')
    results=boolean.findall(xml)
    if(results):
        fork_b=results[0]
        fork_b=fork_b[21:len(fork_b)-7]
        results=integer.findall(xml)
        if(results):
            fork_i=results[0]
            fork_i=fork_i[22:len(fork_i)-8]
            forks=(fork_b,fork_i)
        else:
            forks=(fork_b,None)
    else:
        forks=(None,None)
    return forks

#this parses the private variable for the XML
def parse_private(xml):
    p=re.compile('<private type="boolean">.+?</private>')
    results=p.findall(xml)
    if(results):
        private=results[0]
        private=private[24:len(private)-10]
    else:
        private=None
    return private

#this parses the url for the xml
def parse_url(xml):
    p=re.compile('<url>.+?</url>')
    results=p.findall(xml)
    if(results):
        url=results[0]
        url=url[5:len(url)-6]
    else:
        url=None
    return url

#this parses the homepage for the xml
def parse_home(xml):
    p=re.compile('<homepage>.+?</homepage>')
    results=p.findall(xml)
    if(results):
        homepage=results[0]
        homepage=homepage[10:len(homepage)-11]
    else:
        homepage=None
    return homepage

#this parses the watchers for the xml
def parse_watch(xml):
    p=re.compile('<watchers type="integer">.+?</watchers>')
    results=p.findall(xml)
    if(results):
        watchers=results[0]
        watchers=watchers[25:len(watchers)-11]
    else:
        watchers=None
    return watchers

#this parses the open issues for the xml
def parse_issues(xml):
    p=re.compile('<open-issues type="integer">.+?</open-issues>')
    results=p.findall(xml)
    if(results):
        issues=results[0]
        issues=issues[28:len(issues)-14]
    else:
        issues=None
    return issues

