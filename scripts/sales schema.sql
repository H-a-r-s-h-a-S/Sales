drop database if exists sales;
create database sales;

use sales;

drop table if exists rate ;
create table rate (
  name char(100),
  price decimal(10,2)
) engine=InnoDB;

drop table if exists customers ;
create table customers (
  id char(36), 
  name char(100), 
  phone char(30), 
  email char(100),
  primary key (id)
) engine=InnoDB;


drop table if exists transactions ;
create table transactions (
  saledate date,
  transactionid char(36),
  customer_id char(36),
  item char(100),
  rate decimal(10,2),
  quantity decimal(10,2),
  total decimal(10,2),
  primary key (transactionid),
  foreign key (customer_id) references customers(id)
    on update cascade 
    on delete cascade
) engine=InnoDB;