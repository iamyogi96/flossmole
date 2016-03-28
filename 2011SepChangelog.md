# Introduction #

This is a list of stuff we've done in September 2011

# Details #
## September 5, 2011 ##
  * released tigris
  * released github
  * think about what to do about Teragrid index releases. Right now I am using the datamart sql files to populate Teragrid. I'll need to write scripts to upload the index files there also. This is quite large.
## September 2, 2011 ##
  * released rubyforge
  * released alioth
  * created new tables at teragrid alioth
  * need a way to upload indexes (not in datamarts) to teragrid automatically - write this!
## September 1, 2011 ##
  * updated all Objectweb code (c) statements and database connection info
  * asked Joel to update perl modules on grid6 for collectors (needs XML/Parser.pm, LWP/Simple.pm), and java interpreter
  * released ObjectWeb, Free Software Foundation, Savannah code to Google Code
  * updated Savannah database connection info & file
  * Tigris: ran SQL creates from this file (http://flossmole.googlecode.com/svn/FLOSSmoleTigris/creates.sql)
  * deprecated tg prefix tables to have prefix "old". New tigris tables all start with "tig". Did this on both PROD and TEST.
  * asked Carter about small possible bug with tigris collector - developers not getting written to database
  * removed old Tigris and Alioth runs from test database
  * added code to Objectweb/FSF/Savannah/Rubyforge to automatically update to Teragrid after Google Code. Nice! save a step...
  * opened new feature request to add a README to Debian Metrics package.