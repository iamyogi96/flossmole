# Introduction #

This is a reverse-chronological log of things we've done on this project for the month of June 2010. Think of it as a journal of changes and features. An attempt at non-email-based institutional memory.

# Details #
## June 22, 2010 ##
### Collectors ###
  * still running Google Code. There are 4 machines running on it right now (grid0-3). At the moment it is on "l" on step 3 of 8. This means not quite halfway finished. At this rate, and with questionable stops and starts of the machines, it should be done by mid-July.
  * I need to run a Teragrid backup before GC finishes. So. The question is, how to best do this without sending the db into a fit. Should I stop the GC process and run Teragrid backup or should I attempt to work around the GC collection?

---

## June 21, 2010 ##
### Collectors ###
  * Somehow missed some Launchpad tables when moving from test into production. Added these tables. Updated datasource\_id to 227. Released code. lp\_group\_devs has no data. Did not release code into Datamart for June. Will catch this again in July.


---

## June 20, 2010 ##
### Collectors ###
  * Released Tigris metadata. Included are: project info, project categories, project owners, project licenses.
  * Mailing list data is too large to release. I will copy to Teragrid.
### Teragrid ###
  * cannot start teragrid backup until Google Code is finished. (close, I hope?)

## June 19, 2010 ##
### Collectors ###
  * Google Code is on 'tr-'
  * wrote Tigris parser & ran it
### Database Admin ###
  * Created Tigris tables for parsed data (ALTERed `tg_projects` on `ossmole_merged` and `test` and CREATEd the other 3 tables on both:
```
CREATE TABLE `tg_projects` (
  `unixname` varchar(255) NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `last_updated` datetime default NULL,
  `url` varchar(255) default NULL,
  `summary` text,
  `description` text,
  PRIMARY KEY  (`unixname`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1

CREATE TABLE `tg_project_categories` (
  `unixname` varchar(255) NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `category_name` varchar(255) NOT NULL,
  `category_url` varchar(255) NOT NULL,
  `last_updated` datetime NOT NULL,
  PRIMARY KEY  (`unixname`,`datasource_id`,`category_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='this holds the category info for tigris projects';

CREATE TABLE `tg_project_licenses` (
  `unixname` varchar(255) NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `license_name` varchar(255) NOT NULL,
  `license_url` varchar(255) NOT NULL,
  `last_updated` datetime NOT NULL,
  PRIMARY KEY  (`unixname`,`datasource_id`,`license_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='this holds the license info for tigris projects';

CREATE TABLE `tg_project_owners` (
  `unixname` varchar(255) NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `owner_email` varchar(255) NOT NULL,
  `owner_name` varchar(255) NOT NULL,
  `last_updated` datetime NOT NULL,
  PRIMARY KEY  (`unixname`,`datasource_id`,`owner_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='this holds the owner info for tigris projects';
```
### Teragrid ###
  * ran the following based on email sent to mailing list
```
mysql> repair table sf_project_statistics_60;
+-----------------------------------------+--------+----------+--------------------------------------------+
| Table                                   | Op     | Msg_type | Msg_text                                   |
+-----------------------------------------+--------+----------+--------------------------------------------+
| ossmole_merged.sf_project_statistics_60 | repair | warning  | Number of rows changed from 0 to 165798359 | 
| ossmole_merged.sf_project_statistics_60 | repair | status   | OK                                         | 
+-----------------------------------------+--------+----------+--------------------------------------------+
2 rows in set (27 min 20.27 sec)
```

---

## June 18, 2010 ##
### Database Admin ###
  * megan created new tables on ossmole\_merged to hold LP data, as follows:
```
show tables from test like 'lp%';

CREATE TABLE `lp_developer_indexes` (
  `dev_loginname` varchar(100) NOT NULL default '',
  `datasource_id` int(11) NOT NULL default '0',
  `html` mediumtext,
  `last_updated` datetime default NULL,
  PRIMARY KEY  (`dev_loginname`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 ;

CREATE TABLE `lp_developer_irc` (
  `dev_loginname` varchar(100) NOT NULL default '',
  `datasource_id` int(11) NOT NULL default '0',
  `username` varchar(100) NOT NULL default '',
  `server` varchar(100) NOT NULL default '',
  `last_updated` datetime default NULL,
  PRIMARY KEY  (`dev_loginname`,`datasource_id`,`username`,`server`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `lp_developer_languages` (
  `dev_loginname` varchar(100) NOT NULL default '',
  `datasource_id` int(11) NOT NULL default '0',
  `language` varchar(100) NOT NULL default '',
  `last_updated` datetime default NULL,
  PRIMARY KEY  (`dev_loginname`,`datasource_id`,`language`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `lp_developer_projects` (
  `dev_loginname` varchar(100) NOT NULL default '',
  `datasource_id` int(11) NOT NULL default '0',
  `project_name` varchar(50) NOT NULL default '',
  `last_updated` datetime default NULL,
  PRIMARY KEY  (`dev_loginname`,`datasource_id`,`project_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `lp_groups` (
  `group_loginname` varchar(100) NOT NULL default '',
  `group_owner` varchar(100) default NULL,
  `datasource_id` int(11) NOT NULL default '0',
  `realname` varchar(255) default NULL,
  `create_date` datetime default NULL,
  `last_updated` datetime default NULL,
  `description` mediumtext,
  `subscription` varchar(255) default NULL,
  `active_count` int(11) default NULL,
  PRIMARY KEY  (`group_loginname`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `lp_jobs` (
  `datasource_id` int(11) NOT NULL default '0',
  `jobName` varchar(50) NOT NULL default '',
  `startTime` datetime default NULL,
  `endTime` datetime default NULL,
  PRIMARY KEY  (`datasource_id`,`jobName`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `lp_project_indexes` (
  `datasource_id` int(11) NOT NULL default '0',
  `project_name` varchar(50) NOT NULL default '',
  `last_updated` datetime NOT NULL default '0000-00-00 00:00:00',
  `html` mediumtext,
  `rdf` mediumtext,
  `contrib_html` mediumtext,
  PRIMARY KEY  (`datasource_id`,`project_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `lp_project_languages` (
  `project_name` varchar(50) NOT NULL default '',
  `datasource_id` int(11) NOT NULL default '0',
  `language` varchar(100) NOT NULL default '',
  `last_updated` datetime default NULL,
  PRIMARY KEY  (`project_name`,`datasource_id`,`language`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `lp_project_licenses` (
  `project_name` varchar(50) NOT NULL default '',
  `datasource_id` int(11) NOT NULL default '0',
  `license` varchar(255) NOT NULL default '',
  `last_updated` datetime default NULL,
  PRIMARY KEY  (`project_name`,`datasource_id`,`license`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `lp_project_uses` (
  `project_name` varchar(50) NOT NULL default '',
  `datasource_id` int(11) NOT NULL default '0',
  `uses` varchar(50) NOT NULL default '',
  `last_updated` datetime default NULL,
  PRIMARY KEY  (`project_name`,`datasource_id`,`uses`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `lp_projects` (
  `datasource_id` int(11) NOT NULL,
  `project_name` varchar(50) NOT NULL default '',
  `last_updated` datetime NOT NULL,
  `display_name` varchar(255) default NULL,
  `project_title` varchar(255) default NULL,
  `short_description` mediumtext,
  `description` mediumtext,
  `created` date default NULL,
  `project_status` varchar(100) default NULL,
  `wiki` varchar(255) default NULL,
  `screenshot` varchar(255) default NULL,
  `homepage` varchar(255) default NULL,
  `focus` varchar(100) default NULL,
  PRIMARY KEY  (`datasource_id`,`project_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='this holds basic info about launchpad projects' ;
```
  * megan created new datasource on `ossmole_merged` as 227.
```
insert into datasources values (227, 14, '2010-Jun LP', '2010-06-18', 'msquire@___.___', '2010-Jun Launchpad run', '2010-06-10', '2010-06-18');
```
  * megan dumped data from `test` lp-% tables and ran mysql>source lp.sql to import these into the `ossmole_merged` schema
  * unfortunately the datasource numbers are off, so I ran this:
```
delete from lp_developer_indexes where datasource_id=215;
delete from lp_developer_indexes where datasource_id=216;
delete from lp_developer_irc where datasource_id=215;
delete from lp_developer_irc where datasource_id=216;
delete from lp_developer_languages where datasource_id=215;
delete from lp_developer_languages where datasource_id=216;
delete from lp_developer_projects where datasource_id=215;
delete from lp_developer_projects where datasource_id=216;
delete from lp_groups where datasource_id=215;
delete from lp_groups where datasource_id=216;
delete from lp_jobs where datasource_id=215;
delete from lp_jobs where datasource_id=216;
delete from lp_project_indexes where datasource_id=215;
delete from lp_project_indexes where datasource_id=216;
delete from lp_project_languages where datasource_id=215;
delete from lp_project_languages where datasource_id=216;
delete from lp_project_licenses where datasource_id=215;
delete from lp_project_licenses where datasource_id=216;
delete from lp_project_uses where datasource_id=215;
delete from lp_project_uses where datasource_id=216;
delete from lp_projects where datasource_id=215;
delete from lp_projects where datasource_id=216;

update lp_developer_indexes set datasource_id=227 where datasource_id=217;
update lp_developer_irc set datasource_id=227 where datasource_id=217;
update lp_developer_languages set datasource_id=227 where datasource_id=217;
update lp_developer_projects set datasource_id=227 where datasource_id=217;
update lp_groups set datasource_id=227 where datasource_id=217;
update lp_jobs set datasource_id=227 where datasource_id=217;
update lp_project_indexes set datasource_id=227 where datasource_id=217;
update lp_project_languages set datasource_id=227 where datasource_id=217;
update lp_project_licenses set datasource_id=227 where datasource_id=217;
update lp_project_uses set datasource_id=227 where datasource_id=217;
update lp_projects set datasource_id=227 where datasource_id=217;
```
### Collectors ###
  * Tigris is finished. Working on parser. Accidentally left code on work machine (forgot to check in) and have no car to go get it. Sigh.
  * GC is running (still). Is currently on 'sc-'.
  * LP is released as DS 227. Writing new dump scripts to generate delimited files and sql dumps. There is one problem with generating a list of developers. This will need to be fixed in the datamart scripts as soon as Carter updates his code.
  * While searching around, I found an API for Launchpad. Sent the email link to Carter.


---

## June 8, 2010 ##
### Collectors ###
  * Google code is on 'b-'
  * Tigris is on subversion and has been for a while. Lots of mail there.
  * carter's lp code is running and parsing now. Should be a release shortly.
  * worked on Tigris parser (forgot to upload to grid0)
### Database Admin ###
  * created new Tigris tables to hold parsed data
  * the license table is able to hold multiple licenses, even though right now I can not find evidence of projects with multiple licenses. The PK is such that it COULD hold multiples if we ever had a need for it to do so.
```
 CREATE TABLE `ossmole_merged`.`tg_project_licenses` (
`unixname` VARCHAR( 255 ) NOT NULL ,
`datasource_id` INT NOT NULL ,
`license_name` VARCHAR( 255 ) NOT NULL ,
`license_url` VARCHAR( 255 ) NOT NULL ,
`last_updated` DATETIME NOT NULL ,
PRIMARY KEY ( `unixname` , `datasource_id` , `license_name` )
) ENGINE = MYISAM COMMENT = 'this holds the license info for tigris projects' ;

 CREATE TABLE `ossmole_merged`.`tg_project_descriptions` (
`unixname` VARCHAR( 255 ) NOT NULL ,
`datasource_id` INT NOT NULL ,
`description` TEXT NOT NULL ,
`last_updated` DATETIME NOT NULL ,
PRIMARY KEY ( `unixname` , `datasource_id` )
) ENGINE = MYISAM COMMENT = 'holds the tigris project descriptions' ;

```

---

## June 7, 2010 ##
### Collectors ###
  * started Google Code run
  * Tigris still running (it's on 'su-')
  * carter finishing up launchpad
### Database Admin ###
  * ran the following on ossmole\_merged to get GC running:
```
CREATE TABLE IF NOT EXISTS `gc_jobs` (
  `unixname` varchar(200) NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `status` enum('gather_home','gather_updates','gather_people','gather_downloads','gather_issues','gather_wiki','gather_people_specific','gather_issues_specific','completed','In_Progress','error','Clean_Up') NOT NULL,
  `previous_stage` enum('gather_home','gather_updates','gather_people','gather_downloads','gather_issues','gather_wiki','gather_people_specific','gather_issues_specific','completed','Clean_Up') default NULL,
  `last_modified` datetime NOT NULL,
  `modified_by` varchar(200) NOT NULL,
  `error_msg` text,
  PRIMARY KEY  (`unixname`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `gc_developer_indexes` (
  `dev_name` varchar(250) NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `devhtml` text NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY  (`dev_name`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS `gc_developer_projects` (
  `datasource_id` int(11) NOT NULL,
  `unixname` varchar(200) NOT NULL,
  `dev_name` varchar(250) NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY  (`datasource_id`,`unixname`,`dev_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS `gc_issues_indexes` (
  `unixname` varchar(200) NOT NULL,
  `issue_id` int(11) NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `html` text NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY  (`unixname`,`issue_id`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS `gc_project_indexes` (
  `unixname` varchar(200) NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `homehtml` longtext NOT NULL,
  `updateshtml` longtext,
  `peoplehtml` longtext,
  `downloadshtml` longtext,
  `issueshtml` longtext,
  `wikihtml` longtext,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY  (`unixname`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
```

---

## June 6, 2010 ##
  * released github data

---

## June 4, 2010 ##
### Web Site ###
  * megan finished database schema and posted on flossmole.org
  * tigris and github still collecting

---

## June 3, 2010 ##
### Collectors ###
  * Carter has run launchpad and is working on parsers now
  * Megan restarted github (repaired table) and restarted Tigris last night.

### Teragrid Backup ###
  * Megan on Teragrid repaired the fm\_project\_authors, fm\_project\_trove, debian\_project\_indexes\_stable, debian\_project\_indexes\_testing, debian\_project\_indexes\_unstable, sf\_project\_indexes.

### Database Admin ###
  * Megan repaired github table locally after grid0 crash and subsequent table crash.

### Web Site ###
  * Megan started working on the schema documentation. Ugh. Now I see why I waited a year in between schema updates. What a pain.

---

## June 2, 2010 ##
### Collectors ###
  * Grid0 crashed yesterday, but being out of town Megan did not notice it right away, so the run was interrupted. Got it back up and running. Github is producing errors now about mysql index files needing to be repaired. Tigris is back up and running.
  * Carter is working on Launchpad. We've decided to abandon collection of "all developers" since there is not a short way to get a list of all devs on a project other than by looking in the code commits. Instead, we will grab 'person' records from the RDF and declare this good enough, also some projects list "top 5 committers".

---