# Introduction #

This is a list of stuff we've done in June 2011


# Details #
## June 21, 2011 ##
  * add datasource for UDD on test/prod/TG
```
INSERT INTO `datasources` (`datasource_id`, `forge_id`, `friendly_name`, `date_donated`, `contact_person`, `comments`, `start_date`, `end_date`) VALUES ('276', '15', 'UDD 2011-Jun', '2011-06-17 07:18:17', 'ckozak@elon.edu', 'UDD collection June 2011', '2011-06-17', '2011-06-17'), ('277', '7', 'Debian 2011-Jun', '2011-06-17 00:00:00', 'ckozak@elon.edu', 'Debian collection June 2011', '2011-06-17', NULL);
```
  * get list of UDD tables
```
SHOW tables LIKE 'udd%';
```
  * update test to show new datasource NOT 510
```
UPDATE udd_archived_bugs SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_archived_bugs_blockedby SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_archived_bugs_blocks SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_archived_bugs_fixed_in SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_archived_bugs_found_in SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_archived_bugs_merged_with SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_archived_bugs_packages SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_archived_bugs_tags SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_bibref SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_bugs SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_bugs_blockedby SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_bugs_blocks SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_bugs_fixed_in SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_bugs_found_in SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_bugs_merged_with SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_bugs_packages SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_bugs_tags SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_bugs_usertags SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_carnivore_emails SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_carnivore_keys SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_carnivore_login SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_carnivore_names SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_ddtp SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_debtags SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_deferred SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_deferred_architecture SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_deferred_binary SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_deferred_closes SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_dehs SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_derivatives_packages SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_derivatives_packages_distrelcomparch SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_derivatives_packages_summary SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_derivatives_sources SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_derivatives_uploaders SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_hints SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_lintian SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_migrations SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_new_packages SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_new_sources SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_orphaned_packages SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_package_removal SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_package_removal_batch SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_packages SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_packages_distrelcomparch SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_packages_summary SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_popcon SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_popcon_src SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_popcon_src_average SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_releases SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_screenshots SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_sources SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_sources_count SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_timestamps SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_ubuntu_bugs SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_ubuntu_bugs_duplicates SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_ubuntu_bugs_subscribers SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_ubuntu_bugs_tags SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_ubuntu_bugs_tasks SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_ubuntu_packages SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_ubuntu_packages_distrelcomparch SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_ubuntu_packages_summary SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_ubuntu_popcon SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_ubuntu_popcon_src SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_ubuntu_popcon_src_average SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_ubuntu_sources SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_ubuntu_uploaders SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_upload_history SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_upload_history_architecture SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_upload_history_closes SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_uploaders SET datasource_id=276 WHERE datasource_id=510;
UPDATE udd_wannabuild SET datasource_id=276 WHERE datasource_id=510;
```
  * move data from test into prod
```
mysqldump --where='datasource_id=276' -umegan -p<password> -hgrid6.cs.elon.edu --hex-blob --result-file=276.sql --compact test udd_archived_bugs udd_archived_bugs_blockedby udd_archived_bugs_blocks udd_archived_bugs_fixed_in udd_archived_bugs_found_in udd_archived_bugs_merged_with udd_archived_bugs_packages udd_archived_bugs_tags udd_bibref udd_bugs udd_bugs_blockedby udd_bugs_blocks udd_bugs_fixed_in udd_bugs_found_in udd_bugs_merged_with udd_bugs_packages udd_bugs_tags udd_bugs_usertags udd_carnivore_emails udd_carnivore_keys udd_carnivore_login udd_carnivore_names udd_ddtp udd_debtags udd_deferred udd_deferred_architecture udd_deferred_binary udd_deferred_closes udd_dehs udd_derivatives_packages udd_derivatives_packages_distrelcomparch udd_derivatives_packages_summary udd_derivatives_sources udd_derivatives_uploaders udd_hints udd_lintian udd_migrations udd_new_packages udd_new_sources udd_orphaned_packages udd_package_removal udd_package_removal_batch udd_packages udd_packages_distrelcomparch udd_packages_summary udd_popcon udd_popcon_src udd_popcon_src_average udd_releases udd_screenshots udd_sources udd_sources_count udd_timestamps udd_ubuntu_bugs udd_ubuntu_bugs_duplicates udd_ubuntu_bugs_subscribers udd_ubuntu_bugs_tags udd_ubuntu_bugs_tasks udd_ubuntu_packages udd_ubuntu_packages_distrelcomparch udd_ubuntu_packages_summary udd_ubuntu_popcon udd_ubuntu_popcon_src udd_ubuntu_popcon_src_average udd_ubuntu_sources udd_ubuntu_uploaders udd_upload_history udd_upload_history_architecture udd_upload_history_closes udd_uploaders udd_wannabuild 

mysql -hlocalhost -u -p
use ossmole_merged;
source 276.sql;

mysql -hbebop.sdsc.edu -u -p
use ossmole_merged;
source 276.sql;

```
  * mv all old tables for Launchpad prefix lp_to old\_lp_ (test, prod, TG)
```
RENAME TABLE `test`.`lp_developers` TO `test`.`old_lp_developers` ;
RENAME TABLE `test`.`lp_developer_indexes` TO `test`.`old_lp_developer_indexes` ;
RENAME TABLE `test`.`lp_developer_irc` TO `test`.`old_lp_developer_irc` ;
RENAME TABLE `test`.`lp_developer_languages` TO `test`.`old_lp_developer_languages` ;
RENAME TABLE `test`.`lp_developer_projects` TO `test`.`old_lp_developer_projects` ;
RENAME TABLE `test`.`lp_developer_wiki` TO `test`.`old_lp_developer_wiki` ;
RENAME TABLE `test`.`lp_groups` TO `test`.`old_lp_groups` ;
RENAME TABLE `test`.`lp_group_devs` TO `test`.`old_lp_group_devs` ;
RENAME TABLE `test`.`lp_group_indexes` TO `test`.`old_lp_group_indexes` ;
RENAME TABLE `test`.`lp_group_projects` TO `test`.`old_lp_group_projects` ;
RENAME TABLE `test`.`lp_jobs` TO `test`.`old_lp_jobs` ;
RENAME TABLE `test`.`lp_projects` TO `test`.`old_lp_projects` ;
RENAME TABLE `test`.`lp_project_indexes` TO `test`.`old_lp_project_indexes` ;
RENAME TABLE `test`.`lp_project_languages` TO `test`.`old_lp_project_languages` ;
RENAME TABLE `test`.`lp_project_licenses` TO `test`.`old_lp_project_licenses` ;
RENAME TABLE `test`.`lp_project_uses` TO `test`.`old_lp_project_uses` ;
RENAME TABLE `test`.`lp_temp` TO `test`.`old_lp_temp` ;
RENAME TABLE `ossmole_merged`.`lp_developers` TO `ossmole_merged`.`old_lp_developers` ;
RENAME TABLE `ossmole_merged`.`lp_developer_indexes` TO `ossmole_merged`.`old_lp_developer_indexes` ;
RENAME TABLE `ossmole_merged`.`lp_developer_irc` TO `ossmole_merged`.`old_lp_developer_irc` ;
RENAME TABLE `ossmole_merged`.`lp_developer_languages` TO `ossmole_merged`.`old_lp_developer_languages` ;
RENAME TABLE `ossmole_merged`.`lp_developer_projects` TO `ossmole_merged`.`old_lp_developer_projects` ;
RENAME TABLE `ossmole_merged`.`lp_developer_wiki` TO `ossmole_merged`.`old_lp_developer_wiki` ;
RENAME TABLE `ossmole_merged`.`lp_groups` TO `ossmole_merged`.`old_lp_groups` ;
RENAME TABLE `ossmole_merged`.`lp_group_devs` TO `ossmole_merged`.`old_lp_group_devs` ;
RENAME TABLE `ossmole_merged`.`lp_group_indexes` TO `ossmole_merged`.`old_lp_group_indexes` ;
RENAME TABLE `ossmole_merged`.`lp_group_projects` TO `ossmole_merged`.`old_lp_group_projects` ;
RENAME TABLE `ossmole_merged`.`lp_jobs` TO `ossmole_merged`.`old_lp_jobs` ;
RENAME TABLE `ossmole_merged`.`lp_projects` TO `ossmole_merged`.`old_lp_projects` ;
RENAME TABLE `ossmole_merged`.`lp_project_indexes` TO `ossmole_merged`.`old_lp_project_indexes` ;
RENAME TABLE `ossmole_merged`.`lp_project_languages` TO `ossmole_merged`.`old_lp_project_languages` ;
RENAME TABLE `ossmole_merged`.`lp_project_licenses` TO `ossmole_merged`.`old_lp_project_licenses` ;
RENAME TABLE `ossmole_merged`.`lp_project_uses` TO `ossmole_merged`.`old_lp_project_uses` ;
RENAME TABLE `test`.`calculated_statistics` TO `test`.`old_calculated_statistics` ;
RENAME TABLE `ossmole_merged`.`calculated_statistics` TO `ossmole_merged`.`old_calculated_statistics` ;
RENAME TABLE `test`.`debian_copyright_urls` TO `test`.`old_debian_copyright_urls` ;
RENAME TABLE `test`.`debian_jobs` TO `test`.`old_debian_jobs`;
RENAME TABLE `test`.`debian_projects` TO `test`.`old_debian_projects`;
RENAME TABLE `test`.`debian_project_developers` TO `test`.`old_debian_project_developers`;
RENAME TABLE `test`.`debian_project_indexes_stable` TO `test`.`old_debian_project_indexes_stable`;
RENAME TABLE `test`.`debian_project_indexes_testing` TO `test`.`old_debian_project_indexes_testing`;
RENAME TABLE `test`.`debian_project_indexes_unstable` TO `test`.`old_debian_project_indexes_unstable`;
RENAME TABLE `ossmole_merged`.`debian_copyright_urls` TO `ossmole_merged`.`old_debian_copyright_urls` ;
RENAME TABLE `ossmole_merged`.`debian_jobs` TO `ossmole_merged`.`old_debian_jobs`;
RENAME TABLE `ossmole_merged`.`debian_projects` TO `ossmole_merged`.`old_debian_projects`;
RENAME TABLE `ossmole_merged`.`debian_project_developers` TO `ossmole_merged`.`old_debian_project_developers`;
RENAME TABLE `ossmole_merged`.`debian_project_indexes_stable` TO `ossmole_merged`.`old_debian_project_indexes_stable`;
RENAME TABLE `ossmole_merged`.`debian_project_indexes_testing` TO `ossmole_merged`.`old_debian_project_indexes_testing`;
RENAME TABLE `ossmole_merged`.`debian_project_indexes_unstable` TO `ossmole_merged`.`old_debian_project_indexes_unstable`;
RENAME TABLE `test`.`entity_match_scores` TO `test`.`old_entity_match_scores` ;
RENAME TABLE `ossmole_merged`.`entity_match_scores` TO `ossmole_merged`.`old_entity_match_scores` ;
RENAME TABLE `ossmole_merged`.`list_posts` TO `ossmole_merged`.`old_list_posts` 
```
  * mv data from forges table on test into forges tables on prod
```
--on test:
UPDATE test.`forge_trove_defs` SET datasource_id =274 WHERE datasource_id =272;
UPDATE test.`forge_trove` SET datasource_id =275 WHERE datasource_id =273test.
UPDATE test.`forge_stats` SET datasource_id =275 WHERE datasource_id =273

-- on ossmole_merged & Teragrid
INSERT INTO `datasources` ( `datasource_id` , `forge_id` , `friendly_name` , `date_donated` , `contact_person` , `comments` , `start_date` , `end_date` )
VALUES ( 274, 0, 'Forge Trove Definitions - Initial List', '2011-05-09 14:01:37', 'msquire@elon.edu', 'This is the initial list of features that a forge can have.', '2011-05-09', '2011-05-09' ) , ( 275, 0, '2011-May Forge Trove List', '2011-05-09 00:00:00', 'msquire@elon.edu', 'This is the initial attempt to make a list of features available at each forge.', '2011-05-09', '2011-05-10' );

CREATE TABLE IF NOT EXISTS `forge_stats` (
  `forge_id` int(11) NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `numUsers` int(11) DEFAULT NULL,
  `numProjects` int(11) DEFAULT NULL,
  `poweredBy` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`forge_id`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='snapshot forge stats as reported by the forges themselves';

(INSERT SQL snipped out) 

```

  * on production, create & populate forge\_trove
  * do this on Teragrid also
```

CREATE TABLE IF NOT EXISTS `forge_trove` (
  `forge_id` int(11) NOT NULL,
  `datasource_id` int(11) NOT NULL DEFAULT '273',
  `trove_tag` varchar(50) NOT NULL,
  PRIMARY KEY (`forge_id`,`datasource_id`,`trove_tag`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='holds tags for features available at forge';

(INSERT SQL snipped out)

```
  * on production, create & populate forge\_trove\_defs
  * do this on Teragrid also
```
CREATE TABLE IF NOT EXISTS `forge_trove_defs` (
  `trove_tag` varchar(50) NOT NULL,
  `tag_category` varchar(50) DEFAULT NULL,
  `datasource_id` int(11) NOT NULL,
  `tag_description` varchar(255) NOT NULL,
  `last_updated` datetime NOT NULL,
  PRIMARY KEY (`trove_tag`,`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='this holds the description of each trove tag';

(INSERT sql snipped out) 

```
  * on production, create & populate the forges tables
  * do this on Teragrid also
```
DROP TABLE ossmole_merged.forges;

CREATE TABLE IF NOT EXISTS ossmole_merged.`forges` (
  `forge_id` int(5) NOT NULL,
  `forge_abbr` varchar(3) CHARACTER SET utf8 NOT NULL,
  `forge_long_name` varchar(50) DEFAULT NULL,
  `forge_home_page` varchar(255) CHARACTER SET utf8 NOT NULL,
  `is_forge` tinyint(1) NOT NULL,
  `is_directory` tinyint(1) NOT NULL,
  `is_other` tinyint(1) NOT NULL,
  `established` varchar(50) DEFAULT NULL,
  `organization` varchar(50) DEFAULT NULL COMMENT 'organization overseeing this forge project, if any',
  PRIMARY KEY (`forge_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

(INSERT SQL snipped out)

```
  * update Teragrid with datasources and new forges tables:
```
INSERT INTO `datasources` (`datasource_id`, `forge_id`, `friendly_name`, `date_donated`, `contact_person`, `comments`, `start_date`, `end_date`) VALUES
(271, 12, '2011-May GC', '2011-05-04 00:00:00', 'msquire@elon.edu', '2011-May Google Code collection', '2001-05-04', NULL),
(272, 12, 'LP 2011-Jun', '2011-06-17 00:00:00', 'msquire@elon.edu', 'Launchpad 2011-Jun', '2011-06-17', NULL),
(273, 11, 'Github 2011-Jun', '2011-06-17 00:00:00', 'msquire@elon.edu', 'Github 2011-Jun', '2011-06-17', NULL),
(274, 0, 'Forge Trove Definitions - Initial List', '2011-05-09 14:01:37', 'msquire@elon.edu', 'This is the initial list of features that a forge can have.', '2011-05-09', '2011-05-09'),
(275, 0, '2011-May Forge Trove List', '2011-05-09 00:00:00', 'msquire@elon.edu', 'This is the initial attempt to make a list of features available at each forge.', '2011-05-09', '2011-05-10');
```

  * david new user on grid6
  * carter working on alioth
  * david working on debian
## June 20, 2011 ##
  * release LP data - this requires all new LP header files, dump commands in release files
  * post forge web pages on flossmole.org for the forge study
  * get Carter started on new mailing list project
  * get David started on new Debian counting project
## week of June 13-17 ##
  * Google Code finished; files released
  * david working on forges site & css, etc.
  * carter moves all data from grid0 to grid6 (yay)
## week of June 6 - 10 ##
  * Megan conf call on June 7
  * David working on forges table
  * Megan finishing up forges paper; formatting
  * Carter releases Launchpad collector to Google Code
  * Google code finished; megan releases data
  * Carter begins work on grid0 move to grid6
## week of May 30 - June 3 ##
  * Carter working on Launchpad API-based collector
  * David finishing up visualiztations for Examples and 'forges' paper