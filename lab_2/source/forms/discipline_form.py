from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, HiddenField
from wtforms import validators
from datetime import date


class DisciplineForm(FlaskForm):

    # discipline_id = IntegerField("id: ", [
    #     validators.DataRequired("Please enter discipline id."),
    #     validators.NumberRange(1, 9999, "ID should be number")
    # ])

    discipline_id = HiddenField()

    discipline_name = StringField("discipline name: ", [
        validators.DataRequired("Please enter discipline name."),
        validators.Length(3, 50, "Name should be from 3 to 25 symbols")
    ])

    discipline_data = StringField("data (.html): ", [
        validators.DataRequired("Please enter discipline data."),
        validators.Length(5, 100, "Type should in html form.")
    ])

    programming_tag = BooleanField('Programming')

    algorithm_tag = BooleanField('Algorithm')

    graphics_tag = BooleanField('Graphics')

    databases_tag = BooleanField('Databases')

    math_tag = BooleanField('Math')

    submit = SubmitField("Save")