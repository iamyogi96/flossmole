create table tig_project_list_indexes
(
  datasource_id int not null,
  html mediumtext,
  last_updated datetime,
  primary key (datasource_id)
);

create table tig_project_indexes
(
  datasource_id int not null,
  unixname varchar(255),
  html mediumtext,
  last_updated datetime,
  primary key (datasource_id, unixname)
);

create table tig_projects
(
  datasource_id int not null,
  unixname varchar(255),
  description mediumtext,
  license mediumtext,
  body mediumtext,
  last_updated datetime,
  primary key (datasource_id, unixname)
);

create table tig_project_categories
(
  datasource_id int not null,
  project varchar(255),
  category varchar(255),
  last_updated datetime,
  primary key (datasource_id, project, category)
);

create table tig_people
(
  datasource_id int not null,
  username varchar(255),
  full_name varchar(255),
  last_updated datetime,
  primary key (datasource_id, username)
);


create table tig_project_developer_roles
(
  datasource_id int not null,
  project varchar(255),
  username varchar(255),
  role varchar(255),
  last_updated datetime,
  primary key (datasource_id, project, username, role)
);

create table tig_project_developer_indexes
(
  datasource_id int not null,
  project varchar(255),
  html mediumtext,
  last_updated datetime,
  primary key (datasource_id, project)
);

create table tig_project_discussion_indexes
(
  datasource_id int not null,
  project varchar(255),
  html mediumtext,
  last_updated datetime,
  primary key (datasource_id, project)
);

create table tig_project_discussions
(
  datasource_id int not null,
  project varchar(255),
  last_updated datetime,
  discussion varchar(255),
  description mediumtext,
  forumid int,
  last_comment datetime,
  primary key (datasource_id, project, discussion)
);

create table tig_messages
(
  datasource_id int not null,
  project varchar(255),
  forumid int,
  title varchar(255),
  link varchar(255),
  description mediumtext,
  pubDate datetime,
  guid varchar(255),
  creator varchar(255),
  postDate datetime,
  postDateStr varchar(255),
  primary key (project, forumid, guid)
);
