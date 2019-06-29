import os


class Config:
    DEBUG = False
    TESTING = False
    ROLLBAR_TOKEN = os.environ.get('ROLLBAR_TOKEN')
    ROLLBAR_ENVIRONMENT = None
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
    SLACK_AUTH_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
    PORT=3000


class DevelopmentConfig(Config):
    DEBUG = True
    ROLLBAR_ENVIRONMENT = 'development'


class TestingConfig(DevelopmentConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ROLLBAR_TOKEN = None
    ROLLBAR_ENVIRONMENT = 'testing'


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    ROLLBAR_ENVIRONMENT = 'production'


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
