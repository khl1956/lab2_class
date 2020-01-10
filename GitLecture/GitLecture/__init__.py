"""
The flask application package.
"""

from flask import Flask
from GitLecture.dao.db import PostgresDb
from GitLecture.dao.entities import Base
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
db = PostgresDb()

Base.metadata.create_all(db.sqlalchemy_engine)

csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = "secretkey"
app.config['WTF_CSRF_SECRET_KEY'] = "secretkey"
csrf.init_app(app)

import GitLecture.views
