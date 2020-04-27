# Remote SQL Tool
# Note: may not work with newer versions of Python

import MySQLdb
import prettytable
from prettytable import from_db_cursor

host = raw_input('Enter host name: ') #remote host (ex. localhost)
user = raw_input('Enter username: ') #username
pw = raw_input('Enter password: ') #password
database = raw_input('Enter database name: ') #name of database

db = MySQLdb.connect(host, user, pw, database) #connect to database and run query

# create Cursor object
cursor = db.cursor() 
col = raw_input('Enter column name: ')
table = raw_input('Enter table name: ')

#columns = map(col, col.split())
cursor.execute("SELECT " + col + " FROM " + database + "." + table + " ")
pt = from_db_cursor(cursor)
print(pt)

cursor.close()