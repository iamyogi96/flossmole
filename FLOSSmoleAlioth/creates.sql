create table al_messages
(
  datasource_id int not null,
  message_id varchar(255) not null,
  mailing_list varchar(255),
  subject varchar(255),
  sender varchar(255),
  reply_to varchar(255),
  date_sent datetime,
  body mediumtext,
  url varchar(255),
  primary key (message_id, mailing_list)
);

create table al_messages_references
(
  datasource_id int not null,
  message_id varchar(255) not null,
  mailing_list varchar(255) not null,
  reference varchar(255) not null,
  primary key (message_id, mailing_list, reference)
);

/* this will be collected every run, as descriptions can change */
create table al_mailing_lists
(
  datasource_id int not null,
  mailing_list varchar(255) not null,
  project varchar(255) not null,
  description varchar(255),
  primary key (datasource_id, mailing_list, project)
);

create table al_project_indexes
(
  datasource_id int not null,
  page int not null,
  id int not null auto_increment primary key,
  html mediumtext
);

create table al_mailing_lists_indexes
(
  datasource_id int not null,
  project varchar(255) not null,
  html mediumtext,
  primary key (datasource_id, project)
);


/* Will add projects later */

create table al_projects
(
  datasource_id int not null,
  display_name varchar(255),
  unixname varchar(255) not null,
  short_desc mediumtext,
  registered datetime,
  primary key(datasource_id, unixname)
);

create table al_projects_audience
(
  datasource_id int not null,
  audience varchar(255) not null,
  unixname varchar(255) not null,
  primary key(datasource_id,audience,unixname)
);


create table al_projects_os
(
  datasource_id int not null,
  os varchar(255) not null,
  unixname varchar(255) not null,
  primary key(datasource_id,os,unixname)
);


create table al_projects_status
(
  datasource_id int not null,
  status varchar(255) not null,
  unixname varchar(255) not null,
  primary key(datasource_id,status,unixname)
);


create table al_projects_license
(
  datasource_id int not null,
  license varchar(255) not null,
  unixname varchar(255) not null,
  primary key(datasource_id,license,unixname)
);


create table al_projects_environment
(
  datasource_id int not null,
  environment varchar(255) not null,
  unixname varchar(255) not null,
  primary key(datasource_id,environment,unixname)
);


create table al_projects_topic
(
  datasource_id int not null,
  topic varchar(255) not null,
  unixname varchar(255) not null,
  primary key(datasource_id,topic,unixname)
);


create table al_projects_language
(
  datasource_id int not null,
  language varchar(255) not null,
  unixname varchar(255) not null,
  primary key(datasource_id,language,unixname)
);

create table al_messages_indexes
(
  datasource_id int not null,
  url varchar(255) not null primary key,
  mailing_list varchar(255),
  list_index mediumtext
);
