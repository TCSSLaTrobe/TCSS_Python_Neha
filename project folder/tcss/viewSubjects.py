import sqlite3

def generate_subject_data():
    connection = sqlite3.connect("tcss.db")
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM subjects')
    subject_data = cursor.fetchall()
    subjects = []
    i = 0
    for subject in subject_data:
        subjects.append({
            "id": subject[0],
            "code": subject[1],
            "name": subject[2]
        })

    return subjects
