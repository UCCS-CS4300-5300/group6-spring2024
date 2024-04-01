import sqlite3
from sqlite3 import Error
from django.db import connection

def delete_inactive_users():
  with connection.cursor() as cursor:
    the_sql = '''UPDATE users SET is_active = 'FALSE' WHERE last_login < 
    (datetime('now') - interval '7 days');'''
    cursor.execute(the_sql)
