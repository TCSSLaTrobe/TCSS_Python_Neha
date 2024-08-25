from flask import Flask, redirect,request,url_for,flash
import sqlite3
import string
import random
app=Flask(__name__)
app.secret_key='your_secret_key'
DATABASE='TCSS.db'

def get_db_connection():
    conn=sqlite3.connect(DATABASE)#connect
    conn.row_factory=sqlite3.Row
    return conn
def create_table():
    conn=get_db_connection()
    cursor=conn.cursor()
    cursor.execute(" CREATE TABLE IF NOT EXISTS user(loginid varchar (10), "
                   "PRIMARY KEY, pass_word varchar(18) NOT NULL, user_type varchar(15)")

    cursor.execute(" CREATE TABLE IF NOT EXISTS lecturer(lect_name varchar (10), "
                   "Subject_name (255), workload integer) ")
    conn.commit()
    conn.close()
