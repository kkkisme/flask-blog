from datetime import timedelta
import os


class Config:
    # SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:123456@localhost:3306/galaxy'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///galaxy.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    REMEMBER_COOKIE_DURATION = timedelta(hours=8)
