"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, url_for
from GitLecture import app
from GitLecture.forms.forms import *
from GitLecture import db
from GitLecture.dao.entities import *
import requests, json, re

def UserToForm(user):
    form = UserForm()

    form.user_login.data = user.user_login
    form.user_password.data = user.user_password
    form.user_url.data = user.user_github_url
    return form

def FormToUser(form): 
     user = User()
     user.user_login = form.user_login.data
     r = requests.get('https://api.github.com/users/' + form.user_login.data, auth=(form.user_login.data, form.user_password.data))
     user.user_url = r.json()['html_url']
     return user

@app.route('/', methods=['GET', 'POST'])
def createUser():
    userForm = UserForm()
    if request.method == 'POST':
        errors = ""
        r = requests.get('https://api.github.com/user', auth=(userForm.user_login.data, userForm.user_password.data))
        if r.status_code != 200:
            errors = "Invalid github user"
        else:
            temp_user = FormToUser(userForm)
            try:
                db.sqlalchemy_session.add(temp_user)
                db.sqlalchemy_session.commit()
                return redirect(url_for('users'))
            except :
                errors = "User " + temp_user.user_login + " exist"
                db.sqlalchemy_session.rollback()

        return render_template(
                'create_user.html',
                form = userForm,
                errors = errors)
    else:
        return render_template(
                'create_user.html',
                form = userForm)
        
@app.route('/users')
@app.route('/users/<error>')
def users(error = ''):
    userForm = UserForm()
    dbUsers = db.sqlalchemy_session.query(User).all()
    return render_template(
            'users.html',
            users = dbUsers,
            form = userForm,
            error = error)


@app.route('/user-delete/<userId>', methods=['POST'])
def userDelete(userId):
    login = request.form['user_login']
    password = request.form['user_password']
    user = db.sqlalchemy_session.query(User.user_login).filter(User.user_id == int(userId)).one()
    db.sqlalchemy_session.commit()

    if login != user.user_login:
        return redirect(url_for('users', error = "Invalid user to delete"))

    r = requests.get('https://api.github.com/user', auth=(login, password))
    if r.status_code != 200:
        return redirect(url_for('users', error = "Invalid user to delete"))

    db.sqlalchemy_session.query(Lecture).filter(Lecture.user_id_fk == userId).delete()
    db.sqlalchemy_session.query(User).filter(User.user_id == userId).delete()
    db.sqlalchemy_session.commit()
    return redirect(url_for('users'))

@app.route('/lectures', methods=['GET', 'POST'])
@app.route('/lectures/<error>', methods=['GET', 'POST'])
def lectures(error = ''):
    dbLectures = db.sqlalchemy_session.query(Lecture.lecture_id, Lecture.lecture_name, Lecture.gitgist_id, User.user_login, Subject.subject_name ).join(User).join(Subject).all()
    userForm = UserForm()
    
    if request.method == 'POST':
        pass
    else:
        return render_template(
            'lectures.html',
            lectures = dbLectures,
            form = userForm,
            deleteError = error)

@app.route('/lecture-read/<lectureId>', methods=['GET', 'POST'])
def lectureRead(lectureId):
    lecture = db.sqlalchemy_session.query(Lecture.gitgist_id, Lecture.lecture_name).filter(Lecture.lecture_id == int(lectureId)).one()
    db.sqlalchemy_session.commit()
    r = requests.get('https://api.github.com/gists/' + lecture.gitgist_id)
    if (r.status_code != 200):
        return redirect(url_for('lectures', error = "Error reading lecture. It may be deleted from gist."))

    text_tag_map = {}

    lecture_text = r.json()["files"][lecture.lecture_name]["content"]
    
    tags = re.findall(r'\[#.*\]', lecture_text)
    tags_count = len(tags)

    if tags:
        for i in range(0, tags_count):
            tag_start_index = lecture_text.index(tags[i])
            if i == 0:
                if tag_start_index != 0:
                    text_tag_map[''] = lecture_text[0, tag_start_index - 1]
                    continue 
            if i != tags_count - 1:
                tag_end_index = lecture_text.index(tags[i + 1])
                text_tag_map[tags[i][2 : len(tags[i]) - 1]] = lecture_text[tag_start_index + len(tags[i]) : tag_end_index - 1]
            else:
                text_tag_map[tags[i][2 : len(tags[i]) - 1]] = lecture_text[tag_start_index + len(tags[i]):]
    else:
        text_tag_map[''] = lecture_text

    return render_template('read_lecture.html',
                           lectureName = lecture.lecture_name,
                           lectureMap = text_tag_map,
                           lectureId = lectureId)

@app.route('/lecture-delete/<lectureId>', methods=['POST'])
def lectureDelete(lectureId):
    login = request.form['user_login']
    password = request.form['user_password']
    lecture = db.sqlalchemy_session.query(Lecture.gitgist_id, Lecture.user_id_fk).filter(Lecture.lecture_id == lectureId).one()
    user = db.sqlalchemy_session.query(User.user_login).filter(User.user_id == lecture.user_id_fk).one()
    db.sqlalchemy_session.commit()

    if login != user.user_login:
        return redirect(url_for('lectures', error = "Invalid user to delete"))

    r = requests.delete('https://api.github.com/gists/' + lecture.gitgist_id, auth=(login, password))
    if r.status_code == 401:
        return redirect(url_for('lectures', error = "Invalid user to delete"))
    if r.status_code == 404:
        db.sqlalchemy_session.query(Lecture).filter(Lecture.lecture_id == lectureId).delete()
        db.sqlalchemy_session.commit()
        return redirect(url_for('lectures', error = "Lecture already deleted from gist"))

    db.sqlalchemy_session.query(Lecture).filter(Lecture.lecture_id == lectureId).delete()
    db.sqlalchemy_session.commit()
    return redirect(url_for('lectures'))

@app.route('/subjects', methods=['GET','POST'])
def subjects():
    dbSubjects = db.sqlalchemy_session.query(Subject).all()
    form = SubjectForm()
    deleteForm = DeleteForm()
    if request.method == 'POST':
        temp_subject = Subject()
        temp_subject.subject_name = form.subject_name.data
        temp_subject.subject_description = form.subject_description.data
        try:
            db.sqlalchemy_session.add(temp_subject)
            db.sqlalchemy_session.commit()
        except :
            db.sqlalchemy_session.rollback()
            return render_template(
            'subjects.html',
            subjects = dbSubjects,
            form = form,
            errors = "Subject " + temp_subject.subject_name + " exist")
        return redirect(url_for('subjects'))
    else:
        return render_template(
            'subjects.html',
            subjects = dbSubjects,
            form = form,
            deleteForm = deleteForm)

@app.route('/subject-delete/<subjectId>', methods=['POST'])
def subjectDelete(subjectId):
    db.sqlalchemy_session.query(Subject).filter(Subject.subject_id == subjectId).delete()
    db.sqlalchemy_session.commit()
    return redirect(url_for('subjects'))

@app.route('/edit-subject/<subjectId>', methods=['POST', 'GET'])
def subjectEdit(subjectId):
    subject = db.sqlalchemy_session.query(Subject).filter(Subject.subject_id == subjectId).one()
    db.sqlalchemy_session.commit()
    form = SubjectForm()

    if request.method == 'POST':
        subject.subject_name = form.subject_name.data
        subject.subject_description = form.subject_description.data
        try:
            db.sqlalchemy_session.commit()
        except :
            db.sqlalchemy_session.rollback()
            return render_template(
                'edit_subject.html',
                form = form,
                subjectId = subjectId,
                subjectName = subject.subject_name,
                errors = "Subject " + form.subject_name.data + " exist")
        return redirect(url_for('subjects'))
    else:
        form.subject_name.data = subject.subject_name
        form.subject_description.data = subject.subject_description
        return render_template(
            'edit_subject.html',
            form = form,
            subjectId = subjectId,
            subjectName = subject.subject_name)


@app.route('/create-lecture', methods=['POST', 'GET'])
def createLecture():
    form = LectureForm()
    form.subject.choices = db.sqlalchemy_session.query(Subject.subject_id, Subject.subject_name).all()
    if request.method == 'POST':
        try:
            user_id = db.sqlalchemy_session.query(User.user_id).filter(User.user_login == form.user_name.data).one()
            db.sqlalchemy_session.commit()
        except :
            db.sqlalchemy_session.rollback()
            return render_template(
            'create_lecture.html',
            form = form,
            errors = "User " + form.user_name.data + " not exist")
        r = requests.post('https://api.github.com/gists', json.dumps({'files':{ form.lecture_name.data:{"content": form.lecture_text.data}}}), auth=requests.auth.HTTPBasicAuth(form.user_name.data, form.user_password.data)) 
        if r.status_code != 201:
            return render_template(
            'create_lecture.html',
            form = form,
            errors = "Invalid user")
        temp_lecture = Lecture()

        temp_lecture.lecture_name = form.lecture_name.data
        temp_lecture.user_id_fk = user_id
        temp_lecture.subject_id_fk = form.subject.data
        temp_lecture.gitgist_id = r.json()['id']

        db.sqlalchemy_session.add(temp_lecture)
        db.sqlalchemy_session.commit()

        return redirect(url_for('lectures'))
    else:
        return render_template(
            'create_lecture.html',
            form = form)

@app.route('/dashboard')
def dashboard():
    subjects = db.sqlalchemy_session.query(Subject.subject_id, Subject.subject_name).all()
    
    subjects_str = ''
    subjects_values = ''

    for subject in subjects:
        e = db.sqlalchemy_session.query(Lecture.lecture_id).all()
        subjects_values += str(db.sqlalchemy_session.query(Lecture.lecture_id).filter(Lecture.subject_id_fk == subject.subject_id).count()) + ',' 
        subjects_str += '\'' + str(subject.subject_name) + '\','

    return render_template('dashboard.html', 
                           subjects = subjects_str,
                           subjects_values = subjects_values)

@app.route('/books/show')
def books_show():
    for i in range(3):
        n_book = Book()
        n_book.book_author = 'author' + str(i)
        n_book.book_category = 'Math'
        n_book.book_isbn = '34fd3-3fdf2-fsdf34f'
        n_book.book_year = 2020
        lectures_list = []
        dbLectures = db.sqlalchemy_session.query(Lecture).all()
        for lecture in dbLectures:
            lectures_list.append(lecture)
        n_book.lectures = lectures_list
        db.sqlalchemy_session.add(n_book)
        db.sqlalchemy_session.commit()
        

@app.route('/books', methods = ['GET', 'POST'])
def books():
    dbBooks = db.sqlalchemy_session.query(Book).all()
    bookForm = BookForm()
    bookForm.book_category.choices = [("Math","Math"), ("English", "English"), ("Ukraine", "Ukraine")]
    
    if request.method == 'POST':
        if bookForm.year.data <= 2019:
            return render_template('books.html',
                           books = dbBooks,
                           form = bookForm,
                           error = "Invalid year")
        else:
            n_book = Book()
            n_book.book_author = 'author' + str(i)
            n_book.book_category = 'Math'
            n_book.book_isbn = '34fd3-3fdf2-fsdf34f'
            n_book.book_year = 2020
            lectures_list = []
            dbLectures = db.sqlalchemy_session.query(Lecture).all()
            for lecture in dbLectures:
                lectures_list.append(lecture)
            n_book.lectures = lectures_list
            db.sqlalchemy_session.commit()

    return render_template('books.html',
                           books = dbBooks,
                           form = bookForm)

@app.route('/books/insert')
def books_insert():
    bookForm = BookForm()