import sqlite3

def query_lecturer_details():
    connection = sqlite3.connect("tcss.db")
    cursor = connection.cursor()

    cursor.execute('SELECT id, name FROM lecturers')
    lecturer_names = cursor.fetchall()

    cursor.execute('''SELECT lecturers.id, lecturers.name, subjects.code, subjects.name FROM lecturer_sme
                    JOIN lecturers
                    ON lecturers.id = lecturer_sme.lecturer_id
                    JOIN subjects
                    ON lecturer_sme.subject_id = subjects.id
                    ''')
    lecturer_expertise = cursor.fetchall()

    return lecturer_names, lecturer_expertise

def generate_lecturer_data():
    lecturer_data = query_lecturer_details()
    lecturers = []
    i = 0
    for lecturer in lecturer_data[0]:
        lecturers.append({
            "id": lecturer[0],
            "name": lecturer[1],
            "expertise": []})

        for pair in lecturer_data[1]:
            if pair[1] == lecturer[1]:
                lecturers[i]["expertise"].append(pair[2] + " - " + pair[3])
        i += 1
    return lecturers