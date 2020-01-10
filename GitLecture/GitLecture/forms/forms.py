from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, HiddenField, PasswordField, SelectField, TextAreaField, IntegerField
from wtforms import validators
from datetime import date
from GitLecture.dao.entities import Subject
from GitLecture.dao.db import PostgresDb


class UserForm(FlaskForm):
    user_id = HiddenField()

    user_login = StringField("Login: ", [
        validators.DataRequired("Please enter github login."),
        validators.Length(3, 255, "Login should be from 3 to 255 symbols")
    ])

    user_password = PasswordField("Password: ", [
        validators.DataRequired("Please enter password."),
        validators.Length(3, 255, "Should be from 3 to 255 symbols")
    ])

    submit = SubmitField("Save")

class SubjectForm(FlaskForm):
    subject_id = HiddenField()

    subject_name = StringField("Subject name: ", [
        validators.DataRequired("Please enter subject name."),
        validators.Length(3, 255, "Login should be from 3 to 255 symbols")
    ])

    subject_description = StringField("Subject description: ", [
        validators.DataRequired("Please enter subject name."),
        validators.Length(3, 255, "Login should be from 3 to 255 symbols")
    ])

class LectureForm(FlaskForm):
    lecture_id = HiddenField()

    lecture_name = StringField("Lecture name: ", [
        validators.DataRequired("Please enter lecture name."),
        validators.Length(3, 255, "Lecture name should be from 3 to 255 symbols")
    ])

    user_name = StringField("Login: ", [
        validators.DataRequired("Please enter user name."),
        validators.Length(3, 255, "User name should be from 3 to 255 symbols")
    ])

    user_password = PasswordField("Password: ", [
        validators.DataRequired("Please enter password."),
        validators.Length(3, 255, "Should be from 3 to 255 symbols")
    ])

    subject = SelectField("Subject: ")

    lecture_text = TextAreaField("Lecture text")

class BookForm(FlaskForm):
    book_id = HiddenField()

    book_author = StringField("Author: ", [
        validators.DataRequired("Please enter user name."),
        validators.Length(3, 255, "User name should be from 3 to 255 symbols")
    ])

    isbn = StringField("ISBN: ", [
        validators.DataRequired("Please enter ISBN."),
        validators.Length(3, 255, "ISBN should be from 3 to 255 symbols")
    ])

    year = IntegerField("Book year", [validators.DataRequired("Please enter book year.")])
    
    book_category = SelectField("Category: ")

class DeleteForm(FlaskForm):
    delete = HiddenField()