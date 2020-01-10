from flask_wtf import Form
from wtforms import SelectField, SubmitField, BooleanField
from sqlalchemy import func
from source.dao.db import PostgresDb
from source.dao.orm.entities import Search, Result, login_session, Discipline, Car


class StudentSearchForm(Form):
    student_id = SelectField("student_id:", choices=[("", "---")])
    submit = SubmitField("Search")

    def init_search(self):
        db = PostgresDb()
        self.student_id.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Search.student_id).distinct(Search.student_id).all())]

    def init_result(self):
        db = PostgresDb()
        self.student_id.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Result.student_id).distinct(Result.student_id).all())]


if __name__ == '__main__':
    from source.dao.db import PostgresDb

    db = PostgresDb()
    input_data = 'Комп`ютер'
    res_filter = db.sqlalchemy_session.query(Car.color).all()

    color_2 = []
    model_2 = []
    color = db.sqlalchemy_session.query(Car.model, func.count(Car.color)).group_by(Car.model)
    model = db.sqlalchemy_session.query(Car.model).all()
    q1 = color.all()
    print(q1)
    # for j in range(len(color)):
    #     color_2.append(color[j][0])
    # for k in range(len(model)):
    #     model_2.append(model[k][0])
    #
    # print(model_2, color_2)

    # group_2 = db.sqlalchemy_session.query(Result.student_id, func.count(Result.student_id), Result.discipline_name) \
    #     .filter(Result.student_id == searchrequest.student_id.data).group_by(Result.discipline_name, Result.student_id)
    # db.sqlalchemy_session.commit()
    #
    # q2 = group_2.all()










