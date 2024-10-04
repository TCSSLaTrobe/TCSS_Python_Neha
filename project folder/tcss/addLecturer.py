import sqlite3

def add_lecturer(name, workload, sme):
    connection = sqlite3.connect('tcss.db')
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO lecturers (name, load)
        VALUES (?,?)
    ''',(name,workload))

    lecturer_id = cursor.execute("SELECT MAX(id) FROM lecturers").fetchone()[0]

    for subject_id in sme:
        cursor.execute('''
            INSERT INTO lecturer_sme (lecturer_id, subject_id)
            VALUES (?,?)
        ''',(lecturer_id, subject_id))

    connection.commit()