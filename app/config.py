import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-later")
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'instance', 'expadvisor.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
