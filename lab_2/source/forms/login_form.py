from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, HiddenField, IntegerField, PasswordField
from wtforms import validators


class LoginForm(FlaskForm):

    login_id = IntegerField("ID: ", [
        validators.DataRequired("Please enter student id."),
        validators.NumberRange(1, 9999, "ID should be integer")
    ])

    password = PasswordField("Password: ", [
        validators.DataRequired("Please enter password."),
        validators.Length(6, 40, "Password should be from 6 to 40 symbols")
    ])

    log_in = SubmitField("Log in")
