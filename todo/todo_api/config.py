import os

secret_key = 'secretKey'
basedir = os.path.abspath(os.path.dirname(__file__))

aws_rds_db = {
    "user": "sunni546",
    "password": "sunni546",
    "host": "todo-db.c9sok0icsfl4.ap-northeast-2.rds.amazonaws.com",
    "port": "3306",
    "database": "todo",
}


class Config:
    SECRET_KEY = secret_key
    BCRYPT_LEVEL = 10

    # 문자열 URL : "dialect+driver://username:password@host:port/database"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{aws_rds_db['user']}:{aws_rds_db['password']}@{aws_rds_db['host']}:{aws_rds_db['port']}/{aws_rds_db['database']}?charset=utf8"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
