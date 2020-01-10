from os import environ
from GitLecture import app
import os
from flask_wtf.csrf import CSRFProtect

if __name__ == '__main__':
    csrf = CSRFProtect(app)
    app.config['SECRET_KEY'] = "secretkey"
    app.config['WTF_CSRF_SECRET_KEY'] = "secretkey"
    csrf.init_app(app)