# app/config.py

class Config:
    SECRET_KEY = 'Abobusssss'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True


class ConfigDebug(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WTF_CSRF_ENABLED = False


class ConfigTesting(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
