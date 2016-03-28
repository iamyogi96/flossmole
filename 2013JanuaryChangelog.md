# January 2, 2013 #
  * move "old" tables to new schema called "old"

## old alioth ##
```
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged old_al_mailing_lists old_al_mailing_lists_indexes old_al_messages old_al_messages_indexes old_al_messages_references  > old.al.sql
```

## old debian ##
```
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged old_debian_projects old_debian_project_developers old_debian_copyright_urls old_debian_project_indexes_stable old_debian_project_indexes_testing old_debian_project_indexes_unstable > old.debian.sql
```

## old fsf ##
```
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged old_fsf_language_pairs old_fsf_project_interfaces old_fsf_project_languages > old.fsf.sql
```


## old launchpad ##
```
mysqldump --extended-insert=TRUE --compact --no-create-info -umegan -p -hlocalhost ossmole_merged old_lp_developers old_lp_developer_indexes old_lp_developer_irc old_lp_developer_languages old_lp_developer_projects old_lp_developer_wiki old_lp_groups old_lp_group_indexes old_lp_group_projects old_lp_projects old_lp_project_indexes old_lp_project_languages old_lp_project_licenses old_lp_project_uses > old.lp.all
```

## old SF ##
```
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged old_calculated_statistics  > sf.old_calc_stats.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged old_list_posts > sf.list_posts.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_developers > sf_developers.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_developer_indexes > sf_dev_indexes.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_projects > sf_projects.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_all_time_stats > sf_all_time.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_db_environment > sf_db_env.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_description > sf_p_desc.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_donors > sf_p_donors.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_environment > sf_env.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_intended_audience > sf_int_aud.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_licenses > sf_p_lic.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_list > sf_p_list.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_operating_system > sf_p_opsys.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_programming_language > sf_proglang.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_public_areas > sf_public.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_statistics > sf_stats.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_statistics_60 > sf_stats60.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_project_status > sf_status.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_topic > sf_topic.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_translations > sf_trans.sql
mysqldump --extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_user_interface > sf_userint.sql


#SF indexes
mysqldump --where='datasource_id=1'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes1.sql
mysqldump --where='datasource_id=2'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes2.sql
mysqldump --where='datasource_id=4'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes4.sql
mysqldump --where='datasource_id=5'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes5.sql
mysqldump --where='datasource_id=6'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes6.sql
mysqldump --where='datasource_id=7'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes7.sql
mysqldump --where='datasource_id=8'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes8.sql
mysqldump --where='datasource_id=13'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes13.sql
mysqldump --where='datasource_id=16'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes16.sql
mysqldump --where='datasource_id=19'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes19.sql
mysqldump --where='datasource_id=22'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes22.sql
mysqldump --where='datasource_id=28'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes28.sql
mysqldump --where='datasource_id=34'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes34.sql
mysqldump --where='datasource_id=38'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes38.sql
mysqldump --where='datasource_id=46'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes46.sql
mysqldump --where='datasource_id=57'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes57.sql
mysqldump --where='datasource_id=68'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes68.sql
mysqldump --where='datasource_id=80'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes80.sql
mysqldump --where='datasource_id=93'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes93.sql
mysqldump --where='datasource_id=103'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes103.sql
mysqldump --where='datasource_id=110'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes110.sql
mysqldump --where='datasource_id=119'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes119.sql
mysqldump --where='datasource_id=128'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes128.sql
mysqldump --where='datasource_id=137'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes137.sql
mysqldump --where='datasource_id=143'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes143.sql
mysqldump --where='datasource_id=150'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes150.sql
mysqldump --where='datasource_id=164'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes164.sql
mysqldump --where='datasource_id=172'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes172.sql
mysqldump --where='datasource_id=206'--extended-insert=TRUE --compact -umegan -p -hlocalhost ossmole_merged sf_project_indexes > sf_p_indexes206.sql

```