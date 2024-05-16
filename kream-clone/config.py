import os

secret_key = 'kreamSecretKey'
basedir = os.path.abspath(os.path.dirname(__file__))

DELIVERY_TYPE = ["빠른 배송", "일반 배송"]


class Config:
    SECRET_KEY = secret_key
    BCRYPT_LEVEL = 10

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'kream.db')
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
