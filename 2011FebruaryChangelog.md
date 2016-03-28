# Introduction #
Reverse-Chronological list of changes made February 2011


# Details #
## February 24, 2011 ##
  * One DOI fix this morning; ready to go for March release
  * Google SOC application begun; all questions answered. Waiting on application to be released.
## February 23, 2011 ##
  * DOI generator scripts written
  * DOI for 62 data sources submitted to Germany
## February 22, 2011 ##
  * Google fixed the downloads page issue. yay
  * launchpad fixed and pages parsed, but still a few errors on filling in columns; probably a regex issue. Defect opened in Google Code.
  * Teragrid is blocked on Launchpad.
  * Working on DOI in the meantime.
## February 17, 2011 ##
  * federated search review of lit
  * mailing lists and natural language review of lit
  * Launchpad collector is done; but parser seems broken; entered bug for Carter to fix.
## February 16, 2011 ##
  * Better do a Teragrid backup since the Google Code downloads site is returning a 500-error for some reason. I'd really like to start Teragrid AFTER Launchpad finishes, but it's taking forever.
  * added 'dependencies' to Freshmeat data downloads. Not sure why, but this table had never been released. It will be next time. It has been in the database the whole time, just never released as flat files.
  * looked at Tigris mailing list data for the first time; thinking about natural language processing. Sent email to colleague on some ideas for this.
## February 15, 2011 ##
  * Released January data (fm, rf, ow, fsf, sv, gc, tg)
  * TODO: Pick up DOI where we left off
  * Debian data is released (need to document this somewhere besides in our paper)
    * export sql and data from test, move to production
    * change datasource to 246
    * drop rows that are not C or C++
    * release code to GC
  * Launchpad is still chugging along
  * github is still broken
## February 14, 2011 ##
  * Google increased our disk storage. File uploads are now finished.
  * Google Code parser has been re-written as of this afternoon; was getting errors on labels, activity levels, etc. Added functionality for groups.
```
CREATE TABLE IF NOT EXISTS `gc_project_groups` (
  `proj_name` varchar(100) NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `group_name` varchar(100) NOT NULL,
  `group_url` varchar(255) character set latin1 NOT NULL,
  `last_updated` datetime NOT NULL,
  PRIMARY KEY  (`proj_name`,`datasource_id`,`group_url`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='this holds the optional groups listed for a project';
```
  * Carter added column to Debian release data; I can now release the Debian metrics as soon as I get the data moved from dev into production.

## February 11, 2011 ##
  * moved many older legacy data files from SF to GC, but blocked on this task since the uploader quit working - I suspect we are out of disk space? Here is the error:
```
flossmole$ python googlecode_upload.py --summary="Sourceforge Project Descriptions: 2007-Aug" --project=flossmole --user=megansquire --password=password sfProjectDesc2007-Aug.txt.bz2
Please enter your googlecode.com username: 
```

No matter what I enter, it just asks for the password, then fails. (It should not even get this far since the username is given on the commandline. This just suddenly stopped working today after I had uploaded about 700 files between yesterday and today using this identical method.) In the past I have gotten this error when two things were wrong (1) ran out of disk space (2) badly formed .bz2 file. (I tested the bzipping in this case, and it was fine.)

## February 10, 2011 ##
  * Running Launchpad
  * Google Code still running (it's on developers)
  * As part of the DOI project I decided to finally get all the file releases into one location and to write a db-driven script system for doing file releases.
  * This means that the SF site will basically just hold our mailing list for now. At some point I'll move that too.
  1. Copy all files from grid0 to local
  1. copy all files from SF to local
  1. this should give me a complete set
  1. move any files from this set NOT already on Google Code up there
  1. fill new DB tables with DOI info
  1. write a script to generate new DOI records
  1. update release scripts to take into account new tables
  1. generate new DOI records and send to company
  1. test new release system with January data

## February 9, 2011 ##
  * working on new tables to hold information about releases. This will be used to generate DOI information.

## February 8, 2011 ##
  * add bugs to google
  * create new feature list
  * some notes on federated search and data integration

## February 7, 2011 ##
  * Google crawler still running; noticed developer collector is broken (only returning a hash of dev info if not logged in)
## February 6, 2011 ##
  * github collector broken; bug submitted to snorris
## February 4, 2011 ##
  * make list of Debian items to fix with ckozak
## January 31, 2011 ##
  * submit paper to conference