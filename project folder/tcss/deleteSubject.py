import sqlite3

def delete_subject(subject_id):
    connection = sqlite3.connect('tcss.db')
    cursor = connection.cursor()

    cursor.execute('''
        DELETE FROM instances
        WHERE subject_id = ?
    ''', (subject_id,))

    # NEED TO UPDATE INSTANCES/SCHEDULE ONCE DELETED
    cursor.execute('''
        DELETE FROM lecturer_sme 
        WHERE subject_id = ?
    ''', (subject_id,))

    cursor.execute('''
        DELETE FROM subjects
        WHERE id = ?
    ''', (subject_id,))

    print("deleted")

    connection.commit()