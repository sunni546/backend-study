import os

secret_key = 'instaSecretKey'
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = secret_key
    BCRYPT_LEVEL = 10

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'insta.db')
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
