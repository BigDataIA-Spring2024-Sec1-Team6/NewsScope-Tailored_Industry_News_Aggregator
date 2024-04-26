Create database USER_DATABASE
Create Schema USER
  

create or replace TABLE USER_DATABASE.USER.USERS_CRED (
	USERID NUMBER(38,0) NOT NULL autoincrement start 1 increment 1 noorder,
	USERNAME VARCHAR(255),
	PASSWORD VARCHAR(255),
	unique (USERNAME),
	primary key (USERID)
);
