# June 1, 2012 #

working on fixing anomalies in the Teragrid database. Here are the sql commands run today, in order by forge:

## ALIOTH ##
```
rename table al_mailing_lists to old_al_mailing_lists;
rename table al_mailing_lists_indexes to old_al_mailing_lists_indexes;
rename table al_messages to old_al_messages;
rename table al_messages_indexes to old_al_messages_indexes;
rename table al_messages_references to old_al_messages_references;


mysqldump -umegan -p -h localhost ossmole_merged al_projects al_projects_audience al_projects_environment al_projects_language al_projects_license al_projects_os al_projects_status al_projects_tags al_projects_topic al_project_indexes al_project_members al_project_members_roles > al_all.2012-May.sql

drop table al_projects; 
drop table al_projects_audience ;
drop table al_projects_environment ;
drop table al_projects_language ;
drop table al_projects_license ;
drop table al_projects_os ;
drop table al_projects_status ;
drop table al_projects_topic ;
drop table al_project_indexes;

source al_all.2012-May.sql;

select datasource_id, count(*) from al_projects group by 1;
+---------------+----------+
| datasource_id | count(*) |
+---------------+----------+
|           287 |      896 |
|           295 |      903 |
|           315 |      914 |
+---------------+----------+
3 rows in set (0.08 sec)

```

Alioth notes:
  * old tables holding messages and mailing lists have been moved to 'old`_`' and will be re-released when we figure out how to scrape these again
  * indexes were not saved for 287 and 295 for an unknown reason (indexes will be collected and saved from now on)

## DATASOURCES ##
```
drop table datasources;

mysqldump -umegan -p -h localhost ossmole_merged datasources > datasources.2012-May.sql

source /home/megan/flossmole/backups/2012/2012-May/datasources.sql;
```

## DEBIAN ##
no changes

## FRESHMEAT/FREECODE ##
  * Strategy: first just replicate tables to Teragrid, then worry about changing their name to 'fc' rather than fm

```
drop table fm_project_authors;
drop table fm_project_dependencies;
drop table fm_project_homepages;
drop table fm_project_tags;
drop table fm_project_trove;
drop table fm_projects;
drop table FM_TROVE_DEFS;

mysqldump -umegan -p -h localhost ossmole_merged fm_projects > fm_projects.2012-May.sql
mysqldump -umegan -p -h localhost ossmole_merged fm_project_authors> fm_project_authors.2012-May.sql
mysqldump -umegan -p -h localhost ossmole_merged fm_project_dependencies > fm_project_dependencies.2012-May.sql
mysqldump -umegan -p -h localhost ossmole_merged fm_project_homepages > fm_project_homepages.2012-May.sql
mysqldump -umegan -p -h localhost ossmole_merged fm_project_tags > fm_project_tags.2012-May.sql
mysqldump -umegan -p -h localhost ossmole_merged fm_project_trove > fm_project_trove.2012-May.sql
mysqldump -umegan -p -h localhost ossmole_merged fm_trove_defs > fm_trove_defs.2012-May.sql

source /home/megan/flossmole/backups/2012/2012-May/fm/fm_projects.2012-May.sql;
source /home/megan/flossmole/backups/2012/2012-May/fm/fm_project_authors.2012-May.sql;
source /home/megan/flossmole/backups/2012/2012-May/fm/fm_project_dependencies.2012-May.sql;
source /home/megan/flossmole/backups/2012/2012-May/fm/fm_project_homepages.2012-May.sql;
source /home/megan/flossmole/backups/2012/2012-May/fm/fm_project_tags.2012-May.sql;
source /home/megan/flossmole/backups/2012/2012-May/fm/fm_project_trove.2012-May.sql;
source /home/megan/flossmole/backups/2012/2012-May/fm/fm_trove_defs.2012-May.sql;
```

Here are all the Freshmeat/Freecode datasources now listed in the database, and the number of projects for each:

```
select datasource_id, count(*) from fm_projects group by 1;
+---------------+----------+
| datasource_id | count(*) |
+---------------+----------+
|             9 |    37123 |
|            10 |    37413 |
|            11 |    38741 |
|            12 |    39023 |
|            14 |    39406 |
|            15 |    39594 |
|            17 |    39842 |
|            18 |    40164 |
|            21 |    40596 |
|            23 |    40673 |
|            25 |    40404 |
|            26 |    40842 |
|            29 |    41021 |
|            33 |    41318 |
|            37 |    41546 |
|            41 |    41906 |
|            42 |    41908 |
|            47 |    42181 |
|            52 |    42317 |
|            58 |    42500 |
|            63 |    42720 |
|            69 |    42970 |
|            75 |    43082 |
|            81 |    43300 |
|            87 |    43463 |
|            94 |    43615 |
|            99 |    43808 |
|           104 |    43759 |
|           107 |    43859 |
|           111 |    44015 |
|           115 |    44185 |
|           120 |    44379 |
|           124 |    44543 |
|           129 |    44617 |
|           133 |    44716 |
|           139 |    44824 |
|           144 |    45078 |
|           151 |    45257 |
|           156 |    45573 |
|           160 |    45807 |
|           173 |    39621 |
|           178 |    39881 |
|           183 |    40303 |
|           188 |    40505 |
|           194 |    40691 |
|           200 |    40898 |
|           207 |    41443 |
|           218 |    41902 |
|           228 |    42545 |
|           237 |    43206 |
|           247 |    43470 |
|           255 |    43639 |
|           270 |    43778 |
|           296 |    44579 |
|           297 |    44895 |
|           306 |    45373 |
+---------------+----------+
56 rows in set (2.30 sec)
```


## FORGES ##
```
drop table forges;

mysqldump -umegan -p -h localhost ossmole_merged forges > forges.2012-May.sql

source /home/megan/flossmole/backups/2012/2012-May/forges.sql;
```

## FREE SOFTWARE FOUNDATION ##

```
rename table fsf_project_interfaces to old_fsf_project_interfaces;
rename table fsf_project_languages to old_fsf_project_languages;
rename table fsf_project_related to old_fsf_project_related;

drop table fsf_developer_projects;
drop table fsf_projects;
drop table fsf_project_licenses;
drop table fsf_project_requirements;

mysqldump -umegan -p -h localhost ossmole_merged fsf_developer_projects > fsf_developer_projects.2012-May.sql
mysqldump -umegan -p -h localhost ossmole_merged fsf_projects > fsf_projects.2012-May.sql
mysqldump -umegan -p -h localhost ossmole_merged fsf_project_categories > fsf_project_categories.2012-May.sql
mysqldump -umegan -p -h localhost ossmole_merged fsf_project_licenses > fsf_project_licenses.2012-May.sql
mysqldump -umegan -p -h localhost ossmole_merged fsf_project_related > fsf_project_related.2012-May.sql
mysqldump -umegan -p -h localhost ossmole_merged fsf_project_requirements > fsf_project_requirements.2012-May.sql

source /home/megan/flossmole/backups/2012/2012-May/fsf/fsf_developer_projects.2012-May.sql
source /home/megan/flossmole/backups/2012/2012-May/fsf/fsf_projects.2012-May.sql
source /home/megan/flossmole/backups/2012/2012-May/fsf/fsf_project_categories.2012-May.sql
source /home/megan/flossmole/backups/2012/2012-May/fsf/fsf_project_licenses.2012-May.sql
source /home/megan/flossmole/backups/2012/2012-May/fsf/fsf_project_related.2012-May.sql
source /home/megan/flossmole/backups/2012/2012-May/fsf/fsf_project_requirements.2012-May.sql

gzip *.sql
```

Deal with indexes separately because they are so big:

```
mysqldump -umegan -p -h localhost ossmole_merged fsf_project_indexes > fsf_project_indexes.2012-May.sql

source /home/megan/flossmole/backups/2012/2012-May/fsf/fsf_project_indexes.2012-May.sql

gzip fsf_project_indexes.2012-May.sql
```

Here is a list of all the datasources we have for FSF and the count of projects for each:

```
select datasource_id, count(*) from fsf_project_indexes group by 1;

+---------------+----------+
| datasource_id | count(*) |
+---------------+----------+
|            45 |     5226 |
|            50 |     5265 |
|            55 |     5298 |
|            61 |     5328 |
|            66 |     5355 |
|            72 |     5364 |
|            78 |     5386 |
|            84 |     5381 |
|            90 |     5397 |
|            97 |     5366 |
|           142 |     5513 |
|           147 |     5513 |
|           154 |     5584 |
|           159 |     5674 |
|           163 |     5720 |
|           168 |     5760 |
|           171 |     5820 |
|           176 |     5870 |
|           181 |     5918 |
|           186 |     6027 |
|           191 |     6067 |
|           197 |     6130 |
|           203 |     6162 |
|           221 |     6438 |
|           231 |     6679 |
|           240 |     6683 |
|           250 |     6671 |
|           258 |     6671 |
|           268 |     6671 |
|           281 |     6671 |
|           314 |     6849 |
+---------------+----------+
31 rows in set (0.19 sec)
```

## GOOGLE CODE ##
```
drop table gc_developer_projects;
drop table gc_issues_indexes
drop table gc_projects;
drop table gc_project_blogs;
drop table gc_project_groups;
drop table gc_project_labels;
drop table gc_project_links;
drop table gc_project_people;
drop table gc_project_indexes;            |



mysql> CREATE TABLE IF NOT EXISTS `gc_developer_indexes` (
    ->   `dev_name` varchar(250) NOT NULL,
    ->   `datasource_id` int(11) NOT NULL,
    ->   `devhtml` text,
    ->   `last_modified` datetime NOT NULL,
    ->   PRIMARY KEY (`dev_name`,`datasource_id`)
    -> ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
Query OK, 0 rows affected (0.25 sec)

mysql> CREATE TABLE IF NOT EXISTS `gc_developer_projects` (
    ->   `datasource_id` int(11) NOT NULL,
    ->   `unixname` varchar(100) NOT NULL,
    ->   `dev_name` varchar(100) NOT NULL,
    ->   `last_modified` datetime NOT NULL,
    ->   PRIMARY KEY (`datasource_id`,`unixname`,`dev_name`)
    -> ) ENGINE=MyISAM DEFAULT CHARSET=utf8;


mysql> CREATE TABLE IF NOT EXISTS `gc_issues_indexes` (
    ->   `unixname` varchar(100) NOT NULL,
    ->   `issue_id` int(11) NOT NULL,
    ->   `datasource_id` int(11) NOT NULL,
    ->   `html` text NOT NULL,
    ->   `last_modified` datetime NOT NULL,
    ->   PRIMARY KEY (`unixname`,`issue_id`,`datasource_id`)
    -> ) ENGINE=MyISAM DEFAULT CHARSET=utf8;


mysql> CREATE TABLE IF NOT EXISTS `gc_projects` (
    ->   `proj_name` varchar(100) NOT NULL,
    ->   `datasource_id` int(11) NOT NULL,
    ->   `last_updated` datetime NOT NULL,
    ->   `code_license` varchar(100) DEFAULT NULL COMMENT 'code license chosen',
    ->   `code_url` varchar(255) DEFAULT NULL COMMENT 'url for the license',
    ->   `activity_level` varchar(50) DEFAULT NULL COMMENT 'the word describing the activity level',
    ->   `content_license` varchar(100) DEFAULT NULL COMMENT 'content license (optional)',
    ->   `content_url` varchar(255) DEFAULT NULL,
    ->   `project_summary` varchar(255) DEFAULT NULL COMMENT 'short tag line',
    ->   `project_description` text COMMENT 'the longer description of the project',
    ->   PRIMARY KEY (`proj_name`,`datasource_id`)
    -> ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='this holds basic info about google code projects';


mysql> CREATE TABLE IF NOT EXISTS `gc_project_blogs` (
    ->   `proj_name` varchar(100) NOT NULL,
    ->   `datasource_id` int(11) NOT NULL,
    ->   `blog_title` varchar(255) NOT NULL,
    ->   `blog_link` varchar(255) CHARACTER SET latin1 NOT NULL,
    ->   `last_updated` datetime NOT NULL,
    ->   PRIMARY KEY (`proj_name`,`datasource_id`,`blog_link`)
    -> ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='this holds the optional external blog title/link listed for ';


mysql> CREATE TABLE IF NOT EXISTS `gc_project_groups` (
    ->   `proj_name` varchar(100) NOT NULL,
    ->   `datasource_id` int(11) NOT NULL,
    ->   `group_name` varchar(100) NOT NULL,
    ->   `group_url` varchar(255) CHARACTER SET latin1 NOT NULL,
    ->   `last_updated` datetime NOT NULL,
    ->   PRIMARY KEY (`proj_name`,`datasource_id`,`group_url`)
    -> ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='this holds the optional groups listed for a project';

mysql> CREATE TABLE IF NOT EXISTS `gc_project_indexes` (
    ->   `unixname` varchar(100) CHARACTER SET utf8 NOT NULL,
    ->   `datasource_id` int(11) NOT NULL,
    ->   `homehtml` longtext CHARACTER SET utf8 NOT NULL,
    ->   `updateshtml` longtext CHARACTER SET utf8 COMMENT 'deprecated 2012-May',
    ->   `peoplehtml` longtext CHARACTER SET utf8,
    ->   `downloadshtml` longtext CHARACTER SET utf8 COMMENT 'No longer collected 2012-May',
    ->   `issuescsv` longtext CHARACTER SET utf8 COMMENT 'Chg to CSV 2012-May',
    ->   `wikihtml` longtext CHARACTER SET utf8 COMMENT 'No longer collected 2012-May',
    ->   `last_modified` datetime NOT NULL,
    ->   PRIMARY KEY (`unixname`,`datasource_id`),
    ->   KEY `datasource_id` (`datasource_id`)
    -> ) ENGINE=MyISAM DEFAULT CHARSET=latin1;


mysql> CREATE TABLE IF NOT EXISTS `gc_project_labels` (
    ->   `proj_name` varchar(100) CHARACTER SET utf8 NOT NULL,
    ->   `datasource_id` int(11) NOT NULL,
    ->   `label` varchar(100) CHARACTER SET utf8 NOT NULL,
    ->   `last_updated` datetime NOT NULL,
    ->   PRIMARY KEY (`proj_name`,`datasource_id`,`label`)
    -> ) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='this holds the optional labels for a project';


mysql> CREATE TABLE IF NOT EXISTS `gc_project_links` (
    ->   `proj_name` varchar(100) NOT NULL,
    ->   `datasource_id` int(11) NOT NULL,
    ->   `link_title` varchar(100) NOT NULL,
    ->   `link` varchar(255) CHARACTER SET latin1 NOT NULL,
    ->   `last_updated` datetime NOT NULL,
    ->   PRIMARY KEY (`proj_name`,`datasource_id`,`link`)
    -> ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='this holds the optional external links listed for a project';


mysql> CREATE TABLE IF NOT EXISTS `gc_project_people` (
    ->   `proj_name` varchar(100) NOT NULL,
    ->   `datasource_id` int(11) NOT NULL,
    ->   `person_name` varchar(100) NOT NULL,
    ->   `role` varchar(100) NOT NULL,
    ->   `duties` varchar(255) NOT NULL,
    ->   `notes` varchar(255) NOT NULL,
    ->   `last_updated` datetime NOT NULL,
    ->   PRIMARY KEY (`proj_name`,`datasource_id`,`person_name`)
    -> ) ENGINE=MyISAM DEFAULT CHARSET=utf8;


# write individual mysqldump commands for each datasource_id in GC
# put all the mysqldump commands in a shell script
bash dump.sh
# put all source commands in a shell script
bash load.sh

```
## Github ##
```
mysqldump -umegan -p -h localhost ossmole_merged gh_projects > gh_projects.2012-May.sql

mysql -e "source gh_projects.2012-May.sql" -u msquire -p -hnibbler.sdsc.edu -P3315 ossmole_merged

select datasource_id, count(*) from gh_projects group by 1;

+---------------+----------+
| datasource_id | count(*) |
+---------------+----------+
|           193 |    41967 |
|           199 |   131207 |
|           205 |   138182 |
|           212 |   177016 |
|           223 |   221970 |
|           234 |   272592 |
|           273 |   101666 |
|           283 |   118490 |
|           292 |   133074 |
|           305 |   163566 |
|           311 |   191669 |
+---------------+----------+
11 rows in set (6.31 sec)
```

## Launchpad ##
  * There were problems with the data in the following Launchpad tables for certain datasources:
|affected table name|datasource\_id with problems|
|:------------------|:---------------------------|
|lpd\_licenses      |286, 294, 302               |
|lpd\_milestones    |286, 294, 302               |
|lpd\_official\_bug\_tags|286, 294, 302               |
|lpd\_programming\_languages|286, 294, 302               |
|lpd\_releases      |286, 294, 302               |
|lpd\_series        |286, 294, 302               |

  * After deleting this bad data, the tables were re-created and data was re-inserted.
```
delete from lpd_licenses where datasource_id=x
delete from lpd_milestones where datasource_id=x
delete from lpd_official_bug_tags where datasource_id=x
delete from lpd_programming_languages where datasource_id=x
delete from lpd_releases where datasource_id=x
delete from lpd_series where datasource_id=x

mysqldump -umegan -p -h localhost ossmole_merged lpd_language_pairs lpd_official_bug_tags lpd_programming_languages lpd_projects lpd_releases lpd_series > lp.2012-May.sql

source lp.2012-May.sql

select datasource_id, count(*) from lpd_projects group by 1;

+---------------+----------+
| datasource_id | count(*) |
+---------------+----------+
|           272 |    23369 |
|           286 |    24374 |
|           294 |    25148 |
|           302 |    26072 |
|           312 |    27570 |
+---------------+----------+
5 rows in set (0.19 sec)
```

## Objectweb ##
```
mysqldump -umegan -p -h localhost ossmole_merged ow_developer_projects ow_developers ow_project_description ow_project_environment ow_project_indexes ow_project_intended_audience ow_project_licenses ow_project_operating_system ow_project_programming_language ow_project_status ow_project_topic ow_projects > ow.2012-May.sql

source ow.2012-May.sql

select datasource_id, count(*) from ow_projects group by 1;
+---------------+----------+
| datasource_id | count(*) |
+---------------+----------+
|            27 |      125 |
|            32 |      108 |
|            36 |      122 |
|            40 |      114 |
|            44 |      114 |
|            49 |      114 |
|            54 |      108 |
|            60 |      114 |
|            65 |      114 |
|            71 |      116 |
|            77 |      116 |
|            83 |      117 |
|            89 |      118 |
|            96 |      119 |
|           101 |      119 |
|           106 |      120 |
|           109 |      120 |
|           113 |      120 |
|           117 |      120 |
|           122 |      120 |
|           126 |      120 |
|           131 |      120 |
|           135 |      120 |
|           141 |      122 |
|           146 |      123 |
|           153 |      123 |
|           158 |      125 |
|           162 |      125 |
|           167 |      125 |
|           170 |      127 |
|           175 |      129 |
|           180 |      129 |
|           185 |      130 |
|           190 |      132 |
|           196 |      135 |
|           202 |      135 |
|           220 |      140 |
|           230 |      142 |
|           239 |      143 |
|           249 |      144 |
|           257 |      143 |
|           267 |      144 |
|           280 |      145 |
|           290 |      147 |
|           299 |      147 |
|           308 |      147 |
+---------------+----------+
46 rows in set (0.08 sec)
```

## Rubyforge ##
```
mysqldump -umegan -p -h localhost ossmole_merged [rf tables] > rf.2012-May.sql

source rf.2012-May.sql

select datasource_id, count(*) from rf_projects group by 1;

+---------------+----------+
| datasource_id | count(*) |
+---------------+----------+
|            24 |     1732 |
|            30 |     1891 |
|            31 |     1998 |
|            35 |     2144 |
|            39 |     2499 |
|            43 |     2626 |
|            48 |     2784 |
|            53 |     2951 |
|            59 |     3126 |
|            64 |     3304 |
|            70 |     3505 |
|            76 |     3657 |
|            82 |     3857 |
|            88 |     4059 |
|            95 |     4241 |
|           100 |     4433 |
|           105 |     4648 |
|           108 |     4835 |
|           112 |     5069 |
|           116 |     5309 |
|           121 |     5534 |
|           125 |     5615 |
|           134 |     6131 |
|           140 |     6302 |
|           145 |     6595 |
|           152 |     6894 |
|           157 |     7199 |
|           161 |     7359 |
|           166 |     7506 |
|           169 |     7678 |
|           174 |     7849 |
|           179 |     8040 |
|           184 |     8262 |
|           189 |     8386 |
|           195 |     8523 |
|           201 |     8595 |
|           208 |     8737 |
|           219 |     8816 |
|           229 |     8944 |
|           238 |     9095 |
|           248 |     9156 |
|           256 |     9178 |
|           266 |     9199 |
|           279 |     9264 |
|           289 |     9282 |
|           298 |     9341 |
|           307 |     9407 |
+---------------+----------+
47 rows in set (0.18 sec)
```

## Sourceforge ##
no changes.

## Savannah ##

```
mysqldump -umegan -p -h localhost ossmole_merged sv_dev_skills sv_developer_projects sv_developers sv_project_indexes sv_projects > sv.2012-May.sql

source sv.2012-May.sql

select datasource_id, count(*) from sv_projects group by 1;

+---------------+----------+
| datasource_id | count(*) |
+---------------+----------+
|           177 |     2336 |
|           182 |     2336 |
|           192 |     2356 |
|           198 |     2363 |
|           204 |     2372 |
|           211 |     2405 |
|           224 |     2455 |
|           232 |     2477 |
|           241 |     2529 |
|           251 |     2542 |
|           259 |     2547 |
|           269 |     2551 |
|           282 |     2575 |
|           291 |     2597 |
|           300 |     2618 |
|           309 |     2634 |
+---------------+----------+
16 rows in set (0.13 sec)
```

## Tigris ##

```
mysqldump -umegan -p -h localhost ossmole_merged tig_people tig_project_categories tig_projects > tig.2012-May.sql

mysqldump -umegan -p -h localhost ossmole_merged tig_project_developer_indexes > tig_dev_index.2012-May.sql

mysqldump -umegan -p -h localhost ossmole_merged tig_project_developer_roles > tig_dev_roles.2012-May.sql

mysqldump -umegan -p -h localhost ossmole_merged tig_messages > tig_messages.2012-May.sql

mysqldump -umegan -p -h localhost ossmole_merged tig_project_discussions > tig_proj_disc.2012-May.sql

mysqldump -umegan -p -h localhost ossmole_merged tig_project_discussion_indexes > tig_disc_ix.2012-May.sql

mysqldump -umegan -p -h localhost ossmole_merged tig_project_indexes > tig_proj_ix.2012-May.sql

mysqldump -umegan -p -h localhost ossmole_merged tig_project_list_indexes > tig_list_ix.2012-May.sql

source /home/megan/flossmole/backups/2012/2012-May/tig/tig.2012-May.sql
source /home/megan/flossmole/backups/2012/2012-May/tig/tig_dev_index.2012-May.sql
source /home/megan/flossmole/backups/2012/2012-May/tig/tig_dev_roles.2012-May.sql
source /home/megan/flossmole/backups/2012/2012-May/tig/tig_messages.2012-May.sql
source /home/megan/flossmole/backups/2012/2012-May/tig/tig_disc_ix.2012-May.sql
source /home/megan/flossmole/backups/2012/2012-May/tig/tig_proj_disc.2012-May.sql
source /home/megan/flossmole/backups/2012/2012-May/tig/tig_proj_ix.2012-May.sql
source /home/megan/flossmole/backups/2012/2012-May/tig/tig_list_ix.2012-May.sql

select datasource_id, count(*) from tig_projects group by 1;

+---------------+----------+
| datasource_id | count(*) |
+---------------+----------+
|           284 |      691 |
|           293 |      692 |
|           301 |      690 |
|           310 |      690 |
+---------------+----------+
4 rows in set (0.08 sec)

```