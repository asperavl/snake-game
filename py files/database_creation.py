#Code to create the database snake to house scores

import time

import mysql.connector as my

passkey = input("Enter Password for root ")

con = my.connect(host='localhost', user='root', password=passkey)

cur=con.cursor()

cur.execute('create database snake')

print("Database created successfully!")

cur.execute('use snake')

cur.execute('create table snake_scores(Name varchar(20), Score int, Date_of_Score date)')

print("Table create successfully!")

print("This window will auto close in 5 seconds")

con.commit()

time.sleep(5)

con.close()

