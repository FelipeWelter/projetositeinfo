import os

class Config:
    SECRET_KEY = 'sua_chave_segura_aqui'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
