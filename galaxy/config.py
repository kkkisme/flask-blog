from datetime import timedelta
import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    REMEMBER_COOKIE_DURATION = timedelta(hours=8)
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    QINIU_ACTION = 'https://up-z2.qiniup.com'
    QINIU_BUCKET = 'mypic'
    QINIU_SECRET_KEY = os.environ.get('QINIU_SECRET_KEY')
    QINIU_ACCESS_KEY = os.environ.get('QINIU_ACCESS_KEY')