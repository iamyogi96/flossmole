create table lpd_projects
(
  datasource_id int not null,
  name varchar(255) not null,
  display_name varchar(255),
  web_link varchar(255),
  active bool,
  bug_reported_acknowledgement mediumtext,
  bug_reporting_guidelines mediumtext,
  commercial_subscription_is_due bool,
  date_created datetime,
  date_next_suggest_packaging datetime,
  description mediumtext,
  download_url varchar(255),
  freshmeat_project varchar(255),
  homepage_url varchar(255),
  license_info mediumtext,
  qualifies_for_free_hosting bool,
  screenshots_url varchar(255),
  sourceforge_project varchar(255),
  summary mediumtext,
  title varchar(255),
  wiki_url varchar(255),
  bug_supervisor varchar(255),
  bug_tracker varchar(255),
  development_focus varchar(255),
  driver varchar(255),
  owner varchar(255),
  project_group varchar(255),
  registrant varchar(255),
  security_contact varchar(255),
  translation_focus varchar(255),
  last_updated datetime,
  primary key (datasource_id,name)
);

create table lpd_licenses
(
  datasource_id int not null,
  name varchar(255) not null,
  license varchar(255) not null,
  last_updated datetime,
  primary key (datasource_id,name,license)
);

create table lpd_official_bug_tags
(
  datasource_id int not null,
  name varchar(255) not null,
  official_bug_tag varchar(255) not null,
  last_updated datetime,
  primary key (datasource_id,name,official_bug_tag)
);

create table lpd_programming_languages
(
  datasource_id int not null,
  name varchar(255) not null,
  programming_language varchar(255) not null,
  last_updated datetime,
  primary key (datasource_id,name,programming_language)
);

create table lpd_milestones
(
  datasource_id int not null,
  name varchar(255) not null,
  project_name varchar(255) not null,
  title varchar(255),
  is_active bool,
  summary mediumtext,
  code_name varchar(255),
  date_targeted datetime,
  last_updated datetime,
  primary key (datasource_id,name,project_name)
);

create table lpd_releases
(
  datasource_id int not null,
  display_name varchar(255) not null,
  title varchar(255),
  milestone varchar(255),
  version varchar(255),
  project_name varchar(255) not null,
  release_notes mediumtext,
  changelog mediumtext,
  date_created datetime,
  date_released datetime,
  last_updated datetime,
  primary key (datasource_id,display_name,project_name)
);

create table lpd_series
(
  datasource_id int not null,
  display_name varchar(255),
  title varchar(255),
  status varchar(255),
  name varchar(255) not null,
  project_name varchar(255) not null,
  bug_reported_acknowledgement mediumtext,
  bug_reporting_guidelines mediumtext,
  date_created datetime,
  active bool,
  summary mediumtext,
  last_updated datetime,
  primary key(name, project_name, datasource_id)
);
