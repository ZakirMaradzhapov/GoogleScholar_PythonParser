import sqlite3

conn = sqlite3.connect("database.db")
sql = "CREATE TABLE citations (TITLE TEXT, AUTHORS TEXT, JOURNAL TEXT, CITED_BY TEXT, YEAR TEXT, LINK TEXT)"
cursor = conn.cursor()
cursor.execute(sql)
conn.close()