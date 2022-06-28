import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'PASSWORD'
    SQLALCHEMY_DATABASE = os.environ.get('DATABASE_URL') or 'sqlite:///'
    SQLALCHEMY_TRACK_MODIFICATIONS = False