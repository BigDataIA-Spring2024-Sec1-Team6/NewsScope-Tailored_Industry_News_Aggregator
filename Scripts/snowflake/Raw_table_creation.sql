Create database RAW_NEWSFEED

create schema CNN
--use schema cnn

CREATE TABLE cnn_newsfeed (
    Headings VARCHAR(256),
    Links VARCHAR(512),
    Content TEXT,
    Industry VARCHAR(128),
    entry_date date
    
);


create schema CNBC
--use schema cnbc

CREATE TABLE cnbc_newsfeed (
    Headings VARCHAR(256),
    Links VARCHAR(512),
    Content TEXT,
    Industry VARCHAR(128),
    entry_date date
);

create schema SI
-- use schema SI

CREATE TABLE si_newsfeed (
    Headings VARCHAR(256),
    Links VARCHAR(512),
    Content TEXT,
    Industry VARCHAR(128),
    entry_date date
);


create schema WIRED
--use schema wired

CREATE TABLE wired_newsfeed (
    Headings VARCHAR(256),
    Links VARCHAR(512),
    Content TEXT,
    Industry VARCHAR(128),
    entry_date date
);
