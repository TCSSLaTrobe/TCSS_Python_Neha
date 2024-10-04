import sqlite3

from sqlalchemy.engine import connection_memoize


def generate_instance_dates():
    connection  = sqlite3.connect('tcss.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id, subject_id, start_id
        FROM instances;
    ''')
    data = cursor.fetchall()
    connection.close()

    instances = {}

    for instance_id, subject_id, start_id in data:
        if subject_id not in instances:
            instances[subject_id] = []
        instances[subject_id].append(instance_id)

    return instances

def generate_calendar_dates():
    connection = sqlite3.connect('tcss.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT calendar.year, calendar.month, calendar.month_name
        FROM instances
        JOIN calendar 
        ON instances.start_id = calendar.id
        GROUP BY instances.start_id;
        ''')
    data = cursor.fetchall()
    connection.close()

    dates = {}

    for year,month, month_name in data:
        if year not in dates:
            dates[year] = {}
        dates[year][month] = month_name[:3].upper()
    return dates

def generate_subject_data():
    connection = sqlite3.connect('tcss.db')
    cursor = connection.cursor()
    cursor.execute('''
           SELECT id, code, name
            FROM subjects;
       ''')
    data = cursor.fetchall()
    connection.close()

    subjects = []

    for item in data:
        subject = {"id": item[0], "code": item[1], "name": item[2]}
        subjects.append(subject)

    return subjects

def generate_row_data():
    connection = sqlite3.connect('tcss.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT subjects.id, subjects.code, subjects.name, calendar.year, calendar.month
        FROM subjects
        JOIN instances
        ON subjects.id = instances.subject_id
        JOIN calendar
        ON calendar.id = instances.start_id
          ''')
    data = cursor.fetchall()
    connection.close()

    rows = []
    subject_data = {}

    for subject_id, subject_code, subject_name, year, month in data:
        if subject_id not in subject_data:
            subject_data[subject_id] = {
                "code": subject_code,
                "name": subject_name,
                "start_dates": {}
            }

        if year not in subject_data[subject_id]["start_dates"]:
            subject_data[subject_id]["start_dates"][year] = []

        subject_data[subject_id]["start_dates"][year].append(month)

    for subject_id, subject_info in subject_data.items():
        rows.append({
            "id": subject_id,
            "code": subject_info["code"],
            "name": subject_info["name"],
            "start_dates": subject_info["start_dates"]
        })

    return rows

def generate_instance_ids():
    connection = sqlite3.connect('tcss.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT instances.id
        FROM instances
        JOIN subjects
        ON subjects.id = instances.subject_id
        ORDER BY subjects.id
    ''')
    data = cursor.fetchall()

    instance_ids = [x[0] for x in data]

    return instance_ids

def generate_assigned_lecturers():
    connection = sqlite3.connect('tcss.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id, lecturer_id, assistant_id
        FROM instances; 
        ''')
    data = cursor.fetchall()

    assigned_lecturers = {}
    for instance_id, lecturer_id, assistant_id in data:
        assigned_lecturers[instance_id] = {
            "lecturer": lecturer_id,
            "assistant": assistant_id
        }

    return assigned_lecturers

