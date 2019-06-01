from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory, session, logging
from werkzeug.utils import secure_filename
from files import Files
from functools import wraps
import os
import re
from os import listdir
from os import path, walk
from os.path import isfile, join
from config import app, mysql, extensions, uploads
from auth import register, login, logout

# @files in the uploads folder
Files = Files()

# Check if user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        #if logged in do nothing
        if 'logged_in' in session:
            return f(*args, **kwargs)
        # else return to login page
        else:
            flash('Please login', 'error')
            return redirect(url_for('log_in'))
    return wrap

# @template Home
# @desc Return home route
@app.route('/')
def index():
    return render_template('home.html')

# @template About
# @desc Return about router
@app.route('/about')
def about():
    return render_template('about.html')

# @template Register
# @desc Register route with register form
@app.route('/register', methods=['GET', 'POST'])
def reg():
    return register()


# @template Login
# @desc Login route with login form
@app.route('/login', methods=['GET', 'POST'])
def log_in():
    return login()
    

# @desc Check if given file extenstion is allowed
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in extensions

# @template Index
# @desc Main app route with preview of uploaded documents and method for uploading documents
@app.route('/documents', methods=['GET', 'POST'])
@is_logged_in
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            files = Files
            files.append(filename)
            return render_template('index.html', files = files)
    return render_template('index.html', files = Files)

@app.route('/delete/<filename>')
def delete(filename):
    if filename:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(filepath)
        os.remove(filepath)
        files = Files
        files.remove(filename)
        return render_template('index.html', files = files)

# @desc Route for viewing uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = request.form
    if request.method == 'POST' and form:
        key = request.form['search']
        files = Files
        if len(files) > 0:
            match = []
            for file in files:
                if re.search(key, file):
                    match.append(file)
            if len(match) > 0:    
                return render_template('search.html', files=match)
            else:
                flash('Sorry no dox found, please try again')
                return redirect(request.url)
        else:
            flash('Sorry no dox found, please try again')
            return redirect(request.url)    
    return render_template('search.html') 
                             

@app.route('/logout')
def out():
    return logout()

if __name__ == '__main__':
    app.run(debug=True)