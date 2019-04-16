import sqlite3
import json

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (mid INTEGER PRIMARY KEY,name text, imdb_score real, _99popularity real,director text, genre text)"
cursor.execute(create_table)

traffic = json.load(open('imdb.json'))

columns = ['name','imdb_score','_99popularity', 'director', 'genre']
for data in traffic:
    keys = tuple(data[c] for c in columns)
    cursor.execute("insert into items values(NULL,?,?,?,?,?)", keys)

connection.commit()
connection.close()

