from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, HiddenField, IntegerField, PasswordField
from wtforms import validators
from datetime import date


class StudentForm(FlaskForm):

    # student_id = IntegerField("id: ", [
    #     validators.DataRequired("Please enter student id."),
    #     validators.NumberRange(1, 9999, "ID should be number")
    # ])

    student_id = HiddenField()

    student_name = StringField("name: ", [
        validators.DataRequired("Please enter student name."),
        validators.Length(3, 25, "Name should be from 3 to 25 symbols")
    ])

    student_surname = StringField("surname: ", [
        validators.DataRequired("Please enter student surname."),
        validators.Length(3, 25, "Type should be from 3 to 25 symbols")
    ])

    student_age = IntegerField("Age: ", [
        validators.DataRequired("Please enter student age."),
        validators.NumberRange(1, 99, "Age should be number. Maximum length 2 symbols.")])

    student_spec = IntegerField("Specialization: ", [
        validators.DataRequired("Please enter student specialization."),
        validators.NumberRange(100, 199, "Specialization code")])

    student_course = IntegerField("course: ", [
        validators.DataRequired("Please enter student course."),
        validators.NumberRange(1, 6, "Course should be number")])

    student_group = StringField("group: ", [
        validators.DataRequired("Please enter student Group."),
        validators.Length(3, 10, "Group should be as code")])

    student_password = PasswordField("password: ", [
        validators.DataRequired("Please enter correct password."),
        validators.Length(6, 20, "Passwords must be at least 6 characters in length")])

    submit = SubmitField("Save")