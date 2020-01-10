from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from GitLecture.dao.credentials import *


class PostgresDb(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            try:
                engine = create_engine(DATABASE_URI)

                Session = sessionmaker(bind=engine)
                session = Session()

                PostgresDb._instance.sqlalchemy_session = session
                PostgresDb._instance.sqlalchemy_engine = engine

            except Exception as error:
                print('Error: connection not established {}'.format(error))

        return cls._instance

    def __init__(self):
        engine = create_engine(DATABASE_URI)

        Session = sessionmaker(bind=engine)
        session = Session()

        self.sqlalchemy_session = session
        self.sqlalchemy_engine = engine

    def __del__(self):
        self.sqlalchemy_session.close()

