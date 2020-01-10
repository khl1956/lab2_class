from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, HiddenField, IntegerField, RadioField, BooleanField
from wtforms import validators
from wtforms.validators import DataRequired
from datetime import date


class SearchTagForm(FlaskForm):

    search_request = StringField("Search: ", [
        validators.DataRequired("Please enter search request."),
        validators.Length(3, 40, "Search request should be from 3 to 40 symbols")
    ])

    programming_tag = BooleanField('Programming')

    algorithm_tag = BooleanField('Algorithm')

    graphics_tag = BooleanField('Graphics')

    databases_tag = BooleanField('Databases')

    math_tag = BooleanField('Math')

    # practice_tag = BooleanField('Practice')
    #
    # lecture_tag = BooleanField('Lecture')

    search_by_tags = SubmitField("Search")

    result_1 = StringField("Result: ")

