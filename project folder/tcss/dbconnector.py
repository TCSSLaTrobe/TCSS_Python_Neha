import sqlite3

db = "tcss.db"
connection = sqlite3.connect(db)
cursor = connection.cursor()

cursor.execute("SELECT * FROM instances")
results = cursor.fetchall()
for result in results:
    print(result)

connection.close()