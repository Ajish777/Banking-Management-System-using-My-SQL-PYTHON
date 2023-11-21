
# Banking-Management-System-using-My-SQL-PYTHON
About

In this project, we have created a Virtual Bank (COLONY BANK OF INDIA) using Python and MySQL. Data entered by the user are stored in the MYSQL database in tabular form. Here We have done a CRUD Operation. The Best Part of this code is that it is 100 % user-friendly because of the excess use of exceptional handling.

This project is designed for The Bank Staff to keep a record of their customers. Only authorized Users can have the accessibility to the program. Users after Logging in have the support to display all records, and modify them accordingly. If someone does not have a Login Id or password he/she could make a new ID. Further, it can also check the overall record of a local customer or full details of a single a/c as per transactions, create a new record for a new customer, Update an old customer record, Delete a record of a customer and Update the Loans of the customer. Python is used as Front End and MySQL is used as Back End.

*Requirement

Python Latest Version

Visual Code

Mysql

Python My SQL Converter: Most Important

*Module Used in Python Code

datetime

mysql.connector

*About Mysql Code

The database used here is Hubnet

address = local

user=root

password=12345678

UserName is the Primary Key in Bank Table and UserName1 is the Foreign Key in Transaction Table.

Suggestion: Run Bank-Project.py Code in IDLE.

Before Running This Code in Your System Make Sure you have created the bank and transactions Table.

*My Sql Code for Creating Table Bank create table bank(name varchar(30), UserName varchar(30),password tinytext , Date_of_birth date, address varchar(40) ,Mobile_Number varchar(30) ,Aadhar_no varchar(30), Balance int);

*My Sql code for creating Table Transaction: create table Transaction(credited int , debited int , username1 varchar(20), foreign key(username1) references bank(username));

Some Glimpse of this project are shown below

