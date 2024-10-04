import sqlite3

def generate_lecturer_data(lecturer_id):
    connection = sqlite3.connect("tcss.db")
    cursor = connection.cursor()

    cursor.execute('''
        SELECT lecturers.id, lecturers.name, lecturers.load, subjects.code, subjects.name FROM lecturer_sme
        JOIN lecturers
        ON lecturers.id = lecturer_sme.lecturer_id
        JOIN subjects
        ON lecturer_sme.subject_id = subjects.id
        WHERE lecturers.id = ?
    ''',(lecturer_id,))
    lecturer_data = cursor.fetchall()

    lecturer = {
        "id": lecturer_id,
        "name": lecturer_data[0][1],
        "load": lecturer_data[0][2],
        "expertise": []
    }

    for lecturer_tuple in lecturer_data:
        lecturer["expertise"].append(lecturer_tuple[3] + "-" + lecturer_tuple[4])

    return lecturer

def generate_subject_data():
    connection = sqlite3.connect("tcss.db")
    cursor = connection.cursor()
    # Get subject data for SME checkboxes
    cursor.execute('''
        SELECT code, name FROM subjects 
    ''')
    subject_data = cursor.fetchall()
    return subject_data

def generate_sme(lecturer_id):
    connection = sqlite3.connect("tcss.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Get subject data for SME checkboxes
    subjects = generate_subject_data()
    cursor.execute('''
            SELECT subject_id 
            FROM lecturer_sme 
            WHERE lecturer_id =  
        ''' + lecturer_id)
    rows = cursor.fetchall()
    lecturer_sme = [row['subject_id'] for row in rows]

    all_sme = [0] * len(subjects)
    for subject_id in lecturer_sme:
        all_sme[subject_id - 1] = 1

    return all_sme

def update_lecturer(lect_id, name, workload, sme):
    connection = sqlite3.connect("tcss.db")
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE lecturers
        SET name = ?, [load] = ?
        WHERE id = ?
    ''', (name, workload, lect_id))

    cursor.execute('''
        DELETE FROM lecturer_sme WHERE lecturer_id = ?
    ''', (lect_id,))

    for subject_id in sme:
        cursor.execute('''
            INSERT INTO lecturer_sme (lecturer_id, subject_id)
            VALUES(?,?)
        ''', (lect_id, subject_id))

    connection.commit()

