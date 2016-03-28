# Introduction #

This is a reverse-chronological log of things we've done on this project for the month of May 2010. Think of it as a journal of changes and features. An attempt at non-email-based institutional memory.

# Details #
## May 31, 2010 ##
  * MySQL command for finding the size of the ossmole\_merged database:
```
select table_schema "Name of DB", sum(data_length + index_length)/1024/1024/1024 "Database Size in GB" FROM information_schema.TABLES GROUP BY table_schema;
```
  * Updated the web site links to download files
  * Updated the web site "direct download" link with correct server information


---

## May 30, 2010 ##
### Teragrid backup ###
  * backup is finished running. Notified mailing list & web site.
### Collectors ###
  * Github is on 'g'
  * Tigris died at 4am on Friday and I didn't notice. :( Restarted today and is on 'a'. This is collecting all mailing list messages so is going to be quite long.


---

## May 28, 2010 ##
### Collectors ###
  * carter is working on launchpad.
  * megan released Savannah data (ds 224)& posted to web site.
  * Tigris is in message gathering phase
  * github jobs are made, database alters are done - collector is running(221,971 projects to do)

### Teragrid backup ###
  * currently running - this is taking about 24 hours per 10 datasources. I have 30 left to go to get through DS222

### Database Changes ###
```
GITHUB
ALTER TABLE  `gh_jobs` CHANGE  `status`  `status` ENUM(  'In_Progress',  'XMLgathering',  'Parsing',  'Completed',  'error', 'Clean_Up' ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL;
ALTER TABLE  `gh_jobs` ADD  `previous_stage` ENUM(  'XMLgathering',  'Parsing',  'Clean_Up' ) NOT NULL AFTER  `status`;
```

NOTE: still need to do SF changes before running SF next time. Here is the list of changes and they are copied in email from SN dated 05/21/2010 subj: "Hey Update"
```
SOURCEFORGE
ALTER TABLE  `sf_jobs` Change  `status`  `status` ENUM(  'gather_index',  'gather_development',  'gather_memberlist', 'gather_resumes',  'gather_donors',  'gather_mailinglists',  'gather_mailinglistsspecific',  'gather_messages',  'gather_60day', 'gather_year',  'error_60day',  'error_year',  'error',  'completed',  'In_Progress' ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ,
ADD  `previous_stage` ENUM(  'gather_index',  'gather_development',  'gather_memberlist', 'gather_resumes',  'gather_donors',  'gather_mailinglists',  'gather_mailinglistsspecific',  'gather_messages',  'gather_60day', 'gather_year',  'error_60day',  'error_year',  'error',  'completed',  'Clean_Up',  'In_Progress' ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
ADD  `modified_by` VARCHAR( 255 ) NOT NULL; 

ALTER TABLE  `sf_developer_indexes` CHANGE  `skills_html`  `skills_html` MEDIUMTEXT CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL;

ALTER TABLE  `sf_project_indexes` ADD  `donors_html` MEDIUMTEXT NULL DEFAULT NULL AFTER  `indexhtml` ;

ALTER TABLE  `sf_jobs` CHANGE  `status`  `status` ENUM(  'gather_index',  'gather_development',  'gather_memberlist', 'gather_resumes',  'gather_donors',  'gather_mailinglists',  'gather_mailinglistsspecific',  'gather_messages',  'gather_60day', 'gather_year',  'error_60day',  'error_year',  'error',  'completed',  'In_Progress',  'Clean_Up' ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL
```

---

## May 27, 2010 ##
### Collectors ###
  * carter is working on launchpad.
  * megan is running Savannah (ds 224) and Github (ds 223) and Tigris (ds 225)/

### Teragrid backup ###

  * wrote insert.sh script to do the inserts of .sql files automatically. This will take a very long time.

### Hardware ###

  * met with TLT @Elon about hardware and research infrastructure, admins.

### Dissemination ###

  * worked on presentations for OSS 2010 next week.

### Database changes ###
```
SAVANNAH
ALTER TABLE  `sv_jobs` ADD  `previous_stage` ENUM(  'indexHTML',  'skillsHTML',  'indexparsing',  'error',  'completed' ) NOT NULL AFTER  `status` ;

ALTER TABLE  `sv_jobs` CHANGE  `status`  `status` ENUM(  'indexHTML',  'skillsHTML',  'indexparsing',  'error',  'completed' ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL

ALTER TABLE  `sv_jobs` CHANGE  `previous_stage`  `previous_stage` ENUM(  'indexHTML',  'skillsHTML',  'indexparsing',  'error', 'completed',  'Clean_Up' ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL

ALTER TABLE  `sv_jobs` CHANGE  `status`  `status` ENUM(  'indexHTML',  'skillsHTML',  'indexparsing',  'error',  'completed', 'In_Progress' ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL

ALTER TABLE  `sv_jobs` CHANGE  `status`  `status` ENUM(  'indexHTML',  'skillsHTML',  'indexparsing',  'skillsparsing',  'error', 'completed',  'In_Progress' ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ,
CHANGE  `previous_stage`  `previous_stage` ENUM(  'indexHTML',  'skillsHTML',  'indexparsing',  'skillsparsing',  'error', 'completed',  'Clean_Up' ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL

ALTER TABLE  `sv_jobs` CHANGE  `status`  `status` ENUM(  'indexHTML',  'skillsHTML',  'indexparsing',  'skillsparsing',  'error', 'completed',  'In_Progress',  'Clean_Up' ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL
```

---

## May 26, 2010 ##
### Teragrid backup ###

  * continued working on the teragrid backup (finished changes to database setup started yesterday - those took a long time b/c of the size of the tables. Note to self: in the future avoid adding new columns to tables. Make a new table instead.)


---

## May 25, 2010 ##

### Collectors ###

  * Carter worked on Launchpad.
  * Steven has submitted several code changes. Will run these new collectors as soon as I can get this Teragrid backup done.

### User administration ###

  * Megan deleted jschatz user account (Happy Graduation and Congrats Jamie!)
  * Megan added ckozak user account to flossmole.org drupal site
  * Joel added ckozak user account to grid0
  * megan gave ckozak 'select' on grid0 mysql

### Teragrid backup ###

  * megan ran the following database commands to get teragrid database to match grid0:
```
FRESHMEAT
ALTER TABLE `ossmole_merged`.`fm_projects` ADD COLUMN `calc_dev_count` INT(11) NULL  AFTER `projectname_short_fixed` ;

FREE SOFTWARE FNDTN
ALTER TABLE `ossmole_merged`.`fsf_developer_projects` ADD COLUMN `web_page` VARCHAR(255) NULL DEFAULT NULL  AFTER `email` ;
ALTER TABLE `ossmole_merged`.`fsf_projects` ADD COLUMN `calc_dev_count` INT(11) NULL DEFAULT NULL  AFTER `datasource_id` , ADD COLUMN `user_level` VARCHAR(50) NULL DEFAULT NULL  AFTER `desc_long` ;
CREATE TABLE IF NOT EXISTS `fsf_project_licenses` (
  `proj_num` int(11) NOT NULL,
  `license` varchar(50) NOT NULL,
  `date_collected` datetime NOT NULL,
  `datasource_id` int(11) NOT NULL,
  PRIMARY KEY  (`proj_num`,`license`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
CREATE TABLE IF NOT EXISTS `fsf_project_related` (
  `proj_num` int(11) NOT NULL,
  `related_project_name` varchar(50) NOT NULL,
  `date_collected` datetime NOT NULL,
  `datasource_id` int(11) NOT NULL,
  PRIMARY KEY  (`proj_num`,`related_project_name`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
CREATE TABLE IF NOT EXISTS `fsf_project_requirements` (
  `proj_num` int(11) NOT NULL,
  `requirement` varchar(50) NOT NULL,
  `requirement_type` varchar(50) NOT NULL,
  `date_collected` datetime NOT NULL,
  `datasource_id` int(11) NOT NULL,
  PRIMARY KEY  (`proj_num`,`requirement`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

GOOGLE CODE
CREATE TABLE IF NOT EXISTS `gc_projects` (
  `proj_name` varchar(100) NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `last_updated` datetime NOT NULL,
  PRIMARY KEY  (`proj_name`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='this holds basic info about google code projects';

GITHUB
CREATE TABLE IF NOT EXISTS `gh_projects` (
  `project_name` varchar(80) collate utf8_swedish_ci NOT NULL,
  `developer_name` varchar(50) collate utf8_swedish_ci NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `description` text collate utf8_swedish_ci,
  `private` enum('true','false') collate utf8_swedish_ci default NULL,
  `url` varchar(200) collate utf8_swedish_ci default NULL,
  `forked` enum('true','false') collate utf8_swedish_ci default NULL,
  `fork_number` int(11) default NULL,
  `homepage` varchar(200) collate utf8_swedish_ci default NULL,
  `watchers` int(11) default NULL,
  `open_issues` int(11) default NULL,
  `XML` text collate utf8_swedish_ci,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY  (`project_name`,`developer_name`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci COMMENT='Github, from xml API';

SOURCEFORGE
ALTER TABLE `ossmole_merged`.`developers` RENAME TO  `ossmole_merged`.`sf_developers` ;
ALTER TABLE `ossmole_merged`.`sf_developers` ADD COLUMN `member_since` DATETIME NULL DEFAULT NULL  AFTER `email` , ADD COLUMN `user_id` INT(11) NULL DEFAULT NULL  AFTER `member_since` ;
CREATE TABLE IF NOT EXISTS `sf_developer_indexes` (
  `dev_loginname` varchar(100) NOT NULL,
  `profile_html` mediumtext NOT NULL,
  `skills_html` mediumtext,
  `date_collected` datetime NOT NULL,
  `datasource_id` int(11) NOT NULL,
  PRIMARY KEY  (`dev_loginname`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
ALTER TABLE `ossmole_merged`.`developer_projects` RENAME TO  `ossmole_merged`.`sf_developer_projects` ;
CREATE TABLE IF NOT EXISTS `sf_developer_skills` (
  `dev_loginname` varchar(100) NOT NULL,
  `skill_desc` varchar(100) NOT NULL,
  `date_collected` datetime NOT NULL,
  `datasource_id` int(11) NOT NULL,
  PRIMARY KEY  (`dev_loginname`,`skill_desc`,`datasource_id`),
  KEY `datasource_id_index13` (`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
ALTER TABLE `ossmole_merged`.`projects` RENAME TO  `ossmole_merged`.`sf_projects` ;
ALTER TABLE `ossmole_merged`.`project_alltime_statistics` RENAME TO  `ossmole_merged`.`sf_project_all_time_stats` ;
ALTER TABLE `ossmole_merged`.`project_db_environment` RENAME TO  `ossmole_merged`.`sf_project_db_environment` ;
ALTER TABLE `ossmole_merged`.`project_description` RENAME TO  `ossmole_merged`.`sf_project_description` ;
ALTER TABLE `ossmole_merged`.`project_donors` RENAME TO  `ossmole_merged`.`sf_project_donors` ;
ALTER TABLE `ossmole_merged`.`project_environment` RENAME TO  `ossmole_merged`.`sf_project_environment` ;
ALTER TABLE `ossmole_merged`.`project_indexes` RENAME TO  `ossmole_merged`.`sf_project_indexes` ;
ALTER TABLE `ossmole_merged`.`sf_project_indexes` ADD COLUMN `developers_html` MEDIUMTEXT NULL  AFTER `all_time_stats_html` , ADD COLUMN `development_html` MEDIUMTEXT NULL  AFTER `developers_html` ;
ALTER TABLE `ossmole_merged`.`project_intended_audience` RENAME TO  `ossmole_merged`.`sf_project_intended_audience` ;
ALTER TABLE `ossmole_merged`.`project_licenses` RENAME TO  `ossmole_merged`.`sf_project_licenses` ;
ALTER TABLE `ossmole_merged`.`project_list` RENAME TO  `ossmole_merged`.`sf_project_list` ;
ALTER TABLE `ossmole_merged`.`project_operating_system` RENAME TO  `ossmole_merged`.`sf_project_operating_system` ;
ALTER TABLE `ossmole_merged`.`project_programming_language` RENAME TO  `ossmole_merged`.`sf_project_programming_language` ;
ALTER TABLE `ossmole_merged`.`project_public_areas` RENAME TO  `ossmole_merged`.`sf_project_public_areas` ;
ALTER TABLE `ossmole_merged`.`project_statistics` RENAME TO  `ossmole_merged`.`sf_project_statistics` ;
ALTER TABLE `ossmole_merged`.`project_statistics_60` RENAME TO  `ossmole_merged`.`sf_project_statistics_60` ;
ALTER TABLE `ossmole_merged`.`project_status` RENAME TO  `ossmole_merged`.`sf_project_status` ;
ALTER TABLE `ossmole_merged`.`project_topic` RENAME TO  `ossmole_merged`.`sf_project_topic` ;
CREATE TABLE IF NOT EXISTS `sf_project_translations` (
  `proj_unixname` varchar(100) NOT NULL default '',
  `code` varchar(100) NOT NULL default '',
  `description` varchar(100) NOT NULL default '',
  `date_collected` datetime NOT NULL default '0000-00-00 00:00:00',
  `datasource_id` int(11) NOT NULL default '0',
  PRIMARY KEY  (`code`,`proj_unixname`,`datasource_id`),
  KEY `datasource_id_index42` (`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
ALTER TABLE `ossmole_merged`.`project_user_interface` RENAME TO  `ossmole_merged`.`sf_project_user_interface` ;

SAVANNAH
CREATE TABLE IF NOT EXISTS `sv_developers` (
  `datasource_id` int(11) NOT NULL,
  `dev_loginname` varchar(30) NOT NULL,
  `real_name` varchar(50) default NULL,
  `description` text,
  `infohtml` mediumtext NOT NULL,
  `skillshtml` mediumtext NOT NULL,
  `date_collected` datetime NOT NULL,
  `developer_id` int(11) default NULL COMMENT 'from main developer page',
  `member_since` varchar(100) default NULL COMMENT 'from main developer page',
  PRIMARY KEY  (`datasource_id`,`dev_loginname`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='this table holds developer facts for Savannah';
CREATE TABLE IF NOT EXISTS `sv_developer_projects` (
  `datasource_id` int(11) NOT NULL,
  `dev_loginname` varchar(30) NOT NULL,
  `project_name` varchar(30) NOT NULL default '',
  `date_collected` datetime NOT NULL,
  PRIMARY KEY  (`project_name`,`datasource_id`,`dev_loginname`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='this table holds dev skills for Savannah';
CREATE TABLE IF NOT EXISTS `sv_dev_skills` (
  `datasource_id` int(11) NOT NULL,
  `dev_loginname` varchar(30) NOT NULL,
  `skill` varchar(50) NOT NULL default '',
  `level` varchar(50) default NULL,
  `experience` varchar(50) default NULL,
  `date_collected` datetime NOT NULL,
  PRIMARY KEY  (`dev_loginname`,`datasource_id`,`skill`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='this table holds dev skills for Savannah';
CREATE TABLE IF NOT EXISTS `sv_projects` (
  `project_name` varchar(30) NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `description` text,
  `gnu_or_non` enum('gnu','nongnu') NOT NULL,
  `date_collected` datetime NOT NULL,
  `id_num` int(11) default NULL COMMENT 'parsed from project page',
  `project_dev_count` int(11) default NULL COMMENT 'number of developers from main project page',
  `project_long_name` varchar(100) default NULL COMMENT 'long name from the main project page',
  `project_group_type` varchar(100) default NULL COMMENT 'from main project page',
  `number_of_mailing_lists` int(11) default NULL COMMENT 'taken from main project page',
  `bugs_open` int(11) default NULL COMMENT 'from main project page',
  `bugs_total` int(11) default NULL COMMENT 'from main project page',
  `techsupp_open` int(11) default NULL COMMENT 'from main project page',
  `techsupp_total` int(11) default NULL COMMENT 'from main project page',
  `looking_for_number` int(11) default NULL COMMENT 'from main project page',
  `taskmgr_open` int(11) default NULL COMMENT 'from main project page',
  `taskmgr_total` int(11) default NULL COMMENT 'from main project page',
  `patchmgr_open` int(11) default NULL COMMENT 'from main project page',
  `patchmgr_total` int(11) default NULL COMMENT 'from main project page',
  `license` varchar(300) default NULL COMMENT 'from main project page',
  `development_status` varchar(100) default NULL COMMENT 'from main project page',
  PRIMARY KEY  (`project_name`,`datasource_id`,`gnu_or_non`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='these are the Savannah projects';
CREATE TABLE IF NOT EXISTS `sv_project_indexes` (
  `project_name` varchar(30) NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `indexhtml` mediumtext NOT NULL,
  `memberhtml` mediumtext NOT NULL COMMENT '"view members" on home page',
  `date_collected` datetime NOT NULL,
  PRIMARY KEY  (`project_name`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='this holds the index & member (dev) html pages for Savannah';

TIGRIS
CREATE TABLE IF NOT EXISTS `tg_discussions_indexes` (
  `unixname` varchar(255) NOT NULL,
  `discussion_id` int(11) NOT NULL,
  `discussion_name` varchar(255) NOT NULL,
  `html` longtext NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY  (`unixname`,`discussion_id`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
CREATE TABLE IF NOT EXISTS `tg_messages_indexes` (
  `unixname` varchar(255) NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `discussion_id` int(11) NOT NULL,
  `message_id` int(11) NOT NULL,
  `html` text NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY  (`unixname`,`datasource_id`,`discussion_id`,`message_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
CREATE TABLE IF NOT EXISTS `tg_projects` (
  `unixname` varchar(255) NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `last_modified` datetime default NULL,
  `url` varchar(255) default NULL,
  PRIMARY KEY  (`unixname`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
CREATE TABLE IF NOT EXISTS `tg_project_indexes` (
  `unixname` varchar(255) NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `indexhtml` text NOT NULL,
  `memberlisthtml` longtext,
  `discussionshtml` text,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY  (`unixname`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
```

---

## May 24, 2010 ##
  * megan met with funk and joel regarding the grid0 situation. Grid0 is getting old. What to do.

---

## May 21, 2010 ##
  * megan contacted sdsc about doing a backup. The servers are no longer the same names as what they were last time we did a backup so I was unable to connect.