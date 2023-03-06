
drop database if exists database_1;
drop database if exists database_2;
drop database if exists database_3;

create database database_1;
create database database_2;
create database database_3;

use database_1;
create table table_1 (id int primary key,column_1 int);

use database_2;
create table table_1 (id int primary key,column_1 int);

use database_3;
create table table_1 (id int primary key,column_1 int);

use database_1;
insert into table_1 values (1,1);
insert into table_1 values (2,2);
insert into table_1 values (3,3);
insert into table_1 values (4,4);
insert into table_1 values (5,5);
insert into table_1 values (6,6);
insert into table_1 values (7,7);
insert into table_1 values (8,8);
insert into table_1 values (9,9);
insert into table_1 values (10,10);
insert into table_1 values (11,10);

use database_2;
insert into table_1 values (1,11);
insert into table_1 values (2,12);
insert into table_1 values (3,13);
insert into table_1 values (4,14);
insert into table_1 values (5,15);
insert into table_1 values (6,16);
insert into table_1 values (7,17);
insert into table_1 values (8,18);
insert into table_1 values (9,19);
insert into table_1 values (10,20);
insert into table_1 values (11,20);

use database_3;
insert into table_1 values (1,21);
insert into table_1 values (2,22);
insert into table_1 values (3,23);
insert into table_1 values (4,24);
insert into table_1 values (5,25);
insert into table_1 values (6,26);
insert into table_1 values (7,27);
insert into table_1 values (8,28);
insert into table_1 values (9,29);
insert into table_1 values (10,30);
insert into table_1 values (11,30);