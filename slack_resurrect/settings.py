import os


class Config:
    DEBUG = False
    TESTING = False
    ROLLBAR_TOKEN = os.environ.get('ROLLBAR_TOKEN')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
    SLACK_AUTH_TOKEN = os.environ.get('SLACK_BOT_TOKEN')


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(DevelopmentConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ROLLBAR_TOKEN = None


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


ENV = os.environ.get('APP_ENV', os.environ.get('FLASK_ENV', 'development'))
CONFIG = None

if ENV == 'dev' or ENV == 'development':
    CONFIG = DevelopmentConfig
elif ENV == 'test':
    CONFIG = TestingConfig
elif ENV == 'prod':
    CONFIG = ProductionConfig
else:
    raise ValueError('Invalid environment name')
