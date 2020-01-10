import os

username = 'postgres'
password = 'nevermorepoem091'
host = 'localhost'
port = '5432'
database = 'postgres'
DATABASE_URI = os.getenv("DATABASE_URL", 'postgresql://postgres:{}@{}:{}/{}'.format(password, host, port, database))