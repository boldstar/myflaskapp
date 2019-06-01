from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory, session, logging
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import Required, Length
from passlib.hash import sha256_crypt
from functools import wraps
from forms import *
import os
from config import app, mysql

# @template Register
# @desc Register route with register form
# @job Grab form values | Hash password | Create new user record | Redirect to documents page
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        # set mysql cursor
        cur = mysql.connection.cursor()
        # insert statement for data to be commited
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
        # commit to db
        mysql.connection.commit()
        # close connection
        cur.close()
        flash('You are now registered, please login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# @template Login
# @desc Login route with login form
# @job Find user | Verify credentials | Create session
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        passsword_candidate = form.password.data
        # create database cursor
        cur = mysql.connection.cursor()
        #get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        if result > 0:
            # get the stored hash of the password
            data = cur.fetchone()
            password = data['password']
            #compare passwords
            if sha256_crypt.verify(passsword_candidate, password):
                #session variables
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('upload_file'))
            else:
                error = 'Incorrect password'
                return render_template('login.html', form=form, error=error)
            cur.close()
        else:
            error = 'User not found'
            return render_template('login.html', form=form, error=error)
    return render_template('login.html', form=form)

# @desc Logout route
# @job Destroy session | Redirect to login page | Flash message
def logout():
    session.clear()
    flash('You have logged out')
    return redirect(url_for('log_in'))