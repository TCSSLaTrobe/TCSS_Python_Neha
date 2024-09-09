from enum import unique
import manageLecturers
from flask import Flask, render_template, request, url_for, abort
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
    email = db.Column(db.String, unique=True)
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
        compare = User.query.filter_by(email = request.form['email']).all()
        for user in compare:
            if request.form['email'] == user.email and request.form['password'] == user.password and user.enabled == True:
                login_user(user)
                return redirect('/dashboard')
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
    print(account_level)
    return render_template('dashboard.html', account_level=account_level)

@app.route('/view_lecturers')
def view_lecturers():
    lecturer_data = manageLecturers.generate_lecturer_data()
    return render_template('fulltimelecturers.html', lecturer_data=lecturer_data)

if __name__ == '__main__':
    app.run()