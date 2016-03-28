# Introduction #

This is a reverse-chronological log of things we've done on this project for the month of July 2010. Think of it as a journal of changes and features. An attempt at non-email-based institutional memory.

# Details #
## July 21, 2010 ##
### Parsers ###
  * parsing Google Code requires pulling the following from main page and put into table:
    * code license - new column in projects table (done)
    * activity level - new column in projects table (done)
    * content license (opt) - new column in projects table (done)
    * content from main page (paragraph description area) - new column in projects table (done)
    * summary from main page (tag line) - new column in projects table (done)
    * label(s) from main page - needs new table (done)
```
 CREATE TABLE `ossmole_merged`.`gc_project_labels` (
`proj_name` VARCHAR( 255 ) NOT NULL ,
`datasource_id` INT NOT NULL ,
`label` VARCHAR( 255 ) NOT NULL ,
`last_updated` DATETIME NOT NULL ,
PRIMARY KEY ( `proj_name` , `datasource_id` , `label` )
) ENGINE = MYISAM COMMENT = 'this holds the optional labels for a project' 
```
    * link(s) from main page - needs new table (done)
```
 CREATE TABLE `ossmole_merged`.`gc_project_links` (
`proj_name` VARCHAR( 255 ) NOT NULL ,
`datasource_id` INT NOT NULL ,
`link_title` VARCHAR( 255 ) NOT NULL,
`link` VARCHAR( 255 ) NOT NULL ,
`last_updated` DATETIME NOT NULL ,
PRIMARY KEY ( `proj_name` , `datasource_id` , `link` )
) ENGINE = MYISAM COMMENT = 'this holds the optional external links listed for a project' 
```
    * blog(s) from main page - needs new table (done)
```
 CREATE TABLE `ossmole_merged`.`gc_project_blogs` (
`proj_name` VARCHAR( 255 ) NOT NULL ,
`datasource_id` INT NOT NULL ,
`blog_title` VARCHAR( 255 ) NOT NULL ,
`blog_link` VARCHAR( 255 ) NOT NULL,
`last_updated` DATETIME NOT NULL ,
PRIMARY KEY ( `proj_name` , `datasource_id` , `blog_link` )
) ENGINE = MYISAM COMMENT = 'this holds the optional external blog title/link listed for a project' 
```
  * pull people from 'people' and 'roles' html pages and add to new table gc\_project\_people (each person should have only one role so this is a single table) (done)
```
 CREATE TABLE `ossmole_merged`.`gc_project_people` (
`proj_name` VARCHAR( 255 ) NOT NULL ,
`datasource_id` INT NOT NULL ,
`person_name` VARCHAR( 255 ) NOT NULL ,
`role` VARCHAR( 255 ) NOT NULL ,
`duties` VARCHAR( 255 ) NOT NULL ,
`notes` VARCHAR( 255 ) NOT NULL ,
`last_updated` DATETIME NOT NULL ,
PRIMARY KEY ( `proj_name` , `datasource_id` , `person_name` )
) ENGINE = MYISAM 
```
  * not really sure what to do with updates, wiki, downloads, or issues html yet. We have this raw html but what to parse out?? Maybe count of downloadable items? Count of issues? Other?

## July 15, 2010 ##
### Collectors ###
  * google code is done. Miracle! Now to parse it. Sigh.

### Database Administration ###
ran on test and prod:
```
ALTER TABLE `gc_projects` ADD `code_license` VARCHAR( 100 ) NULL COMMENT 'code license chosen',
ADD `activity_level` VARCHAR( 50 ) NULL COMMENT 'the word describing the activity level',
ADD `content_license` VARCHAR( 100 ) NULL COMMENT 'content license (optional)';

ALTER TABLE `gc_projects` ADD `project_summary` VARCHAR(255) NULL COMMENT 'short tag line',
ADD `project_description` text NULL COMMENT 'the longer description of the project';
```

---

## July 14, 2010 ##
### Collectors ###
  * google code still chugging along 58K projects completed; 108K to go. Ecstatic!!

---

## July 9, 2010 ##
### Collectors ###
  * google code still running
  * carter getting errors with launchpad API
  * carter making a plan for linux gentoo metric collection

### Teragrid ###
  * I need to run a Teragrid backup - still waiting for GC to finish

### Administrative ###
  * thinking about grants