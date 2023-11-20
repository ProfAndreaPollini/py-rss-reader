import sqlite3 as sq

# create rss.db
conn = sq.connect('rss.db')
c = conn.cursor()

# create table from db.sql
with open('db.sql', 'r') as f:
    sql = f.read()
c.executescript(sql)


c.close()