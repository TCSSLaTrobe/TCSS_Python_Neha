# from flask import Flask, render_template, request, redirect, url_for, flash, session
# import sqlite3
# import string
# import random
#
# app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Keep this secret in a safe place in production
# DATABASE = 'TCSS.db'
#
# def get_db_connection():
#     conn = sqlite3.connect(DATABASE)
#     conn.row_factory = sqlite3.Row
#     return conn
#
# def create_table():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS user (
#             loginid VARCHAR(10) PRIMARY KEY,
#             pass_word VARCHAR(18) NOT NULL,
#             user_type VARCHAR(15)
#         )
#     """)
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS lecturer (
#             lect_name VARCHAR(100),
#             subject_name VARCHAR(255),
#             workload FLOAT
#             )
#     """)
#     conn.commit()
#     conn.close()
#
# @app.route('/')
# def main_homepage():
#     return render_template('main_homepage.html')
#
# @app.route('/admin')
# def admin_homepage():
#     if not session.get('logged_in'):
#         return redirect(url_for('admin_login'))
#     return render_template('admin_homepage.html')
#
# @app.route('/login', methods=['GET', 'POST'])
# def admin_login():
#     if request.method == 'POST':
#         username = request.form["username"]
#         password = request.form["password"]
#
#         if username == 'admin@123' and password == 'tcss':
#             session['logged_in'] = True
#             return redirect(url_for('admin_homepage'))
#         else:
#             flash("Invalid Credentials. Please retry logging in.")
#     return render_template('admin_login.html')
#
# @app.route('/addlecturer_subject', methods=['GET', 'POST'])
# def add_lecturer():
#     if not session.get('logged_in'):
#         return redirect(url_for('admin_login'))
#     if request.method == 'POST':
#         lect_name = request.form['lecturerName']
#         sub_name = request.form['subjectPrefix']
#         workload = float(request.form['lecturerLoad'])
#         print(f"Received data - Lecturer Name: {lect_name}, Subject: {sub_name}, Workload: {workload}")
#
#         login_id = 'Lect' + lect_name[:4]
#         password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
#         usertype = 'lecturer'
#
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         try:
#             cursor.execute("INSERT INTO user (loginid, pass_word, user_type) VALUES (?, ?, ?)", (login_id, password, usertype))
#             cursor.execute("INSERT INTO lecturer (lect_name, subject_name, workload) VALUES (?, ?, ?)", (lect_name, sub_name, workload))
#             conn.commit()
#             flash('Lecturer added successfully!')
#         except Exception as e:
#             flash(f"An error occurred: {str(e)}")
#         finally:
#             conn.close()
#         return redirect(url_for('admin_homepage'))
#     return render_template('addlecturer_subject.html')
#
# @app.route('/view_logindetails')
# def view_logindetails():
#     if not session.get('logged_in'):
#         return redirect(url_for('admin_login'))
#     conn = get_db_connection()
#     users = conn.execute('SELECT loginid, user_type, pass_word FROM user').fetchall()
#     conn.close()
#     return render_template('view_logindetails.html', users=users)
#
# @app.route('/view_lecturer')
# def view_lecturer():
#     if not session.get('logged_in'):
#         return redirect(url_for('admin_login'))
#     conn = get_db_connection()
#     lecturers = conn.execute('SELECT * FROM lecturer').fetchall()
#     conn.close()
#     return render_template('view_lecturer.html', lecturers=lecturers)
#
# @app.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     return redirect(url_for('main_homepage'))
#
# if __name__ == '__main__':
#     create_table()
#     app.run(debug=True)
