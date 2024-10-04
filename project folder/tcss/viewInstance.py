import sqlite3

def generate_instance_data(instance_id):
    connection = sqlite3.connect('tcss.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT subjects.id,subjects.code, subjects.name, instances.student_count, calendar.month_name, calendar.year
        FROM instances
        JOIN subjects ON subjects.id = instances.subject_id
        JOIN calendar ON calendar.id = instances.start_id
        WHERE instances.id = ?;
    ''',(instance_id,))

    data = cursor.fetchall()
    connection.close()

    instance_data = {}
    for item in data:
        instance_data = {
            "id": item[0],
            "code":item[1],
            "name":item[2],
            "student_count":item[3],
            "start_month":item[4],
            "start_year":item[5]}

    possible_lectures = generate_possible_lecturers(instance_data["id"])
    return instance_data, possible_lectures

def generate_assigned_lecturers(instance_id):
    connection = sqlite3.connect('tcss.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT lecturers.name
        FROM lecturers 
        JOIN instances on lecturers.id = instances.lecturer_id
        WHERE instances.id = ?;
    ''',(instance_id,))
    current_lecturer = cursor.fetchone()

    cursor.execute('''
        SELECT lecturers.name
        FROM lecturers 
        JOIN instances on lecturers.id = instances.assistant_id
        WHERE instances.id = ?;
    ''', (instance_id,))
    current_assistant = cursor.fetchone()

    connection.close()

    assigned_lecturers = {
        "lecturer": current_lecturer[0] if current_lecturer else None,
        "assistant": current_assistant[0] if current_assistant else None
       }

    return assigned_lecturers

def generate_possible_lecturers(subject_id):
    connection = sqlite3.connect('tcss.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT lecturers.id, lecturers.name, lecturers.workload
        FROM lecturers
        JOIN lecturer_sme ON lecturers.id = lecturer_sme.lecturer_id
        WHERE lecturers.id IN ( SELECT lecturer_sme.lecturer_id
                                FROM lecturer_sme
                                WHERE lecturer_sme.subject_id = ?)
        GROUP BY lecturers.id;
        ''', (subject_id,))
    data = cursor.fetchall()

    connection.close()

    possible_lecturers = []
    for item in data:
        possible_lecturers.append({
            "id":item[0],
            "name":item[1],
            "workload":item[2]
        })
    return possible_lecturers

def generate_create_new_data(new_instance_data):
    subject_id = new_instance_data[0]
    year = new_instance_data[1]
    month = new_instance_data[2]

    connection = sqlite3.connect('tcss.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT subjects.id, subjects.code, subjects.name
        FROM subjects
        WHERE subjects.id = ?
            ''', (subject_id,))
    data = cursor.fetchone()

    subject_data = {
        "id": data[0],
        "code": data[1],
        "name": data[2]
    }

    cursor.execute('''
        SELECT DISTINCT month_name
        FROM calendar
        WHERE month = ?
    ''',(month,))
    month_name = cursor.fetchone()

    instance_date = {
        "month":month_name[0],
        "year": year
    }

    possible_lecturers = generate_possible_lecturers(subject_id)

    connection.close()

    return subject_data, instance_date, possible_lecturers
