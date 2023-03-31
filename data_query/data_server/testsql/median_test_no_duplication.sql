
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

use database_2;
insert into table_1 values (1,9);
insert into table_1 values (2,10);
insert into table_1 values (3,11);
insert into table_1 values (4,12);

use database_3;
insert into table_1 values (1,13);
insert into table_1 values (2,14);
insert into table_1 values (3,15);
insert into table_1 values (4,16);
insert into table_1 values (5,17);
insert into table_1 values (6,18);
insert into table_1 values (7,19);


use database_1;
select * from table_1;



select COUNT(*) from database_1.table_1 GROUP BY column_1;

SELECT COUNT(*) AS i FROM database_1.table_1 GROUP BY id ORDER BY i DESC;