import os

secret_key = 'secretKey'
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = secret_key
    BCRYPT_LEVEL = 10

    # 문자열 URL : "dialect+driver://username:password@host:port/database"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'todo.db')
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
