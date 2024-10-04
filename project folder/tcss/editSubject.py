import sqlite3

def generate_subject_data(subject_id):
    connection = sqlite3.connect('tcss.db')
    cursor = connection.cursor()

    cursor.execute('''
        SELECT *
        FROM subjects
        WHERE id = ?
    ''', (subject_id,))

    subject_data = cursor.fetchall()
    subject_data = subject_data[0]
    subject = {
        "id": subject_data[0],
        "code": subject_data[1],
        "name": subject_data[2],
        "instances": subject_data[3]
    }

    return subject

def update_subject(subject_id,code,name):
    connection = sqlite3.connect('tcss.db')
    cursor = connection.cursor()

    cursor.execute('''
        UPDATE subjects
        SET code = ?, name = ?
        WHERE id = ? 
    ''', (code, name, subject_id))

    connection.commit()
