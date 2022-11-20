import os
basedir = os.path.abspath(os.path.dirname(__file__))
Leiders =['Kroeme','Danny','JVA','Sammy','Danny sjot','Strits']
Groepen ={'Sloebers':1,'Speelclub':2,'Rakkers':3,'Topper':4,'Kerels':5,'Aspiranten':6}


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
