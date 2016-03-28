# Introduction #

This is a reverse-chronological list of changes for May 2011

# Details #
## May 23-27, 2011 ##
  * David: working on visualizations for "examples" page on flossmole.org
  * Carter: working on fixing up Debian code for release & instructions, starting Launchpad

## May 23, 2011 ##
  * student team meeting
  * worked on last 5 forges
  * google code still running

## May 14-19, 2011 ##
  * collected stats on various forges for forge\_stats table
  * started forge project stats and forge developer stats
  * google still running
  * con call with grant team

## May 11-12, 2011 ##
  * worked on filling forges tables
  * Google Code still chugging along

---

## May 10, 2011 ##
  * git training
  * working on forges tables

---

## May 9, 2011 ##
  * git training
  * working on forges tables
  * google code still running

---

## May 6, 2011 ##
  * Google still running
  * outline F paper
  * meeting with carter and david
  * con call with grant team

---

## Cinco de Mayo ##
  * Google still running
  * signup for github learning thingie
  * go over to-do list
  * start F paper

---

## May 4, 2011 ##
  * release rest of May data; backup to Teragrid all datasources > 262
  * work on paper; sent to Carter to review
  * work on student summer schedule & budget

---

## May 3, 2011 ##
  * worked on May release
### UDD ###
  * 263 = UDD bugfix (moved from test to prod)
```
mysqldump --host grid0.cs.elon.edu --port 3306 -umegan -p<password> --hex-blob --where='datasource_id=263' --result-file=263.sql --compact test udd_archived_bugs udd_archived_bugs_blockedby udd_archived_bugs_blocks udd_archived_bugs_fixed_in udd_archived_bugs_found_in udd_archived_bugs_merged_with udd_archived_bugs_packages udd_archived_bugs_tags udd_bibref udd_bugs udd_bugs_blockedby udd_bugs_blocks udd_bugs_fixed_in udd_bugs_found_in udd_bugs_merged_with udd_bugs_packages udd_bugs_tags udd_bugs_usertags udd_carnivore_emails udd_carnivore_keys udd_carnivore_login udd_carnivore_names udd_ddtp udd_debtags udd_deferred udd_deferred_architecture udd_deferred_binary udd_deferred_closes udd_dehs udd_derivatives_packages udd_derivatives_packages_distrelcomparch udd_derivatives_packages_summary udd_derivatives_sources udd_derivatives_uploaders udd_hints udd_lintian udd_migrations udd_new_packages udd_new_sources udd_orphaned_packages udd_package_removal udd_package_removal_batch udd_packages udd_packages_distrelcomparch udd_packages_summary udd_popcon udd_popcon_src udd_popcon_src_average udd_releases udd_screenshots udd_sources udd_sources_count udd_timestamps udd_ubuntu_bugs udd_ubuntu_bugs_duplicates udd_ubuntu_bugs_subscribers udd_ubuntu_bugs_tags udd_ubuntu_bugs_tasks udd_ubuntu_packages udd_ubuntu_packages_distrelcomparch udd_ubuntu_packages_summary udd_ubuntu_popcon udd_ubuntu_popcon_src udd_ubuntu_popcon_src_average udd_ubuntu_sources udd_ubuntu_uploaders udd_upload_history udd_upload_history_architecture udd_upload_history_closes udd_uploaders udd_wannabuild

mysql -hlocalhost -umegan -p
use ossmole_merged;
source 263.sql
```
  * 264 = UDD bugfix (moved from test to prod)
```
mysqldump --host grid0.cs.elon.edu --port 3306 -umegan -p<password> --hex-blob --where='datasource_id=264' --result-file=264.sql --compact test udd_archived_bugs udd_archived_bugs_blockedby udd_archived_bugs_blocks udd_archived_bugs_fixed_in udd_archived_bugs_found_in udd_archived_bugs_merged_with udd_archived_bugs_packages udd_archived_bugs_tags udd_bibref udd_bugs udd_bugs_blockedby udd_bugs_blocks udd_bugs_fixed_in udd_bugs_found_in udd_bugs_merged_with udd_bugs_packages udd_bugs_tags udd_bugs_usertags udd_carnivore_emails udd_carnivore_keys udd_carnivore_login udd_carnivore_names udd_ddtp udd_debtags udd_deferred udd_deferred_architecture udd_deferred_binary udd_deferred_closes udd_dehs udd_derivatives_packages udd_derivatives_packages_distrelcomparch udd_derivatives_packages_summary udd_derivatives_sources udd_derivatives_uploaders udd_hints udd_lintian udd_migrations udd_new_packages udd_new_sources udd_orphaned_packages udd_package_removal udd_package_removal_batch udd_packages udd_packages_distrelcomparch udd_packages_summary udd_popcon udd_popcon_src udd_popcon_src_average udd_releases udd_screenshots udd_sources udd_sources_count udd_timestamps udd_ubuntu_bugs udd_ubuntu_bugs_duplicates udd_ubuntu_bugs_subscribers udd_ubuntu_bugs_tags udd_ubuntu_bugs_tasks udd_ubuntu_packages udd_ubuntu_packages_distrelcomparch udd_ubuntu_packages_summary udd_ubuntu_popcon udd_ubuntu_popcon_src udd_ubuntu_popcon_src_average udd_ubuntu_sources udd_ubuntu_uploaders udd_upload_history udd_upload_history_architecture udd_upload_history_closes udd_uploaders udd_wannabuild

```

  * 265 = UDD may (moved from test to prod)
```
mysqldump --host grid0.cs.elon.edu --port 3306 -umegan -p<password> --hex-blob --where='datasource_id=265' --result-file=265.sql --compact test udd_archived_bugs udd_archived_bugs_blockedby udd_archived_bugs_blocks udd_archived_bugs_fixed_in udd_archived_bugs_found_in udd_archived_bugs_merged_with udd_archived_bugs_packages udd_archived_bugs_tags udd_bibref udd_bugs udd_bugs_blockedby udd_bugs_blocks udd_bugs_fixed_in udd_bugs_found_in udd_bugs_merged_with udd_bugs_packages udd_bugs_tags udd_bugs_usertags udd_carnivore_emails udd_carnivore_keys udd_carnivore_login udd_carnivore_names udd_ddtp udd_debtags udd_deferred udd_deferred_architecture udd_deferred_binary udd_deferred_closes udd_dehs udd_derivatives_packages udd_derivatives_packages_distrelcomparch udd_derivatives_packages_summary udd_derivatives_sources udd_derivatives_uploaders udd_hints udd_lintian udd_migrations udd_new_packages udd_new_sources udd_orphaned_packages udd_package_removal udd_package_removal_batch udd_packages udd_packages_distrelcomparch udd_packages_summary udd_popcon udd_popcon_src udd_popcon_src_average udd_releases udd_screenshots udd_sources udd_sources_count udd_timestamps udd_ubuntu_bugs udd_ubuntu_bugs_duplicates udd_ubuntu_bugs_subscribers udd_ubuntu_bugs_tags udd_ubuntu_bugs_tasks udd_ubuntu_packages udd_ubuntu_packages_distrelcomparch udd_ubuntu_packages_summary udd_ubuntu_popcon udd_ubuntu_popcon_src udd_ubuntu_popcon_src_average udd_ubuntu_sources udd_ubuntu_uploaders udd_upload_history udd_upload_history_architecture udd_upload_history_closes udd_uploaders udd_wannabuild

```
### May datasources ###
  * 266 Rubyforge
  * 267 Objectweb
  * 268 Free Software Foundation
  * 269 Savannah
  * 270 Freshmeat

---

## May 2, 2011 ##
  * con call about grant
  * worked on Debian queries
  * looked at paper on software release history
  * paper deadline extended until Saturday