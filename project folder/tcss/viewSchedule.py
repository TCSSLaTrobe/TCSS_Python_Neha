from flask import Flask, render_template
import sqlite3
import os

def generate_schedule(user_id):
    connection = sqlite3.connect('tcss.db')
    cursor = connection.cursor()

    cursor.execute('''
        SELECT lecturers.name, subjects.name, subjects.code, calendar.full_date, instances.student_count, instances.assistant_id
        FROM calendar
        JOIN instances ON calendar.id = instances.start_id
        JOIN subjects ON subjects.id = instances.subject_id
        JOIN lecturers ON lecturers.id = instances.lecturer_id
        JOIN user ON lecturers.user_id = user.id
        WHERE user.id = ?;
    ''',(user_id,))
    schedule_data = cursor.fetchall()

    schedule = []

    if schedule_data:
        lecturer_name = schedule_data[0][0]

        for row in schedule_data:
            instance = {
                "name": row[1],
                "code": row[2],
                "start_date": row[3],
                "student_count": row[4],
                "assistant": row[5]
            }
            schedule.append(instance)

    return lecturer_name, schedule



