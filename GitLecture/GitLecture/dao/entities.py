from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, ForeignKeyConstraint, update, func
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_login = Column(String(255), nullable=False)
    user_url = Column(String(255), nullable=False)

    user_lectures = relationship("Lecture")

class Subject(Base):
    __tablename__ = 'Subjects'

    subject_id = Column(Integer, primary_key=True, autoincrement=True)
    subject_name = Column(String(255), nullable=False)
    subject_description = Column(String(255), nullable=False)

class LectureIncludeBook(Base):
    __tablename__ = 'BookInLecture'

    lecture_id = Column(Integer, ForeignKey('Lectures.lecture_id'), primary_key = True)
    book_id = Column(Integer, ForeignKey('Books.book_id'), primary_key = True)

class Lecture(Base):
    __tablename__ = 'Lectures'

    lecture_id = Column(Integer, primary_key = True, autoincrement=True)
    lecture_name = Column(String(255), nullable=False)
    gitgist_id = Column(String(255), nullable=False)
    user_id_fk = Column(Integer, ForeignKey('Users.user_id'))
    subject_id_fk = Column(Integer, ForeignKey('Subjects.subject_id'))

    books = relationship("Book", secondary="BookInLecture", backref = backref( "Lectures" ))

class Book(Base):
    __tablename__ = 'Books'

    book_id = Column(Integer, primary_key = True, autoincrement=True)
    book_author = Column(String(255), nullable=False)
    book_isbn = Column(String(255), nullable=False)
    book_year = Column(Integer, nullable = False)
    book_category = Column(String(255), nullable=False)

    lectures = relationship("Lecture", secondary="BookInLecture", backref = backref( "Books" ))

