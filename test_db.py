import sqlite3

conn = sqlite3.connect("test.db")

c = conn.cursor()

c.execute("SELECT * FROM users")

items = c.fetchall()

for item in items:
    print(item[0] + "" + item[1])

conn.commit()

conn.close()