import sqlite3

connection = sqlite3.connect('tcss.db')

cursor = connection.cursor()

command2 = "INSERT INTO test_table VALUES (1,'Darragh'),(2,'Neha'),(3,'Dee'),(4,'Alecia')"
command3 = "SELECT * FROM test_table"

cursor.execute(command2)
connection.commit() #insert must be commited

cursor.execute(command3)
result = cursor.fetchall()
print(result)