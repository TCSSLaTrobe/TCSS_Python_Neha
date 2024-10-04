from enum import unique
from statistics import pstdev

import viewLecturers, editLecturer, addLecturer, deleteLecturer, viewSubjects, editSubject, addSubject, deleteSubject, viewSchedule, manageSchedule, viewInstance
from flask import Flask, render_template, request, url_for, abort, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tcss.db"
app.config['SECRET_KEY'] = 'MY_SECRET'
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    account_level = db.Column(db.Integer())
    enabled = db.Column(db.Boolean)

    def get_id(self):
        return self.id

app.secret_key = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login 1.html'
@login_manager.user_loader
def load_user(email):
    db.engine.dispose()
    db.engine.connect()
    return User.query.get(email)

@app.route('/login 1', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            return redirect('/home')
        else:
            msg="Incorrect Credentials"
            return render_template('login 1.html', msg=msg)
    return render_template('login 1.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login 1.html')

@app.route('/')
@app.route('/home')
def home_page():
    if current_user.is_authenticated:
        return redirect('/dashboard')
    else:
        return render_template('login 1.html')

@app.route('/dashboard')
def dashboard():
    account_level = current_user.account_level
    return render_template('dashboard.html', account_level=account_level)

# MANAGE LECTURERS (VIEW/EDIT/DELETE/ADD)
@app.route('/view_lecturers')
def view_lecturers():
    lecturer_data = viewLecturers.generate_lecturer_data()
    return render_template('fulltimelecturers.html', lecturer_data=lecturer_data)

@app.route('/edit_lecturer', methods=['GET','POST'])
def edit_lecturer():
    if request.method == 'POST':
        lecturer_id = request.form['lecturer_id']
        lecturer = editLecturer.generate_lecturer_data(lecturer_id)
        subjects = editLecturer.generate_subject_data()
        sme = editLecturer.generate_sme(lecturer_id)

        return render_template('edit_lecturer.html',lecturer_id=lecturer_id,lecturer=lecturer, subjects=subjects, sme=sme)

@app.route('/update_lecturer', methods=['GET','POST'])
def update_lecturer():
    if request.method == 'POST':
        lect_id = request.form['lecturer_id']
        name = request.form['lecturer_name']
        workload = request.form['lecturer_workload']
        sme = request.form.getlist('sme')

        editLecturer.update_lecturer(lect_id, name, workload, sme)

        return redirect('/view_lecturers')

@app.route('/delete_lecturer', methods=['GET','POST'])
def delete_lecturer():
    if request.method == 'POST':
        lecturer_id = request.form['lecturer_id']

        lecturer = editLecturer.generate_lecturer_data(lecturer_id)

        return render_template('/delete_lecturer.html', lecturer=lecturer)

@app.route('/confirm_delete_lecturer', methods=['GET','POST'])
def confirm_delete_lecturer():
    if request.method == 'POST':
        lecturer_id = request.form['lecturer_id']

        deleteLecturer.delete_lecturer(lecturer_id)

        return redirect('/view_lecturers')

@app.route('/add_lecturer', methods=['GET','POST'])
def add_lecturer():
    if request.method == 'POST':
        name = request.form['lecturer_name']
        workload = request.form['lecturer_workload']
        sme = request.form.getlist('sme')

        addLecturer.add_lecturer(name, workload, sme)

        return redirect('/view_lecturers')

    subjects = editLecturer.generate_subject_data()
    return render_template('/add_lecturer.html', subjects=subjects)

# MANAGE SUBJECTS (VIEW/EDIT/DELETE/ADD)
@app.route('/view_subjects')
def view_subjects():
    subjects = viewSubjects.generate_subject_data()
    return render_template('/view_subjects.html', subjects=subjects)

@app.route('/edit_subject', methods=['GET','POST'])
def edit_subject():
    if request.method == 'POST':
        subject_id = request.form['subject_id']
        subject = editSubject.generate_subject_data(subject_id)

        return render_template('edit_subject.html', subject=subject)

@app.route('/update_subject', methods=['GET','POST'])
def update_subject():
    if request.method == 'POST':
        subject_id = request.form['subject_id']
        code = request.form['subject_code']
        name = request.form['subject_name']

        editSubject.update_subject(subject_id,code,name)
        return redirect('/view_subjects')

@app.route('/add_subject', methods=['GET','POST'])
def add_subject():
    if request.method == 'POST':
        code = request.form['subject_code']
        name = request.form['subject_name']
        instance_count = 0

        addSubject.add_subject(code,name,instance_count)
        return redirect('/view_subjects')

    return render_template('/add_subject.html')

@app.route('/delete_subject', methods=['GET','POST'])
def delete_subject():
    if request.method == 'POST':
        subject_id = request.form['subject_id']
        subject = editSubject.generate_subject_data(subject_id)
        return render_template('/delete_subject.html', subject=subject)

@app.route('/confirm_delete_subject', methods=['GET','POST'])
def confirm_delete_subject():
    if request.method == 'POST':
        subject_id = request.form['subject_id']
        deleteSubject.delete_subject(subject_id)
        return redirect('/view_subjects')

@app.route('/view_schedule')
def view_schedule():
    lecturer_name, schedule= viewSchedule.generate_schedule(current_user.id)
    return render_template('/schedule.html', lecturer_name=lecturer_name, schedule=schedule)

@app.route('/manage_schedule')
def manage_schedule():
    instances = manageSchedule.generate_instance_dates()
    calendar_dates = manageSchedule.generate_calendar_dates()
    subjects = manageSchedule.generate_subject_data()
    rows = manageSchedule.generate_row_data()
    print(rows)
    print(calendar_dates)
    instance_ids = manageSchedule.generate_instance_ids()
    assigned_lecturers = manageSchedule.generate_assigned_lecturers()
    return render_template('/manage_schedule.html', instances=instances,
                           calendar_dates=calendar_dates, subjects=subjects, rows=rows,instance_ids=instance_ids,
                           assigned_lecturers=assigned_lecturers)

@app.route('/view_instance', methods=['GET','POST'])
def view_instance():
    if request.method == 'POST':
        instance_id = request.form['instance_id']
        instance_data, possible_lecturers = viewInstance.generate_instance_data(instance_id)
        assigned_staff = viewInstance.generate_assigned_lecturers(instance_id)
        return render_template('/view_instance.html',instance_data=instance_data,
                               assigned_staff=assigned_staff, possible_lecturers=possible_lecturers)

@app.route('/update_instance', methods=['GET','POST'])
def update_instance():
    if request.method == 'POST':
        lecturer_id = request.form['lecturer_id']
        assistant_id = request.form['assistant_id']


@app.route('/create_instance', methods=['GET', 'POST'])
def create_instance():
    if request.method == 'POST':
        new_instance_data = request.form['create_ids'].split(",")
        new_instance_data = [int(num) for num in new_instance_data]
        subject_data, instance_date, possible_lecturers = viewInstance.generate_create_new_data(new_instance_data)
        return render_template('create_instance.html', subject_data=subject_data,
                               instance_date=instance_date, possible_lecturers=possible_lecturers)


# def create_user(email, password, account_level):
#     new_user = User(email=email, password=password, account_level=account_level)
#     db.session.add(new_user)
#     db.session.commit()
#     return

if __name__ == '__main__':
    app.run()