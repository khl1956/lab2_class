from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean, ForeignKeyConstraint, CheckConstraint
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()


class Student(Base):
    __tablename__ = 'Student'

    student_id = Column(Integer, primary_key=True, nullable=False)
    student_name = Column(String(25), nullable=False)
    student_surname = Column(String(25), nullable=False)
    student_age = Column(Integer, nullable=False)
    student_spec = Column(Integer, nullable=False)
    student_course = Column(Integer, nullable=False)
    student_group = Column(String(10), nullable=True)
    student_password = Column(String(40))

    search_child = relationship("Search")
    result_child = relationship("Result")
    login_child = relationship("login_session")
    car_child = relationship("Car")


class Car(Base):
    __tablename__ = 'Car'

    number = Column(Integer, ForeignKey('Student.student_id'), primary_key=True, nullable=False)
    model = Column(String)
    year = Column(Integer, CheckConstraint('year > 2000 and year < 2019'))
    color = Column(String, CheckConstraint('color="red" or color="white" or color="black"'))



class Search(Base):
    __tablename__ = 'Search'

    search_id = Column(Integer, primary_key=True, nullable=False)
    student_id = Column(Integer, ForeignKey('Student.student_id'), nullable=False)
    search_request = Column(String(100), nullable=False)
    search_request_date = Column(DateTime, nullable=False, default=datetime.datetime.now())
    s_tag_programming = Column(Boolean)
    s_tag_algorithm = Column(Boolean)
    s_tag_graphics = Column(Boolean)
    s_tag_databases = Column(Boolean)
    s_tag_math = Column(Boolean)

    result_child = relationship("Result")


class Discipline(Base):
    __tablename__ = 'Discipline'

    discipline_id = Column(Integer, primary_key=True, nullable=False)
    discipline_name = Column(String(40), nullable=False)
    discipline_data = Column(String(200), nullable=False)
    tag_programming = Column(Boolean)
    tag_algorithm = Column(Boolean)
    tag_graphics = Column(Boolean)
    tag_databases = Column(Boolean)
    tag_math = Column(Boolean)

    discipline_entity = relationship("Result")


class Result(Base):
    __tablename__ = 'Result'

    result_id = Column(Integer, primary_key=True, nullable=False)
    student_id = Column(Integer, ForeignKey('Student.student_id'), nullable=False)
    search_id = Column(Integer, ForeignKey('Search.search_id'), nullable=False)
    discipline_id = Column(Integer, ForeignKey('Discipline.discipline_id'))
    discipline_name = Column(String(40))
    result_data = Column(String(100))

class login_session(Base):
    __tablename__ = 'login_session'

    login_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('Student.student_id'), nullable=False)
    login_date = Column(DateTime, nullable=False, default=datetime.datetime.today())


if __name__ == '__main__':
    from source.dao.db import PostgresDb

    db = PostgresDb()
    # simple query test
    # q1 = db.sqlalchemy_session.query(Discipline).all()
    # q2 = Student(
    #     student_id=323,
    #     student_name="wewe",
    #     student_surname="wewe",
    #     student_age=12,
    #     student_spec=334,
    #     student_course=4,
    #     student_group="33ff")
    #
    # db = PostgresDb()
    # db.sqlalchemy_session.add(q2)
    # db.sqlalchemy_session.commit()
    # a = db.sqlalchemy_session.query(Student).join(Search).all()
    # print(q2)



