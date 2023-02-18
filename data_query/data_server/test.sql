drop database database_1;
drop database database_2;
drop database database_3;

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
insert into table_1 values (4,2);
insert into table_1 values (5,3);
insert into table_1 values (6,2);
insert into table_1 values (7,3);
insert into table_1 values (8,1);

use database_2;
insert into table_1 values (1,1);
insert into table_1 values (2,2);
insert into table_1 values (3,3);
insert into table_1 values (4,1);

use database_3;
insert into table_1 values (1,1);
insert into table_1 values (2,2);
insert into table_1 values (3,2);
insert into table_1 values (4,2);
insert into table_1 values (5,2);
insert into table_1 values (6,3);
insert into table_1 values (7,1);


use database_1;
select * from table_1;



select COUNT(*) from database_1.table_1 GROUP BY column_1;

SELECT COUNT(*) AS i FROM database_1.table_1 GROUP BY id ORDER BY i DESC;