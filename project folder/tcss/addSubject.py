import sqlite3

def add_subject(code,name,instance_count):
    connection = sqlite3.connect('tcss.db')
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO subjects (code,name,instance_count)
        VALUES (?,?,?)
    ''',(code,name,instance_count))

    connection.commit()