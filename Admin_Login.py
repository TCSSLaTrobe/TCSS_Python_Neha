from flask import Flask, redirect, request, url_for, flash, render_template
import sqlite3
import string
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE = 'TCSS.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user(
            loginid VARCHAR(10) PRIMARY KEY,
            pass_word VARCHAR(18) NOT NULL,
            user_type VARCHAR(15)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lecturer(
            lect_name VARCHAR(10),
            subject_name VARCHAR(255),
            workload INTEGER
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def main_homepage():
    return render_template('main_homepage.html')

@app.route('/admin')
def admin_homepage():
    return render_template('admin_homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        if username == 'admin@123' and password == 'tcss':
            return redirect(url_for('admin_homepage'))
        else:
            flash("Invalid Credentials. Please Retry Logging In")
    return render_template('admin_login.html')

@app.route('/addlecturer_subject', methods=['GET', 'POST'])
def add_lecturer():
    if request.method == 'POST':
        lect_name = request.form['LecturerName']
        sub_name = request.form['subjectPrefix']
        workload = request.form['lecturerLoad']
        login_id = 'Lect' + lect_name[:4]
        password1 = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
        usertype = 'lecturer'
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO lecturer (lect_name, subject_name, workload)
            VALUES (?, ?, ?)
        """, (lect_name, sub_name, workload))
        
        cursor.execute("""
            INSERT INTO user (loginid, pass_word, user_type)
            VALUES (?, ?, ?)
        """, (login_id, password1, usertype))
        
        conn.commit()
        conn.close()
        
        flash('Lecturer Details Added Successfully')
        return redirect(url_for('admin_homepage'))
    
    return render_template('addlecturer_subject.html')

@app.route('/view_logindetails', methods=['GET'])
def view_logindetails():
    conn = get_db_connection()
    users = conn.execute('SELECT loginid, user_type, pass_word FROM user').fetchall()
    conn.close()
    return render_template('view_logindetails.html', users=users)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)


