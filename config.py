import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'newsdb.db')  # Путь к файлу БД
    SQLALCHEMY_TRACK_MODIFICATIONS = False

