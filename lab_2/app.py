from flask import *
from source.dao.orm.entities import *
from source.dao.db import PostgresDb
from source.dao.data import *
from source.forms.student_form import StudentForm
from source.forms.search_form import SearchTagForm
from source.forms.discipline_form import DisciplineForm
from source.forms.search_request_form import StudentSearchForm
from source.forms.login_form import LoginForm
from sqlalchemy import func
from datetime import date
import datetime
import json
import plotly
import plotly.graph_objs as go
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "jkm-vsnej9l-vm9sqm3:lmve")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL",
                                                  f"postgresql://{username}:{password}@{host}:{port}/{database}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['WHOOSH_BASE'] = 'whoosh'

_login = 0
_password = ''


@app.route('/', methods=['GET', 'POST'])
def root():
    log = LoginForm()
    db = PostgresDb()
    error = None
    global _login
    global _password
    _login = 0
    _password = ''
    if request.method == 'POST':
        _login = log.login_id.data
        _password = log.password.data
        db = PostgresDb()
        password_check = db.sqlalchemy_session.query(Student.student_password).filter(
            Student.student_id == log.login_id.data).first()
        login_check = db.sqlalchemy_session.query(Student.student_id).filter(
            Student.student_password == log.password.data).first()
        if log.password.data == 'adminpass' and log.login_id.data == 1001:
            login_obj = login_session(login_id=db.sqlalchemy_session.query(func.max(login_session.login_id) + 1),
                                      student_id=log.login_id.data,
                                      login_date=datetime.datetime.now())
            db.sqlalchemy_session.add(login_obj)
            db.sqlalchemy_session.commit()
            return redirect(url_for('search'))
        else:
            try:
                if log.password.data != password_check[0] and log.login_id.data != login_check[0]:
                    error = 'Invalid login or password'
                    return render_template('index.html', form=log, error=error, form_name="Log in")
                else:
                    login_obj = login_session(login_id=db.sqlalchemy_session.query(func.max(login_session.login_id) + 1),
                                              student_id=log.login_id.data,
                                              login_date=datetime.datetime.now())
                    db.sqlalchemy_session.add(login_obj)
                    db.sqlalchemy_session.commit()

                    return redirect(url_for('search_data'))
            except TypeError:
                error = 'Invalid login or password'
                return render_template('index.html', form=log, error=error, form_name="Log in")
    return render_template('index.html', form=log, form_name="Log in")


@app.route('/student', methods=['POST', 'GET'])
def student():
    if _login != 0 and _password != '':
        db = PostgresDb()
        students = db.sqlalchemy_session.query(Student).filter(Student.student_id != 1001).all()
        #print(students)
        return render_template('student.html', students=students)
    else:
        return render_template('login_exception.html')


@app.route('/new_student', methods=['GET', 'POST'])
def new_student():
    if _login != 0 and _password != '':
        form = StudentForm()
        db = PostgresDb()

        if request.method == 'POST':
            student_obj = Student(
                student_id=db.sqlalchemy_session.query(func.max(Student.student_id) + 1),
                student_name=form.student_name.data,
                student_surname=form.student_surname.data,
                student_age=form.student_age.data,
                student_spec=form.student_spec.data,
                student_course=form.student_course.data,
                student_group=form.student_group.data,
                student_password=form.student_password.data)

            db = PostgresDb()
            db.sqlalchemy_session.add(student_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('student'))

        return render_template('student_form.html', form=form, form_name="New student", action="new_student")
    else:
        return render_template('login_exception.html')


@app.route('/edit_student', methods=['GET', 'POST'])
def edit_student():
    if _login != 0 and _password != '':
        form = StudentForm()

        if request.method == 'GET':

            student_id = request.args.get('student_id')
            db = PostgresDb()
            student = db.sqlalchemy_session.query(Student).filter(Student.student_id == student_id).one()

            form.student_id.data = student.student_id
            form.student_name.data = student.student_name
            form.student_surname.data = student.student_surname
            form.student_age.data = student.student_age
            form.student_spec.data = student.student_spec
            form.student_course.data = student.student_course
            form.student_group.data = student.student_group
            form.student_password.data = student.student_password

            db.sqlalchemy_session.commit()

            return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student")

        else:

            db = PostgresDb()

            student = db.sqlalchemy_session.query(Student).filter(Student.student_id == form.student_id.data).one()

            student.student_id = form.student_id.data
            student.student_name = form.student_name.data
            student.student_surname = form.student_surname.data
            student.student_age = form.student_age.data
            student.student_spec = form.student_spec.data
            student.student_course = form.student_course.data
            student.student_group = form.student_group.data
            student.student_password = form.student_password.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('student'))
    else:
        return render_template('login_exception.html')


@app.route('/delete_student')
def delete_student():
    if _login != 0 and _password != '':
        student_id = request.args.get('student_id')
        db = PostgresDb()
        db.sqlalchemy_session.query(Student).filter(Student.student_id == student_id).subquery()
        db.sqlalchemy_session.query(Result).filter(Result.student_id == student_id).delete(synchronize_session='fetch')
        db.sqlalchemy_session.query(Search).filter(Search.student_id == student_id).delete(synchronize_session='fetch')
        db.sqlalchemy_session.query(Student).filter(Student.student_id == student_id).delete()
        db.sqlalchemy_session.commit()
        return redirect(url_for('student'))
    else:
        return render_template('login_exception.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
    if _login != 0 and _password != '':
        search = SearchTagForm()
        db = PostgresDb()

        if request.method == 'POST':
            search_obj = Search(search_id=db.sqlalchemy_session.query(func.max(Search.search_id) + 1),
                                student_id=db.sqlalchemy_session.query(login_session.student_id).order_by(login_session.login_id.desc()).first(),
                                search_request=search.search_request.data,
                                search_request_date=datetime.datetime.now(),
                                s_tag_programming=search.programming_tag.data,
                                s_tag_algorithm=search.algorithm_tag.data,
                                s_tag_graphics=search.graphics_tag.data,
                                s_tag_databases=search.databases_tag.data,
                                s_tag_math=search.math_tag.data)
            db.sqlalchemy_session.add(search_obj)
            db.sqlalchemy_session.commit()

            res_filter = db.sqlalchemy_session.query(Discipline.discipline_name, Discipline.discipline_data). \
                filter(Discipline.discipline_name.like('%' + search.search_request.data + '%')).all()
            temp = db.sqlalchemy_session.query(Discipline.discipline_id). \
                filter(Discipline.discipline_name.like('%' + search.search_request.data + '%')).all()
            res_temp = []
            for k in range(len(temp)):
                res_temp = db.sqlalchemy_session.query(Discipline.discipline_id, Discipline.discipline_name,
                                                       Discipline.discipline_data) \
                    .filter(Discipline.discipline_id == temp[k]).all()
            print(res_temp)

            for p in range(len(res_temp)):
                result_by_name = Result(result_id=db.sqlalchemy_session.query(func.max(Result.result_id) + 1),
                                        student_id=db.sqlalchemy_session.query(login_session.student_id).order_by(
                                            login_session.login_id.desc()).first(),
                                        search_id=db.sqlalchemy_session.query(func.max(Search.search_id)),
                                        discipline_id=res_temp[p][0],
                                        discipline_name=res_temp[p][1],
                                        result_data=res_temp[p][2])
                db.sqlalchemy_session.add(result_by_name)
                db.sqlalchemy_session.commit()

            search_q1 = db.sqlalchemy_session.query(Search.search_id,
                                                    Search.student_id,
                                                    Search.search_request,
                                                    Search.s_tag_programming,
                                                    Search.s_tag_algorithm,
                                                    Search.s_tag_graphics,
                                                    Search.s_tag_databases,
                                                    Search.s_tag_math).order_by(Search.search_id.desc()).first()



            discipline_q = db.sqlalchemy_session.query(Discipline.discipline_id,
                                                       Discipline.discipline_name,
                                                       Discipline.discipline_data,
                                                       Discipline.tag_programming,
                                                       Discipline.tag_algorithm,
                                                       Discipline.tag_graphics,
                                                       Discipline.tag_databases,
                                                       Discipline.tag_math).all()

            result = []
            for tuple in discipline_q:
                for element in range(len(search_q1)):
                    if tuple[element] == True and search_q1[element] == True:
                        result.append(tuple)

            for j in range(len(result)):
                res = Result(result_id=db.sqlalchemy_session.query(func.max(Result.result_id) + 1),
                             student_id=db.sqlalchemy_session.query(login_session.student_id).order_by(login_session.login_id.desc()).first(),
                             search_id=db.sqlalchemy_session.query(func.max(Search.search_id)),
                             discipline_id=result[j][0],
                             discipline_name=result[j][1],
                             result_data=result[j][2])
                db.sqlalchemy_session.add(res)
                db.sqlalchemy_session.commit()
            result_final = db.sqlalchemy_session.query(Result.discipline_name, Result.result_data).order_by(Result.result_id.desc()).limit(len(result)).all()
            print(result_final)
            return render_template('search.html', form=search, res_filter=res_filter, result_final=result_final, form_name="Search", action="search")
        return render_template('search.html', form=search, form_name="Search", action="search")
    else:
        return render_template('login_exception.html')


@app.route('/get', methods=['GET'])
def get():
    db = PostgresDb()
    if request.method == 'GET':
        get_object1 = Car(number=1,
                           model='Toyota',
                           year=2018,
                           color='red')
        get_object2 = Car(number=2,
                           model='BMW',
                           year=2015,
                           color='white')
        get_object3 = Car(number=3,
                           model='Volvo',
                           year=2006,
                           color='black')


        db.sqlalchemy_session.add(get_object1)
        db.sqlalchemy_session.add(get_object2)
        db.sqlalchemy_session.add(get_object3)
        db.sqlalchemy_session.commit()
        cars = db.sqlalchemy_session.query(Car).all()
        print('Comitted')
        return render_template('show.html', cars=cars)

@app.route('/pie', methods=['POST', 'GET'])
def pie():
    db = PostgresDb()
    if request.method == 'GET':
        data = {}
        color_2 = []
        model_2 = []
        color = db.sqlalchemy_session.query(Car.model, func.count(Car.color)).group_by(Car.model).all()
        print(color)

        for j in range(len(color)):
            model_2.append(color[j][0])
        for k in range(len(color)):
            color_2.append(color[k][1])

        pie = go.Pie(labels=model_2, values=color_2)

        data["pie"] = [pie]

        json_data = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('pie.html', json=json_data)


@app.route('/search_data', methods=['POST', 'GET'])
def search_data():
    if _login != 0 and _password != '':
        search_data = SearchTagForm()
        db = PostgresDb()

        if request.method == 'POST':
            search_obj = Search(search_id=db.sqlalchemy_session.query(func.max(Search.search_id) + 1),
                                student_id=db.sqlalchemy_session.query(login_session.student_id).order_by(login_session.login_id.desc()).first(),
                                search_request=search_data.search_request.data,
                                search_request_date=datetime.datetime.now(),
                                s_tag_programming=search_data.programming_tag.data,
                                s_tag_algorithm=search_data.algorithm_tag.data,
                                s_tag_graphics=search_data.graphics_tag.data,
                                s_tag_databases=search_data.databases_tag.data,
                                s_tag_math=search_data.math_tag.data)
            db.sqlalchemy_session.add(search_obj)
            db.sqlalchemy_session.commit()


            res_filter = db.sqlalchemy_session.query(Discipline.discipline_name, Discipline.discipline_data). \
                filter(Discipline.discipline_name.like('%' + search_data.search_request.data + '%')).all()
            temp = db.sqlalchemy_session.query(Discipline.discipline_id).\
                filter(Discipline.discipline_name.like('%' + search_data.search_request.data + '%' )).all()
            res_temp = []
            for k in range(len(temp)):
                res_temp = db.sqlalchemy_session.query(Discipline.discipline_id, Discipline.discipline_name, Discipline.discipline_data)\
                    .filter(Discipline.discipline_id == temp[k]).all()
            print(res_temp)

            for p in range(len(res_temp)):
                result_by_name = Result(result_id=db.sqlalchemy_session.query(func.max(Result.result_id) + 1),
                                        student_id=db.sqlalchemy_session.query(login_session.student_id).order_by(login_session.login_id.desc()).first(),
                                        search_id=db.sqlalchemy_session.query(func.max(Search.search_id)),
                                        discipline_id=res_temp[p][0],
                                        discipline_name=res_temp[p][1],
                                        result_data=res_temp[p][2])
                db.sqlalchemy_session.add(result_by_name)
                db.sqlalchemy_session.commit()

            search_q1 = db.sqlalchemy_session.query(Search.search_id,
                                                    Search.student_id,
                                                    Search.search_request,
                                                    Search.s_tag_programming,
                                                    Search.s_tag_algorithm,
                                                    Search.s_tag_graphics,
                                                    Search.s_tag_databases,
                                                    Search.s_tag_math).order_by(Search.search_id.desc()).first()

            discipline_q = db.sqlalchemy_session.query(Discipline.discipline_id,
                                                       Discipline.discipline_name,
                                                       Discipline.discipline_data,
                                                       Discipline.tag_programming,
                                                       Discipline.tag_algorithm,
                                                       Discipline.tag_graphics,
                                                       Discipline.tag_databases,
                                                       Discipline.tag_math).all()

            result = []
            for tuple in discipline_q:
                for element in range(len(search_q1)):
                    if tuple[element] == True and search_q1[element] == True:
                        result.append(tuple)

            for j in range(len(result)):
                res = Result(result_id=db.sqlalchemy_session.query(func.max(Result.result_id) + 1),
                             student_id=db.sqlalchemy_session.query(login_session.student_id).order_by(login_session.login_id.desc()).first(),
                             search_id=db.sqlalchemy_session.query(func.max(Search.search_id)),
                             discipline_id=result[j][0],
                             discipline_name=result[j][1],
                             result_data=result[j][2])
                db.sqlalchemy_session.add(res)
                db.sqlalchemy_session.commit()
            result_final = db.sqlalchemy_session.query(Result.discipline_name, Result.result_data).order_by(Result.result_id.desc()).limit(len(result)).all()
            print(result_final)
            return render_template('search_data.html', form=search_data, res_filter=res_filter, result_final=result_final, form_name="Search_data", action="search_data")

        return render_template('search_data.html', form=search_data, form_name="Search_data", action="search_data")
    else:
        return render_template('login_exception.html')


@app.route('/discipline', methods=['POST', 'GET'])
def discipline():
    if _login != 0 and _password != '':
        db = PostgresDb()
        disciplines = db.sqlalchemy_session.query(Discipline).all()
        return render_template('discipline.html', disciplines=disciplines)
    else:
        return render_template('login_exception.html')

@app.route('/new_discipline', methods=['GET', 'POST'])
def new_discipline():
    if _login != 0 and _password != '':
        form = DisciplineForm()
        db = PostgresDb()

        if request.method == 'POST':
            discipline_obj = Discipline(discipline_id=db.sqlalchemy_session.query(func.max(Discipline.discipline_id) + 1),
                discipline_name=form.discipline_name.data,
                discipline_data=form.discipline_data.data,
                tag_programming=form.programming_tag.data,
                tag_algorithm=form.algorithm_tag.data,
                tag_graphics=form.graphics_tag.data,
                tag_databases=form.databases_tag.data,
                tag_math=form.math_tag.data)

            db = PostgresDb()
            db.sqlalchemy_session.add(discipline_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('discipline'))
        return render_template('discipline_form.html', form=form, form_name="New discipline", action="new_discipline")
    else:
        return render_template('login_exception.html')


@app.route('/edit_discipline', methods=['GET', 'POST'])
def edit_discipline():
    if _login != 0 and _password != '':
        form = DisciplineForm()

        if request.method == 'GET':

            discipline_id = request.args.get('discipline_id')
            db = PostgresDb()
            discipline = db.sqlalchemy_session.query(Discipline).filter(Discipline.discipline_id == discipline_id).one()

            form.discipline_id.data = discipline.discipline_id
            form.discipline_name.data = discipline.discipline_name
            form.discipline_data.data = discipline.discipline_data
            form.programming_tag.data = discipline.tag_programming
            form.algorithm_tag.data = discipline.tag_algorithm
            form.graphics_tag.data = discipline.tag_graphics
            form.databases_tag.data = discipline.tag_databases
            form.math_tag.data = discipline.tag_math

            db.sqlalchemy_session.commit()

            return render_template('discipline_form.html', form=form, form_name="Edit discipline", action="edit_discipline")

        else:

            db = PostgresDb()

            discipline = db.sqlalchemy_session.query(Discipline).filter(Discipline.discipline_id == form.discipline_id.data).one()

            discipline.discipline_id = form.discipline_id.data
            discipline.discipline_name = form.discipline_name.data
            discipline.discipline_data = form.discipline_data.data
            discipline.tag_programming = form.programming_tag.data
            discipline.tag_algorithm = form.algorithm_tag.data
            discipline.tag_graphics = form.graphics_tag.data
            discipline.tag_databases = form.databases_tag.data
            discipline.tag_math = form.math_tag.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('discipline'))
    else:
        return render_template('login_exception.html')


@app.route('/delete_discipline')
def delete_discipline():
    if _login != 0 and _password != '':
        discipline_id = request.args.get('discipline_id')
        db = PostgresDb()
        db.sqlalchemy_session.query(Discipline).filter(Discipline.discipline_id == discipline_id).subquery()
        db.sqlalchemy_session.query(Result).filter(Result.discipline_id == discipline_id).delete(synchronize_session='fetch')
        db.sqlalchemy_session.query(Discipline).filter(Discipline.discipline_id == discipline_id).delete()
        db.sqlalchemy_session.commit()
        return redirect(url_for('discipline'))
    else:
        return render_template('login_exception.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if _login != 0 and _password != '':
        searchrequest = StudentSearchForm()
        searchrequest.init_search()
        searchrequest.init_result()

        if request.method == 'POST':
            data = {}
            date = []
            request_count = []
            discipline = []
            result_count = []
            searchrequest.init_search()
            searchrequest.init_result()
            db = PostgresDb()
            group_1 = db.sqlalchemy_session.query(Search.student_id, func.count(Search.student_id), Search.search_request_date)\
                .filter(Search.student_id == searchrequest.student_id.data).group_by(Search.search_request_date, Search.student_id)
            group_2 = db.sqlalchemy_session.query(Result.student_id, func.count(Result.student_id), Result.discipline_name) \
                .filter(Result.student_id == searchrequest.student_id.data).group_by(Result.discipline_name, Result.student_id)
            db.sqlalchemy_session.commit()
            q1 = group_1.all()
            q2 = group_2.all()
            for i in range(len(q1)):
                date.append(str(q1[i][2]))
            for j in range(len(q1)):
                request_count.append(str(q1[j][1]))
            for i in range(len(q2)):
                discipline.append(str(q2[i][2]))
            for j in range(len(q2)):
                result_count.append(str(q2[j][1]))
            print(result_count)
            print(discipline)

            bar = go.Scatter(x=date, y=request_count, mode='markers')
            pie = go.Pie(labels=discipline, values=result_count)

            data["bar"] = [bar]
            data["pie"] = [pie]

            json_data = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

            return render_template('dashboard.html', json=json_data, discipline=discipline, searchrequest=searchrequest)

        return render_template('dashboard.html', searchrequest=searchrequest)
    else:
        return render_template('login_exception.html')


if __name__ == '__main__':
    app.run()
