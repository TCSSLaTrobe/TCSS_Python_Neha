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
    return render_template('admin_login.html')

if __name__ == '__main__':
    create_table()
    app.run(debug=True)

