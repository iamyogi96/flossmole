# Introduction #

This is a reverse-chronological list of changes & projects made in April 2011


# Details #
## April 29, 2011 ##
  * added following indexes to TG:
```
#Indexes and PKs on udd_* tables
#===============================
ALTER TABLE `udd_archived_bugs` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_archived_bugs_blockedby` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_archived_bugs_blocks` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_archived_bugs_fixed_in` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_archived_bugs_found_in` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_archived_bugs_merged_with` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_archived_bugs_packages` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_archived_bugs_tags` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_bugs` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_bugs_blockedby` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_bugs_blocks` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_bugs_fixed_in` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_bugs_found_in` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_bugs_merged_with` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_bugs_packages` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_bugs_tags` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_bugs_usertags` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_carnivore_emails` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_carnivore_keys` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_carnivore_login` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_carnivore_names` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_package_removal` ADD INDEX ( `datasource_id` , `batch_id` ) ;
ALTER TABLE `udd_package_removal_batch` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_timestamps` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_ubuntu_bugs` ADD INDEX ( `datasource_id` , `bug` ) ;
ALTER TABLE `udd_ubuntu_bugs_duplicates` ADD INDEX ( `datasource_id` , `bug` ) ;
ALTER TABLE `udd_ubuntu_bugs_subscribers` ADD INDEX ( `datasource_id` , `bug` ) ;
ALTER TABLE `udd_ubuntu_bugs_tags` ADD INDEX ( `datasource_id` , `bug` ) ;
ALTER TABLE `udd_ubuntu_bugs_tasks` ADD INDEX ( `datasource_id` , `bug` ) ;
ALTER TABLE `udd_upload_history_closes` ADD INDEX ( `datasource_id` , `bug` ) ;

#unable to add indexes to text columns, so add'l mods needed:

#SELECT max(length(package)) FROM `udd_bibref`

#udd_bibref
ALTER TABLE `udd_bibref` CHANGE `package` `package` VARCHAR(30) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL;
ALTER TABLE `udd_bibref` ADD INDEX( `datasource_id`, `package`);

#udd_ddtp 
# Affected rows: 164060
ALTER TABLE `udd_ddtp` CHANGE `package` `package` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_ddtp` ADD INDEX ( `datasource_id` , `package` ) ;

#udd_debtags 
# Affected rows: 231102
ALTER TABLE `udd_debtags` CHANGE `package` `package` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_debtags` ADD INDEX ( `datasource_id` , `package` ) ;

#udd_deferred
# 15 rows
ALTER TABLE `udd_deferred` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_deferred` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_deferred_architecture
# 32 rows
ALTER TABLE `udd_deferred_architecture` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_deferred_architecture` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_deferred_binary
# 41 rows
ALTER TABLE `udd_deferred_binary` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_deferred_binary` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_deferred_closes
# 376 rows
ALTER TABLE `udd_deferred_closes` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_deferred_closes` ADD INDEX (`source` ) ;

#udd_dehs
ALTER TABLE `udd_dehs` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_dehs` ADD INDEX (`source` ) ;

#udd_derivatives_packages
# Affected rows: 106695
ALTER TABLE `udd_derivatives_packages` CHANGE `package` `package` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_derivatives_packages` ADD INDEX ( `datasource_id` , `package` ) ;

#udd_derivatives_packages_distrelcomparch
# Affected rows: 31
ALTER TABLE `udd_derivatives_packages_distrelcomparch` CHANGE `distribution` `distribution` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_derivatives_packages_distrelcomparch` ADD INDEX ( `datasource_id` , `distribution` ) ;

#udd_derivatives_packages_summary
# Affected rows: 58973
ALTER TABLE `udd_derivatives_packages_summary` CHANGE `package` `package` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_derivatives_packages_summary` ADD INDEX ( `datasource_id` , `package` ) ;

#udd_derivatives_sources
# Affected rows: 93
ALTER TABLE `udd_derivatives_sources` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_derivatives_sources` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_derivatives_uploaders
# Affected rows: 276
ALTER TABLE `udd_derivatives_uploaders` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_derivatives_uploaders` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_hints
# Affected rows: 168
ALTER TABLE `udd_hints` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_hints` ADD INDEX ( `datasource_id` , `source` ) ;



#udd_lintian
# Affected rows: 164273
ALTER TABLE `udd_lintian` CHANGE `package` `package` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_lintian` ADD INDEX ( `datasource_id` , `package` ) ;

#udd_migrations
# Affected rows: 20966
ALTER TABLE `udd_migrations` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_migrations` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_new_packages
# Affected rows: 441
ALTER TABLE `udd_new_packages` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_new_packages` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_new_sources
# Affected rows: 229
ALTER TABLE `udd_new_sources` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_new_sources` ADD INDEX ( `datasource_id` , `source` ) ;

# udd_orphaned_packages
# Affected rows: 559
ALTER TABLE `udd_orphaned_packages` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_orphaned_packages` ADD INDEX ( `datasource_id` , `source` ) ;

# udd_packages
# Affected rows: 1017982
ALTER TABLE `udd_packages` CHANGE `package` `package` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_packages` ADD INDEX ( `datasource_id` , `package` ) ;

#udd_packages_distrelcomparch - check released column, why are all null?
# Affected rows: 560
ALTER TABLE `udd_packages_distrelcomparch` CHANGE `distribution` `distribution` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_packages_distrelcomparch` ADD INDEX ( `datasource_id` , `distribution` ) ;

#udd_packages_summary
# Affected rows: 169328
ALTER TABLE `udd_packages_summary` CHANGE `package` `package` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_packages_summary` ADD INDEX ( `datasource_id` , `package` ) ;

#udd_popcon
ALTER TABLE `udd_popcon` CHANGE `package` `package` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_popcon` ADD INDEX ( `datasource_id` , `package` ) ;

#udd_popcon_src
ALTER TABLE `udd_popcon_src` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL;
ALTER TABLE `udd_popcon_src` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_popcon_src_average
ALTER TABLE `udd_popcon_src_average` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_popcon_src_average` ADD INDEX ( `datasource_id` , `source` ) ;

# udd_releases - check releasedate column and why is squeeze not filled in?

#udd_screenshots
ALTER TABLE `udd_screenshots` CHANGE `package` `package` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_screenshots` ADD INDEX ( `datasource_id` , `package` ) ;

#udd_sources - text
ALTER TABLE `udd_sources` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_sources` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_sources_count - small table
ALTER TABLE `udd_sources_count` ADD INDEX ( `datasource_id`);

#udd_ubuntu_packages - text
ALTER TABLE `udd_ubuntu_packages` CHANGE `package` `package` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_ubuntu_packages` ADD INDEX ( `datasource_id` , `package` ) ;

#udd_ubuntu_packages_distrelcomparch
ALTER TABLE `udd_ubuntu_packages_distrelcomparch` CHANGE `distribution` `distribution` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL ;
ALTER TABLE `udd_ubuntu_packages_distrelcomparch` ADD INDEX ( `datasource_id` , `distribution` ) ;

#udd_ubuntu_packages_summary
ALTER TABLE `udd_ubuntu_packages_summary` CHANGE `package` `package` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL ;
ALTER TABLE `udd_ubuntu_packages_summary` ADD INDEX ( `datasource_id` , `package` ) ;

#udd_ubuntu_popcon
ALTER TABLE `udd_ubuntu_popcon` CHANGE `package` `package` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_ubuntu_popcon` ADD INDEX ( `datasource_id` , `package` ) ;

#udd_ubuntu_popcon_src
ALTER TABLE `udd_ubuntu_popcon_src` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_ubuntu_popcon_src` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_ubuntu_popcon_src_average
ALTER TABLE `udd_ubuntu_popcon_src_average` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_ubuntu_popcon_src_average` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_ubuntu_sources
ALTER TABLE `udd_ubuntu_sources` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_ubuntu_sources` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_ubuntu_uploaders
ALTER TABLE `udd_ubuntu_uploaders` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL ;
ALTER TABLE `udd_ubuntu_uploaders` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_upload_history
ALTER TABLE `udd_upload_history` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_upload_history` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_upload_history_architecture
ALTER TABLE `udd_upload_history_architecture` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_upload_history_architecture` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_uploaders
ALTER TABLE `udd_uploaders` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL ;
ALTER TABLE `udd_uploaders` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_wannabuild - text
ALTER TABLE `udd_wannabuild` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_wannabuild` ADD INDEX ( `datasource_id` , `source` ) ;

```
## April 28, 2011 ##
  * in prep for moving grid0 to grid6
  * work on indexes
  * work on paper
## April 27, 2011 ##
  * Use the following to see how long the varchar needs to be:
```
SELECT max(length(package)) FROM `udd_bibref`
```

  * Then run these to alter the table to fit
  * Note that their are still a metric ton of columns that are marked text and probably should be varchar. Argh.
```
#udd_bibref
ALTER TABLE `udd_bibref` CHANGE `package` `package` VARCHAR(30) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL;
ALTER TABLE `udd_bibref` ADD INDEX( `datasource_id`, `package`);

#udd_ddtp 
# Affected rows: 164060
ALTER TABLE `udd_ddtp` CHANGE `package` `package` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_ddtp` ADD INDEX ( `datasource_id` , `package` ) ;

#udd_debtags 
# Affected rows: 231102
ALTER TABLE `udd_debtags` CHANGE `package` `package` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_debtags` ADD INDEX ( `datasource_id` , `package` ) ;

#udd_deferred
# 15 rows
ALTER TABLE `udd_deferred` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_deferred` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_deferred_architecture
# 32 rows
ALTER TABLE `udd_deferred_architecture` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_deferred_architecture` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_deferred_binary
# 41 rows
ALTER TABLE `udd_deferred_binary` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_deferred_binary` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_deferred_closes
# 376 rows
ALTER TABLE `udd_deferred_closes` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_deferred_closes` ADD INDEX (`source` ) ;

#udd_dehs
ALTER TABLE `udd_dehs` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_dehs` ADD INDEX (`source` ) ;

#udd_derivatives_packages
# Affected rows: 106695
ALTER TABLE `udd_derivatives_packages` CHANGE `package` `package` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_derivatives_packages` ADD INDEX ( `datasource_id` , `package` ) ;

#udd_derivatives_packages_distrelcomparch
# Affected rows: 31
ALTER TABLE `udd_derivatives_packages_distrelcomparch` CHANGE `distribution` `distribution` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_derivatives_packages_distrelcomparch` ADD INDEX ( `datasource_id` , `distribution` ) ;

#udd_derivatives_packages_summary
# Affected rows: 58973
ALTER TABLE `udd_derivatives_packages_summary` CHANGE `package` `package` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_derivatives_packages_summary` ADD INDEX ( `datasource_id` , `package` ) ;

#udd_derivatives_sources
# Affected rows: 93
ALTER TABLE `udd_derivatives_sources` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_derivatives_sources` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_derivatives_uploaders
# Affected rows: 276
ALTER TABLE `udd_derivatives_uploaders` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_derivatives_uploaders` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_hints
# Affected rows: 168
ALTER TABLE `udd_hints` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_hints` ADD INDEX ( `datasource_id` , `source` ) ;



#udd_lintian
# Affected rows: 164273
ALTER TABLE `udd_lintian` CHANGE `package` `package` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_lintian` ADD INDEX ( `datasource_id` , `package` ) ;

#udd_migrations
# Affected rows: 20966
ALTER TABLE `udd_migrations` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_migrations` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_new_packages
# Affected rows: 441
ALTER TABLE `udd_new_packages` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_new_packages` ADD INDEX ( `datasource_id` , `source` ) ;

#udd_new_sources
# Affected rows: 229
ALTER TABLE `udd_new_sources` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_new_sources` ADD INDEX ( `datasource_id` , `source` ) ;

# udd_orphaned_packages
# Affected rows: 559
ALTER TABLE `udd_orphaned_packages` CHANGE `source` `source` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_orphaned_packages` ADD INDEX ( `datasource_id` , `source` ) ;

SELECT max(length(package)) FROM `udd_packages_distrelcomparch`

# udd_packages
# Affected rows: 1017982
ALTER TABLE `udd_packages` CHANGE `package` `package` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_packages` ADD INDEX ( `datasource_id` , `package` ) ;


#udd_packages_distrelcomparch - check released column, why are all null?
# Affected rows: 560
ALTER TABLE `udd_packages_distrelcomparch` CHANGE `distribution` `distribution` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_packages_distrelcomparch` ADD INDEX ( `datasource_id` , `distribution` ) ;

#udd_packages_summary
# Affected rows: 169328
ALTER TABLE `udd_packages_summary` CHANGE `package` `package` VARCHAR( 100 ) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ;
ALTER TABLE `udd_packages_summary` ADD INDEX ( `datasource_id` , `package` ) ;
```
## April 26, 2011 ##
  * worked on UDD tables; added indexes (below) uploaded to teragrid
```
ALTER TABLE `udd_archived_bugs` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_archived_bugs_blockedby` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_archived_bugs_blocks` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_archived_bugs_fixed_in` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_archived_bugs_found_in` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_archived_bugs_merged_with` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_archived_bugs_packages` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_archived_bugs_tags` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_bugs` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_bugs_blockedby` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_bugs_blocks` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_bugs_fixed_in` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_bugs_found_in` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_bugs_merged_with` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_bugs_packages` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_bugs_tags` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_bugs_usertags` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_carnivore_emails` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_carnivore_keys` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_carnivore_login` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_carnivore_names` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_package_removal` ADD INDEX ( `datasource_id` , `batch_id` ) ;
ALTER TABLE `udd_package_removal_batch` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_timestamps` ADD INDEX ( `datasource_id` , `id` ) ;
ALTER TABLE `udd_ubuntu_bugs` ADD INDEX ( `datasource_id` , `bug` ) ;
ALTER TABLE `udd_ubuntu_bugs_duplicates` ADD INDEX ( `datasource_id` , `bug` ) ;
ALTER TABLE `udd_ubuntu_bugs_subscribers` ADD INDEX ( `datasource_id` , `bug` ) ;
ALTER TABLE `udd_ubuntu_bugs_tags` ADD INDEX ( `datasource_id` , `bug` ) ;
ALTER TABLE `udd_ubuntu_bugs_tasks` ADD INDEX ( `datasource_id` , `bug` ) ;
ALTER TABLE `udd_upload_history_closes` ADD INDEX ( `datasource_id` , `bug` ) ;
```
## April 20-22, 2011 ##
  * entered rest of msr papers, annotated
  * entered papers from "What we know" into flosshub; all those having to do with repositories or non-survey data; nearly 400 papers now
## April 15, 2011 ##
  * meet with David Williams about summer research assistantship
  * meet with Carter, weekly meeting
  * entered 2008 and 2009 paper attachments into flosshub
## April 14, 2011 ##
  * entered 2007, 2006, 2004, and half of 2005 msr papers into flosshub
  * talked to Carter about funding
## April 13, 2011 ##
  * entered 2009 msr papers into flosshub (took 43 minutes to add all papers using DOI and enter keywords and abstracts)
  * entered 2010 msr papers into flosshub
  * DID NOT ENTER non-floss papers!
  * con call on CCC report
  * entered 2008 msr papers into flosshub
  * asked about search/upload in flosshub paper repository
## April 6-12, 2011 ##
  * working with Carter on uploading UDD code
  * new Debian provenance table - needs to be filled before sending 3 Debian datasources to upload
  * worked on master list of papers for replication study
  * asked for and got flosshub admin to work on papers there (upload msr paper list)
  * need msr papers from 2009 and 2010 (IEEE only)

## April 5, 2011 ##
  * finished rubyforge 256
  * finished freshmeat 255
  * finished Savannah 259
  * Teragrid backup

## April 4, 2011 ##
  * collected and released ObjectWeb data = 257
  * started rubyforge
  * started freshmeat
  * started Savannah
  * moved Deb Metrics (Jan) to production ds = 254
  * finished FSF = datasource 258

{{{list of datasources is as follows:
254 7 Deb Metrics
255 2 FM
256 3 RF
257 4 OW
258 5 FSF
259 10 SV
260 13 TG}}}

  * created SRDA doi file; it's in the queue to send to Germany