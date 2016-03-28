# December 21, 2012 #

  * Began user migration to flossdata.syr.edu
  * Received list of users from teragrid
  * Making a plan for how to add users

# December 13, 2012 #

Began database migration to flossdata.syr.edu

## udd and old structures ##
  * Created new databases for 'udd' tables and 'old' tables and 'sf' tables since these are only rarely used and there are a lot of them
  * Will insert data LAST since it's not highly desired

## ossmole\_merged database structure ##
  * Created ossmole\_merged database on flossdata.syr.edu
  * Created all tables

## ossmole\_merged data ##
I will do these by groups of forges, probably alphabetically.
### Alioth ###
  * Exported Alioth data - Alioth is small enough that I did all the data in one file:
```
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged al_project_indexes al_project_members al_project_members_roles al_projects al_projects_audience al_projects_environment al_projects_language al_projects_license al_projects_os al_projects_status al_projects_tags al_projects_topic > alioth.all.sql
```
  * Imported Alioth data
```
source alioth.all.sql
```
### datasources & forges ###
  * Exported all datasources
  * Exported all forges
```
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged datasources forges forge_stats forge_trove forge_trove_defs > dsforges.all.sql
```
  * Imported datasources & forges data, success
### deb\_metrics ###
  * Exported all debian metrics data
```
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged deb_metrics deb_metrics_popcon deb_metrics_provenance deb_metrics_sources deb_metrics_sources_arch deb_metrics_sources_bins deb_metrics_sources_deps > deb.all.sql
```
  * Imported
### Freshmeat/Freecode ###
  * Exported
```
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged fm_projects fm_project_authors fm_project_dependencies fm_project_homepages fm_project_tags fm_project_trove fm_trove_defs > fm.all.sql
```
  * Imported

### FSF ###
  * Exported
```
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged fsf_developer_projects fsf_projects fsf_project_categories fsf_project_indexes fsf_project_licenses fsf_project_related fsf_project_requirements > fsf.all.sql
```
  * Imported

### Github ###
  * Exported
```
#github
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged gh_projects > gh.all.sql
```
  * Imported

### Google Code ###
  * Exported
```
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged gc_developer_indexes > gc.1.sql
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged gc_issues_indexes > gc.2.sql
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged gc_projects > gc.3.sql
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged gc_project_blogs > gc.4.sql
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged gc_project_labels > gc.5.sql
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged gc_project_links > gc.6.sql
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged gc_project_people > gc.7.sql
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged gc_developer_projects > gc.8.sql
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged gc_project_groups > gc.9.sql
mysqldump --where='datasource_id=226' --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged gc_project_indexes > gc.10.sql
mysqldump --where='datasource_id=235' --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged gc_project_indexes > gc.11.sql
mysqldump --where='datasource_id=243' --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged gc_project_indexes > gc.12.sql
mysqldump --where='datasource_id=252' --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged gc_project_indexes > gc.13.sql
mysqldump --where='datasource_id=271' --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged gc_project_indexes > gc.14.sql
mysqldump --where='datasource_id=285' --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged gc_project_indexes > gc.15.sql
mysqldump --where='datasource_id=304' --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged gc_project_indexes > gc.16.sql
mysqldump --where='datasource_id=313' --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged gc_project_indexes > gc.17.sql
mysqldump --where='datasource_id=323' --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged gc_project_indexes > gc.18.sql
mysqldump --where='datasource_id=350' --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged gc_project_indexes > gc.19.sql
```
  * Imported
### Launchpad ###
```
#lpd
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged lpd_language_pairs lpd_licenses lpd_milestones lpd_official_bug_tags lpd_programming_languages lpd_projects lpd_releases lpd_series > lpd.all.sql
```
### ObjectWeb ###
```
#ow
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged ow_developer_projects ow_developers ow_project_description ow_project_environment ow_project_indexes ow_project_intended_audience ow_project_licenses ow_project_operating_system ow_project_programming_language ow_project_status ow_project_topic ow_projects > ow.all.sql
```
### Rubyforge ###
```
#rf
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged rf_developer_projects rf_developers rf_project_description rf_project_environment rf_project_indexes rf_project_intended_audience rf_project_licenses rf_project_natural_language rf_project_operating_system rf_project_programming_language rf_project_status rf_project_topic rf_projects  > rf.all.sql
```
### Sourcekibitzer ###
```
#sk
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged sk_projects > sk.all.sql
```
### Savannah ###
```
#sv
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged sv_dev_skills sv_developer_projects sv_developers sv_project_indexes sv_projects > sv.all.sql
```
### Tigris ###
```
#tig
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged tig_messages tig_people tig_project_categories tig_project_developer_indexes tig_project_developer_roles tig_project_discussion_indexes tig_project_discussions tig_project_indexes tig_project_list_indexes tig_projects > tig.all.sql
```