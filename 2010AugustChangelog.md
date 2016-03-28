# Introduction #

This is a reverse-chronological log of things we've done on this FLOSSmole project for the month of August 2010. Think of it as a journal of changes and features. An attempt at non-email-based institutional memory.


# Details #

## August 4, 2010 ##
  * Turned in NSF collaborative grant proposal with Greg Madey of SRDA.

---

## August 11, 2010 ##
  * Working on Google Code parser.

---

## August 12, 2010 ##
  * Changed Google tables on production side to have UTF-8 collation.
  * Parsed Google Code data.
  * Released Google Code data.

---

## August 20, 2010 ##
  * Backups to Teragrid begun.

---

## August 27, 2010 ##
### Teragrid Backup ###
  * Github ds=223 was backed up successfully to Teragrid.
  * There were certain errors after this that had to do with database versions being out of sync.
  * I ran the following commands on the database to get it to be in agreement with ossmole\_merged:
```
REATE TABLE IF NOT EXISTS `gc_developer_indexes` (
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

 CREATE TABLE `ossmole_merged`.`gc_project_people` (
`proj_name` VARCHAR( 255 ) NOT NULL ,
`datasource_id` INT NOT NULL ,
`person_name` VARCHAR( 255 ) NOT NULL ,
`role` VARCHAR( 255 ) NOT NULL ,
`duties` VARCHAR( 255 ) NOT NULL ,
`notes` VARCHAR( 255 ) NOT NULL ,
`last_updated` DATETIME NOT NULL ,
PRIMARY KEY ( `proj_name` , `datasource_id` , `person_name` )
) ENGINE = MYISAM;

 CREATE TABLE `ossmole_merged`.`gc_project_labels` (
`proj_name` VARCHAR( 255 ) NOT NULL ,
`datasource_id` INT NOT NULL ,
`label` VARCHAR( 255 ) NOT NULL ,
`last_updated` DATETIME NOT NULL ,
PRIMARY KEY ( `proj_name` , `datasource_id` , `label` )
) ENGINE = MYISAM COMMENT = 'this holds the optional labels for a project' ;

 CREATE TABLE `ossmole_merged`.`gc_project_links` (
`proj_name` VARCHAR( 255 ) NOT NULL ,
`datasource_id` INT NOT NULL ,
`link_title` VARCHAR( 255 ) NOT NULL,
`link` VARCHAR( 255 ) NOT NULL ,
`last_updated` DATETIME NOT NULL ,
PRIMARY KEY ( `proj_name` , `datasource_id` , `link` )
) ENGINE = MYISAM COMMENT = 'this holds the optional external links listed for a project' ;

 CREATE TABLE `ossmole_merged`.`gc_project_blogs` (
`proj_name` VARCHAR( 255 ) NOT NULL ,
`datasource_id` INT NOT NULL ,
`blog_title` VARCHAR( 255 ) NOT NULL ,
`blog_link` VARCHAR( 255 ) NOT NULL,
`last_updated` DATETIME NOT NULL ,
PRIMARY KEY ( `proj_name` , `datasource_id` , `blog_link` )
) ENGINE = MYISAM COMMENT = 'this holds the optional external blog title/link listed for a project' ;

ALTER TABLE `gc_projects` ADD `code_license` VARCHAR( 100 ) NULL COMMENT 'code license chosen',
ADD `activity_level` VARCHAR( 50 ) NULL COMMENT 'the word describing the activity level',
ADD `content_license` VARCHAR( 100 ) NULL COMMENT 'content license (optional)';

ALTER TABLE `gc_projects` ADD `project_summary` VARCHAR(255) NULL COMMENT 'short tag line',
ADD `project_description` text NULL COMMENT 'the longer description of the project';

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

CREATE TABLE `tg_projects` (
  `unixname` varchar(255) NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `last_updated` datetime default NULL,
  `url` varchar(255) default NULL,
  `summary` text,
  `description` text,
  PRIMARY KEY  (`unixname`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

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



CREATE TABLE IF NOT EXISTS `lp_developers` (
  `dev_loginname` varchar(100) NOT NULL default '',
  `datasource_id` int(11) NOT NULL default '0',
  `realname` varchar(100) default NULL,
  `karma` int(11) default NULL,
  `timezone` varchar(50) default NULL,
  `join_date` date default NULL,
  `last_updated` datetime default NULL,
  `coc_signer` varchar(50) default NULL,
  `description` mediumtext,
  PRIMARY KEY  (`dev_loginname`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS `lp_developer_wiki` (
  `dev_loginname` varchar(100) NOT NULL default '',
  `datasource_id` int(11) NOT NULL default '0',
  `wiki` varchar(100) NOT NULL default '',
  `last_updated` datetime default NULL,
  PRIMARY KEY  (`dev_loginname`,`datasource_id`,`wiki`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS `lp_group_devs` (
  `group_loginname` varchar(100) NOT NULL default '',
  `dev_loginname` varchar(100) NOT NULL default '',
  `datasource_id` int(11) NOT NULL default '0',
  `last_updated` datetime default NULL,
  PRIMARY KEY  (`group_loginname`,`dev_loginname`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS `lp_group_projects` (
  `group_loginname` varchar(100) NOT NULL default '',
  `datasource_id` int(11) NOT NULL default '0',
  `project_name` varchar(50) NOT NULL default '',
  `last_updated` datetime default NULL,
  PRIMARY KEY  (`group_loginname`,`datasource_id`,`project_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS `tg_project_categories` (
  `unixname` varchar(255) NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `category_name` varchar(255) NOT NULL,
  `category_url` varchar(255) NOT NULL,
  `last_updated` datetime NOT NULL,
  PRIMARY KEY  (`unixname`,`datasource_id`,`category_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='this holds the category info for tigris projects';


ALTER TABLE  `gc_projects` ADD  `code_url` VARCHAR(255) NULL DEFAULT NULL AFTER  `code_license` ;
ALTER TABLE  `gc_projects` ADD  `content_url` VARCHAR(255) NULL DEFAULT NULL AFTER  `content_license` ;
```

## August 31, 2010 ##
### Teragrid Backup ###
  * Having some issues getting the two versions of the database to match. I guess my recordkeeping of changes was somewhat slack. Need to improve that. I was 98% accurate, but tracking down that 2% has taken the better part of two days.
  * re-importing Tigris, Launchpad, and Google Code now.