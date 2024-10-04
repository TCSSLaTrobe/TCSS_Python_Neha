import sqlite3

def delete_lecturer(lecturer_id):
    connection = sqlite3.connect('tcss.db')
    cursor = connection.cursor()

    cursor.execute('''
        UPDATE instances
        SET lecturer_id = NULL
        WHERE lecturer_id = ?
    ''', (lecturer_id,))

    cursor.execute('''
        UPDATE instances
        SET assistant_id = NULL
        WHERE assistant_id = ?
    ''', (lecturer_id,))

    cursor.execute('''
        DELETE FROM lecturer_sme
        WHERE lecturer_id = ?    
    ''', (lecturer_id,))

    cursor.execute('''
        DELETE FROM lecturers
        WHERE id = ?
    ''', (lecturer_id,))

    connection.commit()